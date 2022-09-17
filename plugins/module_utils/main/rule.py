from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.main import \
    ensure_list, is_true, to_digit, get_selected_list, get_selected, get_matching, \
    get_simple_existing
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.api import Session
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.rule import \
    validate_values, get_state_change, get_config_change


class Rule:
    CMDS = {
        'add': 'addRule',
        'del': 'delRule',
        'set': 'setRule',
        'search': 'get',
        'toggle': 'toggleRule',
    }
    API_KEY = 'rule'
    API_MOD = 'firewall'
    API_CONT = 'filter'

    def __init__(
            self, module: AnsibleModule, result: dict, cnf: dict = None,
            session: Session = None, fail: bool = True
    ):
        self.m = module
        self.r = result
        self.s = Session(module=module) if session is None else session
        self.cnf = self.m.params if cnf is None else cnf  # to allow override by rule_multi
        self.fail = fail
        self.exists = False
        self.rule = None
        self.log_name = None
        self.call_cnf = {  # config shared by all calls
            'module': self.API_MOD,
            'controller': self.API_CONT,
        }
        self.existing_rules = None

    def process(self):
        if self.cnf['state'] == 'absent':
            if self.exists:
                self.delete()

        else:
            if self.exists:
                config_changed, state_changed = self._changed()
                if config_changed:
                    self.update()

                elif state_changed:
                    if self.cnf['enabled']:
                        self.enable()

                    else:
                        self.disable()

            else:
                self.create()

    def check(self):
        self._build_log_name()

        # pulling rule info if it exists
        if self.existing_rules is None:
            self.existing_rules = self.search_call()

        if self.m.params['debug']:
            self.m.warn(f"EXISTING RULES: {self.existing_rules}")

        self.rule = get_matching(
            module=self.m, existing_items=self.existing_rules,
            compare_item=self.cnf, match_fields=self.cnf['match_fields'],
            simplify_func=self.simplify_existing,
        )

        if self.rule is not None:
            self.exists = True
            self.call_cnf['params'] = [self.rule['uuid']]

    @staticmethod
    def simplify_existing(rule):
        # because the return of api/firewall/filter/get is too verbose for easy access
        simple = {
            'uuid': rule['uuid'],
            'enabled': is_true(rule['enabled']),
            'log': is_true(rule['log']),
            'quick': is_true(rule['quick']),
            'source_invert': is_true(rule['source_not']),
            'destination_invert': is_true(rule['destination_not']),
            'action': get_selected(data=rule['action']),
            'interface': get_selected_list(data=rule['interface']),
            'direction': get_selected(data=rule['direction']),
            'ip_protocol': get_selected(data=rule['ipprotocol']),
            'protocol': get_selected(data=rule['protocol']),
            'gateway': get_selected(data=rule['gateway']),
        }

        for field in [
            'sequence', 'source_net', 'source_not', 'source_port', 'destination_net',
            'destination_not', 'destination_port', 'description'
        ]:
            simple[field] = rule[field]

        return simple

    def _error(self, msg: str):
        if self.fail:
            self.m.fail_json(msg)

        else:
            self.m.warn(msg)

    def get_existing(self) -> list:
        return get_simple_existing(
            entries=self.search_call(),
            simplify_func=self.simplify_existing
        )

    def search_call(self) -> (dict, list):
        # returns dict of rules
        return self.s.get(cnf={
            **self.call_cnf, **{'command': self.CMDS['search']}
        })['filter']['rules'][self.API_KEY]

    def create(self):
        # creating rule
        validate_values(error_func=self._error, module=self.m, cnf=self.cnf)
        self.r['changed'] = True
        self.r['diff']['after'] = self._build_diff(cnf=self.cnf)
        if not self.m.check_mode:
            self.s.post(cnf={
                **self.call_cnf, **{
                    'command': self.CMDS['add'],
                    'data': self._build_request()
                }
            })

    def _changed(self) -> tuple:
        # check if config changed
        validate_values(error_func=self._error, module=self.m, cnf=self.cnf)
        _before = self._build_diff(cnf=self.rule)
        _after = self._build_diff(cnf=self.cnf)
        self.r['diff']['before'] = _before
        self.r['diff']['after'] = _after

        config_changed = get_config_change(before=_before, after=_after)
        state_changed = get_state_change(before=_before, after=_after)
        self.r['changed'] = any([config_changed, state_changed])

        if self.m.params['debug'] and self.r['changed']:
            self.m.warn(f"{self.r['diff']} {config_changed} {state_changed}")

        return config_changed, state_changed

    def update(self):
        if self.r['changed'] and not self.m.check_mode:
            # updating rule
            self.s.post(cnf={
                **self.call_cnf, **{
                    'command': self.CMDS['set'],
                    'data': self._build_request(),
                }
            })

    def delete(self):
        self.r['changed'] = True
        if not self.m.check_mode:
            # NOTE: there is currently no practical way to check if the rule is in use..
            rule_deletion = self._delete_call()

            if 'status' in rule_deletion and rule_deletion['status'] == 'failed':
                self.r['changed'] = False
                self.m.warn(f"Unable to delete rule '{self.log_name}' as it is currently referenced!")

        if self.r['changed']:
            self.r['diff']['before'] = self._build_diff(cnf=self.rule)

            if self.m.params['debug']:
                self.m.warn(f"{self.r['diff']}")

    def _delete_call(self) -> dict:
        return self.s.post(cnf={
            **self.call_cnf, **{'command': self.CMDS['del']}
        })

    def enable(self):
        if self.exists and not is_true(self.rule['enabled']):
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

    @staticmethod
    def _build_diff(cnf: dict) -> dict:
        diff = {}
        relevant_fields = [
            'action', 'quick', 'direction', 'ip_protocol', 'protocol',
            'source_invert', 'source_net', 'destination_invert', 'destination_net',
            'gateway', 'log', 'description', 'enabled',
        ]

        # special case..
        diff['sequence'] = str(cnf['sequence'])
        diff['destination_port'] = str(cnf['destination_port'])
        diff['source_port'] = str(cnf['source_port'])
        diff['interface'] = ','.join(map(str, ensure_list(cnf['interface'])))

        for field in relevant_fields:
            diff[field] = cnf[field]

        return diff

    def _build_request(self) -> dict:
        return {
            self.API_KEY: {
                'enabled': to_digit(self.cnf['enabled']),
                'sequence': self.cnf['sequence'],
                'action': self.cnf['action'],
                'quick': to_digit(self.cnf['quick']),
                'interface': ','.join(map(str, ensure_list(self.cnf['interface']))),
                'direction': self.cnf['direction'],
                'ipprotocol': self.cnf['ip_protocol'],
                'protocol': self.cnf['protocol'],
                'source_not': to_digit(self.cnf['source_invert']),
                'source_net': self.cnf['source_net'],
                'source_port': '' if self.cnf['source_port'] is None else self.cnf['source_port'],
                'destination_not': to_digit(self.cnf['destination_invert']),
                'destination_net': self.cnf['destination_net'],
                'destination_port': '' if self.cnf['destination_port'] is None else self.cnf['destination_port'],
                'log': to_digit(self.cnf['log']),
                'description': self.cnf['description'],
            }
        }

    def _build_log_name(self) -> str:
        if self.cnf['description'] not in [None, '']:
            log_name = self.cnf['description']

        else:
            log_name = f"{self.cnf['action'].upper()}: FROM "

            if self.cnf['source_invert']:
                log_name += 'NOT '

            log_name += f"{self.cnf['source_net']} <= PROTO {self.cnf['protocol']} => "

            if self.cnf['destination_invert']:
                log_name += 'NOT '

            log_name += f"{self.cnf['destination_net']}:{self.cnf['destination_port']}"

        return log_name
