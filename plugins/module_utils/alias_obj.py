from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.api import \
    Session
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.alias_helper import \
    validate_values, get_alias, equal_type, alias_in_use_by_rule
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper import \
    ensure_list
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.rule_obj import Rule

# todo: updatefreq - https://forum.opnsense.org/index.php?topic=29880.0


class Alias:
    def __init__(
            self, module: AnsibleModule, result: dict, cnf: dict = None,
            session: Session = None, fail: bool = True
    ):
        self.m = module
        self.r = result
        self.s = Session(module=module) if session is None else session
        self.cnf = self.m.params if cnf is None else cnf  # to allow override by multi_alias
        self.fail = fail
        self.exists = False
        self.alias = None
        self.call_cnf = {  # config shared by all calls
            'module': 'firewall',
            'controller': 'alias',
        }
        self.existing_rules = None  # used to check if alias is in use

    def check(self, existing_aliases: dict = None):
        # pulling alias info if it exists
        if existing_aliases is None:
            existing_aliases = self.search_call()

        self.alias = get_alias(aliases=existing_aliases['rows'], name=self.cnf['name'])
        self.exists = len(self.alias) > 0
        if self.exists:
            self.call_cnf['params'] = [self.alias['uuid']]

        if not self.exists and self.cnf['state'] == 'present':
            if self.cnf['content'] is None or len(self.cnf['content']) == 0:
                self.m.fail_json('You need to provide values to create an alias!')

    def _error(self, msg: str):
        if self.fail:
            self.m.fail_json(msg)

        else:
            self.m.warn(msg)

    def search_call(self) -> dict:
        return self.s.get(cnf={
            **self.call_cnf, **{'command': 'searchItem'}
        })

    def create(self):
        # creating alias
        validate_values(error_func=self._error, cnf=self.cnf)
        self.r['changed'] = True
        self.r['diff']['after'] = {self.cnf['name']: self.cnf['content']}

        if not self.m.check_mode:
            self.s.post(cnf={
                **self.call_cnf, **{
                    'command': 'addItem',
                    'data': {
                        'alias': {
                            'name': self.cnf['name'],
                            'description': self.cnf['description'],
                            'type': self.cnf['type'],
                            'content': '\n'.join(map(str, ensure_list(self.cnf['content']))),
                            # 'updatefreq': module.params['updatefreq_days'],
                        }
                    },
                }
            })

    def update(self):
        # checking if alias changed
        validate_values(error_func=self._error, cnf=self.cnf)

        if equal_type(existing=self.alias['type'], configured=self.cnf['type']):
            _before = list(map(str, self.alias['content'].split(',')))
            _after = list(map(str, self.cnf['content']))
            _before.sort()
            _after.sort()
            self.r['changed'] = _before != _after
            self.r['diff']['before'] = {self.cnf['name']: _before}
            self.r['diff']['after'] = {self.cnf['name']: _after}

            if self.m.params['debug'] and self.r['changed']:
                self.m.warn(f"{self.r['diff']}")

            if self.r['changed'] and not self.m.check_mode:
                # updating alias
                self.s.post(cnf={
                    **self.call_cnf, **{
                        'command': 'setItem',
                        'data': {
                            'alias': {
                                'name': self.cnf['name'],
                                'description': self.cnf['description'],
                                'type': self.cnf['type'],
                                'content': '\n'.join(map(str, ensure_list(self.cnf['content']))),
                            }
                        },
                    }
                })

        else:
            self.r['changed'] = True
            self.m.fail_json(
                f"Unable to update alias '{self.cnf['name']}' - it is not of the same type! "
                f"You need to delete the current one first!"
            )

    def delete(self):
        self.r['changed'] = True

        if self.existing_rules is None:
            self.existing_rules = Rule(
                module=self.m,
                result={},
                session=self.s,
            ).search_call()

        if alias_in_use_by_rule(rules=self.existing_rules, alias=self.cnf['name']):
            # this is to fix lacking server-side checks for the automation-rules
            # see: https://forum.opnsense.org/index.php?topic=30077.0
            alias_deletion = 'in_use'

        else:
            if not self.m.check_mode:
                # broad 'in-use' validation will be done on the server-side
                alias_deletion = self._delete_call()

            else:
                alias_deletion = ''

        if 'in_use' in alias_deletion:
            self.r['changed'] = False
            self._error(msg=f"Unable to delete alias '{self.cnf['name']}' as it is currently referenced!")

        else:
            self.r['diff']['before'] = {self.cnf['name']: self.alias['content'].split(',')}

            if self.m.params['debug']:
                self.m.warn(f"{self.r['diff']}")

    def _delete_call(self) -> dict:
        return self.s.post(cnf={**self.call_cnf, **{'command': 'delItem'}})

    def enable(self):
        if self.exists and self.alias['enabled'] != '1':
            self.r['changed'] = True
            self.r['diff']['before'] = {self.cnf['name']: {'enabled': False}}
            self.r['diff']['after'] = {self.cnf['name']: {'enabled': True}}

            if not self.m.check_mode:
                self._enable_call()

    def _enable_call(self):
        self.s.post(cnf={
            **self.call_cnf, **{
                'command': 'toggleItem',
                'params': [self.alias['uuid'], 1],
            }
        })

    def disable(self):
        if (self.exists and self.alias['enabled'] != '0') or not self.exists:
            self.r['changed'] = True
            self.r['diff']['before'] = {self.cnf['name']: {'enabled': True}}
            self.r['diff']['after'] = {self.cnf['name']: {'enabled': False}}

            if not self.m.check_mode:
                self._disable_call()

    def _disable_call(self):
        self.s.post(cnf={
            **self.call_cnf, **{
                'command': 'toggleItem',
                'params': [self.alias['uuid'], 0],
            }
        })
