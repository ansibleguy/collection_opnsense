from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper import ensure_list
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.api import Session
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.rule_helper import \
    get_rule, validate_values, get_any_change


class Rule:
    CMDS = {
        'add': 'addRule',
        'del': 'delRule',
        'set': 'setRule',
        'search': 'get',
        'toggle': 'toggleRule',
    }
    API_KEY = 'rule'

    def __init__(
            self, module: AnsibleModule, result: dict, cnf: dict = None,
            session: Session = None, fail: bool = True
    ):
        self.m = module
        self.p = module.params
        self.r = result
        self.s = Session(module=module) if session is None else session
        self.cnf = self.p if cnf is None else cnf  # to allow override by rule_multi
        self.fail = fail
        self.exists = False
        self.rule = None
        self.log_name = None
        self.call_cnf = {  # config shared by all calls
            'module': 'firewall',
            'controller': 'filter',
        }
        self.existing_rules = None

    def process(self):
        if self.cnf['state'] == 'absent':
            if self.exists:
                self.delete()

        else:
            if self.exists:
                self.update()

            else:
                self.create()

    def check(self):
        self._build_log_name()

        # pulling rule info if it exists
        if self.existing_rules is None:
            self.existing_rules = self.search_call()

        if self.p['debug']:
            self.m.warn(f"EXISTING RULES: {self.existing_rules}")

        self.rule = get_rule(
            rules=self.existing_rules,
            cnf=self.cnf,
        )
        self.exists = len(self.rule) > 0
        if self.exists:
            self.call_cnf['params'] = [self.rule['uuid']]

    def _error(self, msg: str):
        if self.fail:
            self.m.fail_json(msg)

        else:
            self.m.warn(msg)

    def search_call(self) -> dict:
        # returns dict of rules
        rules = self.s.get(cnf={
            **self.call_cnf, **{'command': self.CMDS['search']}
        })['filter']['rules'][self.API_KEY]

        if isinstance(rules, list) and len(rules) == 0:
            # I guess server-side PHP is interpreting the empty named-array as simple array
            return {}

        return rules

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

    def update(self):
        # checking if rule changed
        validate_values(error_func=self._error, module=self.m, cnf=self.cnf)
        _before = self._build_diff(cnf=self.rule)
        _after = self._build_diff(cnf=self.cnf)
        self.r['changed'] = get_any_change(before=_before, after=_after)
        self.r['diff']['before'] = _before
        self.r['diff']['after'] = _after

        if self.p['debug'] and self.r['changed']:
            self.m.warn(f"{self.r['diff']}")

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

            if self.p['debug']:
                self.m.warn(f"{self.r['diff']}")

    def _delete_call(self) -> dict:
        return self.s.post(cnf={
            **self.call_cnf, **{'command': self.CMDS['del']}
        })

    def enable(self):
        if self.exists and self.rule['enabled'] not in [1, '1', True]:
            self.r['changed'] = True
            self.r['diff']['before'] = {'enabled': False}
            self.r['diff']['after'] = {'enabled': True}

            if not self.m.check_mode:
                self._change_enabled_state(1)

    def disable(self):
        if (self.exists and self.rule['enabled'] not in [0, '0', False]) or not self.exists:
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
            'gateway', 'log', 'description'
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
                'enabled': 1 if self.cnf['enabled'] else 0,
                'sequence': self.cnf['sequence'],
                'action': self.cnf['action'],
                'quick': 1 if self.cnf['quick'] else 0,
                'interface': ','.join(map(str, ensure_list(self.cnf['interface']))),
                'direction': self.cnf['direction'],
                'ipprotocol': self.cnf['ip_protocol'],
                'protocol': self.cnf['protocol'],
                'source_not': 1 if self.cnf['source_invert'] else 0,
                'source_net': self.cnf['source_net'],
                'source_port': '' if self.cnf['source_port'] is None else self.cnf['source_port'],
                'destination_not': 1 if self.cnf['destination_invert'] else 0,
                'destination_net': self.cnf['destination_net'],
                'destination_port': '' if self.cnf['destination_port'] is None else self.cnf['destination_port'],
                'log': 1 if self.cnf['log'] else 0,
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
