from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.main import \
    get_matching, is_true, to_digit, get_simple_existing, get_selected, validate_int_fields


class Pipe:
    CMDS = {
        'add': 'addPipe',
        'del': 'delPipe',
        'set': 'setPipe',
        'search': 'get',
        'toggle': 'togglePipe',
    }
    API_KEY = 'pipe'
    API_MOD = 'trafficshaper'
    API_CONT = 'settings'
    API_CONT_REL = 'service'
    API_CMD_REL = 'reconfigure'
    CHANGE_CHECK_FIELDS = [
        'bw', 'bw_metric', 'queue', 'mask', 'buckets', 'scheduler',
        'codel_enable', 'codel_target', 'codel_interval', 'codel_ecn_enable',
        'pie_enable', 'fqcodel_quantum', 'fqcodel_limit', 'fqcodel_flows',
        'delay', 'description',
    ]
    INT_VALIDATIONS = {
        # 'id': {'min': 1, 'max': 65535},
        'queue': {'min': 2, 'max': 100},
        'buckets': {'min': 1, 'max': 65535},
        'codel_target': {'min': 1, 'max': 10000},
        'codel_interval': {'min': 1, 'max': 10000},
        'fqcodel_quantum': {'min': 1, 'max': 65535},
        'fqcodel_limit': {'min': 1, 'max': 65535},
        'fqcodel_flows': {'min': 1, 'max': 65535},
        'delay': {'min': 1, 'max': 3000},
    }

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None):
        self.m = module
        self.p = module.params
        self.r = result
        self.s = Session(module=module) if session is None else session
        self.exists = False
        self.pipe = {}
        self.call_cnf = {  # config shared by all calls
            'module': self.API_MOD,
            'controller': self.API_CONT,
        }
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
        if self.p['state'] == 'present' and self.p['bw'] is None:
            self.m.fail_json('You need to provide bandwidth to create a shaper pipe!')

        validate_int_fields(module=self.m, data=self.p, field_minmax=self.INT_VALIDATIONS)

        # checking if item exists
        self._find_pipe()
        if self.exists:
            self.call_cnf['params'] = [self.pipe['uuid']]

        self.r['diff']['after'] = self._build_diff(self.p)

    def _find_pipe(self):
        if self.existing_pipes is None:
            self.existing_pipes = self._search_call()

        match = get_matching(
            module=self.m, existing_items=self.existing_pipes,
            compare_item=self.p, match_fields=['description'],
            simplify_func=self._simplify_existing,
        )

        if match is not None:
            self.pipe = match
            self.r['diff']['before'] = self._build_diff(self.pipe)
            self.exists = True

    def get_existing(self) -> list:
        return get_simple_existing(
            entries=self._search_call(),
            simplify_func=self._simplify_existing
        )

    def _search_call(self) -> dict:
        return self.s.get(cnf={
            **self.call_cnf, **{'command': self.CMDS['search']}
        })['ts']['pipes'][self.API_KEY]

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
            if str(self.pipe[field]) != str(self.p[field]):
                self.r['changed'] = True
                break

        if not self.r['changed']:
            if self.pipe['enabled'] != self.p['enabled']:
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
    def _simplify_existing(pipe: dict) -> dict:
        # makes processing easier
        return {
            'uuid': pipe['uuid'],
            'enabled': is_true(pipe['enabled']),
            'bw': pipe['bandwidth'],
            'bw_metric': get_selected(pipe['bandwidthMetric']),
            'queue': pipe['queue'],
            'mask': get_selected(pipe['mask']),
            'buckets': pipe['buckets'],
            'scheduler': get_selected(pipe['scheduler']),
            'pie_enable': is_true(pipe['pie_enable']),
            'codel_enable': is_true(pipe['codel_enable']),
            'codel_ecn_enable': is_true(pipe['codel_ecn_enable']),
            'codel_target': pipe['codel_target'],
            'codel_interval': pipe['codel_interval'],
            'fqcodel_quantum': pipe['fqcodel_quantum'],
            'fqcodel_limit': pipe['fqcodel_limit'],
            'fqcodel_flows': pipe['fqcodel_flows'],
            'delay': pipe['delay'],
            'description': pipe['description'],
        }

    def _build_diff(self, data: dict) -> dict:
        relevant_int_fields = [
            'bw', 'queue', 'buckets', 'codel_target', 'codel_interval', 'fqcodel_quantum',
            'fqcodel_limit', 'fqcodel_flows', 'delay',
        ]
        relevant_fields = [
            'codel_enable', 'codel_ecn_enable', 'pie_enable', 'enabled',
            'bw_metric', 'scheduler', 'mask', 'description',
        ]
        diff = {}
        for field in relevant_int_fields:
            try:
                diff[field] = int(data[field])

            except (TypeError, ValueError):
                diff[field] = data[field]

        for field in relevant_fields:
            diff[field] = data[field]

        if self.pipe is not None and 'uuid' in self.pipe:
            diff['uuid'] = self.pipe['uuid']

        else:
            diff['uuid'] = None

        return diff

    def _build_request(self) -> dict:
        return {
            self.API_KEY: {
                'enabled': to_digit(self.p['enabled']),
                'bandwidth': self.p['bw'],
                'bandwidthMetric': self.p['bw_metric'],
                'queue': self.p['queue'],
                'mask': self.p['mask'],
                'buckets': self.p['buckets'],
                'scheduler': self.p['scheduler'],
                'pie_enable': to_digit(self.p['pie_enable']),
                'codel_enable': to_digit(self.p['codel_enable']),
                'codel_ecn_enable': to_digit(self.p['codel_enable']),
                'codel_target': self.p['codel_target'],
                'codel_interval': self.p['codel_interval'],
                'fqcodel_quantum': self.p['fqcodel_quantum'],
                'fqcodel_limit': self.p['fqcodel_limit'],
                'fqcodel_flows': self.p['fqcodel_flows'],
                'delay': self.p['delay'],
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
        if self.exists and not self.pipe['enabled']:
            self.r['changed'] = True
            self.r['diff']['before'] = {'enabled': False}
            self.r['diff']['after'] = {'enabled': True}

            if not self.m.check_mode:
                self._change_enabled_state(1)

    def disable(self):
        if self.exists and self.pipe['enabled']:
            self.r['changed'] = True
            self.r['diff']['before'] = {'enabled': True}
            self.r['diff']['after'] = {'enabled': False}

            if not self.m.check_mode:
                self._change_enabled_state(0)

    def _change_enabled_state(self, value: int):
        self.s.post(cnf={
            **self.call_cnf, **{
                'command': self.CMDS['toggle'],
                'params': [self.pipe['uuid'], value],
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
