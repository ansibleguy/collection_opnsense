from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.main import \
    get_matching, is_true, to_digit, get_simple_existing, get_selected, \
    validate_int_fields, get_selected_list, validate_port


class Rule:
    CMDS = {
        'add': 'addrule',
        'del': 'delrule',
        'set': 'setrule',
        'search': 'get',
        'toggle': 'togglerule',
    }
    API_KEY = 'rule'
    API_MOD = 'trafficshaper'
    API_CONT = 'settings'
    API_CONT_REL = 'service'
    API_CMD_REL = 'reconfigure'
    CHANGE_CHECK_FIELDS = [
        'target', 'sequence', 'interface', 'interface2', 'protocol', 'max_packet_length',
        'source_invert', 'source_net', 'source_port', 'destination_invert',
        'destination_net', 'destination_port', 'dscp', 'direction',
    ]
    INT_VALIDATIONS = {
        'sequence': {'min': 1, 'max': 1000000},
        'max_packet_length': {'min': 2, 'max': 65535},
    }

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None):
        self.m = module
        self.p = module.params
        self.r = result
        self.s = Session(module=module) if session is None else session
        self.exists = False
        self.rule = {}
        self.target = None
        self.call_cnf = {  # config shared by all calls
            'module': self.API_MOD,
            'controller': self.API_CONT,
        }
        self.existing_rules = None
        self.existing_queues = None
        self.existing_pipes = None

    def process(self):
        if self.p['state'] == 'absent':
            if self.exists:
                self.delete()

        else:
            if self.exists:
                self.update()

            else:
                self.create()

    def check(self):
        validate_int_fields(module=self.m, data=self.p, field_minmax=self.INT_VALIDATIONS)
        validate_port(module=self.m, port=self.p['source_port'])
        validate_port(module=self.m, port=self.p['destination_port'])

        if self.p['state'] == 'present':
            if self.p['target_pipe'] in [None, ''] and \
                    self.p['target_queue'] in [None, '']:
                self.m.fail_json(
                    "You need to provide a 'target_pipe' or 'target_queue' to "
                    "create a shaper rule!"
                )

        # checking if item exists
        self._find_rule()
        if self.exists:
            self.call_cnf['params'] = [self.rule['uuid']]

        self._find_pipe()
        if self.target is None:
            self._find_queue()

        if self.target is None and self.p['state'] == 'present':
            target_type = 'queue' if self.p['target_pipe'] in [None, ''] else 'pipe'
            self.m.fail_json(
                f"Provided {target_type} does not exist: "
                f"'{self.p[f'target_{target_type}']}'"
            )

        self.p['dscp'].sort()
        self.r['diff']['after'] = self._build_diff(self.p)

    def _find_rule(self):
        if self.existing_rules is None:
            self.existing_rules = self._search_call()

        match = get_matching(
            module=self.m, existing_items=self.existing_rules,
            compare_item=self.p, match_fields=['description'],
            simplify_func=self._simplify_existing,
        )

        if match is not None:
            self.rule = match
            self.r['diff']['before'] = self._build_diff(self.rule)
            self.exists = True

    def get_existing(self) -> list:
        return get_simple_existing(
            entries=self._search_call(),
            simplify_func=self._simplify_existing
        )

    def _search_call(self) -> dict:
        raw = self.s.get(cnf={
            **self.call_cnf, **{'command': self.CMDS['search']}
        })['ts']
        self.existing_pipes = raw['pipes']['pipe']
        self.existing_queues = raw['queues']['queue']
        return raw['rules'][self.API_KEY]

    def create(self):
        self.r['changed'] = True

        if not self.m.check_mode:
            self.s.post(cnf={
                **self.call_cnf, **{
                    'command': self.CMDS['add'],
                    'data': self._build_request(),
                }
            })

    def update(self):
        # checking if changed
        for field in self.CHANGE_CHECK_FIELDS:
            if str(self.rule[field]) != str(self.p[field]):
                self.r['changed'] = True
                break

        if not self.r['changed']:
            if self.rule['enabled'] != self.p['enabled']:
                if self.p['enabled']:
                    self.enable()

                else:
                    self.disable()

        else:
            # update if changed
            if self.p['debug']:
                self.m.warn(f"{self.r['diff']}")

            if not self.m.check_mode:
                self.s.post(cnf={
                    **self.call_cnf, **{
                        'command': self.CMDS['set'],
                        'data': self._build_request(),
                    }
                })

    @staticmethod
    def _simplify_existing(rule: dict) -> dict:
        # makes processing easier
        target_uuid = get_selected(rule['target'])
        simple = {
            'uuid': rule['uuid'],
            'sequence': rule['sequence'],
            'enabled': is_true(rule['enabled']),
            'interface': get_selected(rule['interface']),
            'interface2': get_selected(rule['interface2']),
            'protocol': get_selected(rule['proto']),
            'source_invert': is_true(rule['source_not']),
            'destination_invert': is_true(rule['destination_not']),
            'destination_net': get_selected(rule['destination']),
            'source_net': get_selected(rule['source']),
            'source_port': rule['src_port'],
            'destination_port': rule['dst_port'],
            'max_packet_length': rule['iplen'],
            'direction': get_selected(rule['direction']),
            'dscp': get_selected_list(rule['dscp']),
            'description': rule['description'],
            'target': {
                'uuid': target_uuid,
                'description': rule['target'][target_uuid]['value'],
            },
        }
        simple['dscp'].sort()
        return simple

    def _find_pipe(self):
        if self.p['target_pipe'] not in ['', None] and len(self.existing_pipes) > 0:
            for uuid, pipe in self.existing_pipes.items():
                if pipe['description'] == self.p['target_pipe']:
                    self.target = {
                        'uuid': uuid,
                        'description': pipe['description'],
                    }
                    self.p['target'] = self.target
                    break

    def _find_queue(self):
        if self.p['target_queue'] not in ['', None] and len(self.existing_queues) > 0:
            for uuid, queue in self.existing_queues.items():
                if queue['description'] == self.p['target_queue']:
                    self.target = {
                        'uuid': uuid,
                        'description': queue['description'],
                    }
                    self.p['target'] = self.target
                    break

    def _build_diff(self, data: dict) -> dict:
        relevant_int_fields = ['max_packet_length', 'sequence']
        relevant_fields = [
            'interface', 'interface2', 'protocol', 'source_invert',
            'source_net', 'source_port', 'destination_invert',
            'destination_net', 'destination_port', 'dscp', 'direction',
        ]
        diff = {}
        for field in relevant_int_fields:
            try:
                diff[field] = int(data[field])

            except (TypeError, ValueError):
                diff[field] = data[field]

        for field in relevant_fields:
            diff[field] = data[field]

        if 'target' in data:
            diff['target'] = data['target']

        if self.rule is not None and 'uuid' in self.rule:
            diff['uuid'] = self.rule['uuid']

        else:
            diff['uuid'] = None

        return diff

    def _build_request(self) -> dict:
        return {
            self.API_KEY: {
                'target': self.p['target']['uuid'],
                'enabled': to_digit(self.p['enabled']),
                'interface': self.p['interface'],
                'interface2': self.p['interface2'],
                'direction': self.p['direction'],
                'iplen': self.p['max_packet_length'],
                'proto': self.p['protocol'],
                'src_port': self.p['source_port'],
                'source': self.p['source_net'],
                'source_not': to_digit(self.p['source_invert']),
                'destination': self.p['destination_net'],
                'destination_not': to_digit(self.p['destination_invert']),
                'dst_port': self.p['destination_port'],
                'dscp': ','.join(self.p['dscp']),
                'description': self.p['description'],
            }
        }

    def delete(self):
        self.r['changed'] = True
        self.r['diff']['after'] = {}

        if not self.m.check_mode:
            self._delete_call()

            if self.p['debug']:
                self.m.warn(f"{self.r['diff']}")

    def _delete_call(self) -> dict:
        return self.s.post(cnf={**self.call_cnf, **{'command': self.CMDS['del']}})

    def enable(self):
        if self.exists and not self.rule['enabled']:
            self.r['changed'] = True
            self.r['diff']['before'] = {'enabled': False}
            self.r['diff']['after'] = {'enabled': True}

            if not self.m.check_mode:
                self._change_enabled_state(1)

    def disable(self):
        if self.exists and self.rule['enabled']:
            self.r['changed'] = True
            self.r['diff']['before'] = {'enabled': True}
            self.r['diff']['after'] = {'enabled': False}

            if not self.m.check_mode:
                self._change_enabled_state(0)

    def _change_enabled_state(self, value: int):
        self.s.post(cnf={
            **self.call_cnf, **{
                'command': self.CMDS['toggle'],
                'params': [self.rule['uuid'], value],
            }
        })

    def reload(self):
        # reload the running config
        if not self.m.check_mode:
            self.s.post(cnf={
                'module': self.API_MOD,
                'controller': self.API_CONT_REL,
                'command': self.API_CMD_REL,
                'params': []
            })
