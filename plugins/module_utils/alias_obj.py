from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.api import \
    Session
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.api_helper import \
    check_or_load_credentials
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.alias_helper import \
    validate_values, get_alias, equal_type


class Alias:
    def __init__(
            self, module: AnsibleModule, result: dict, cnf: dict = None,
            session: Session = None, fail: bool = True
    ):
        self.m = module
        self.r = result
        check_or_load_credentials(module=module)
        self.s = Session(module=module) if session is None else session
        self.cnf = self.m.params if cnf is None else cnf  # to allow override by multi_alias
        self.fail = fail
        self.exists = False
        self.alias = None
        self.call_cnf = {  # config shared by all calls
            'module': 'firewall',
            'controller': 'alias',
            'allowed_http_stati': [200, 'done'],
        }

    def check(self, existing_aliases: dict = None):
        # pulling alias info if it exists
        if existing_aliases is None:
            existing_aliases = self.pull_call()

        self.alias = get_alias(aliases=existing_aliases['rows'], name=self.cnf['name'])
        self.exists = len(self.alias) > 0
        if self.exists:
            self.call_cnf.update({
                'params': [self.alias['uuid']],
            })

        if not self.exists and self.cnf['state'] == 'present':
            if self.cnf['content'] is None or len(self.cnf['content']) == 0:
                self.m.fail_json('You need to provide values to create an alias!')

            validate_values(error_func=self._error, cnf=self.cnf)

    def _error(self, msg: str):
        if self.fail:
            self.m.fail_json(msg)

        else:
            self.m.warn(msg)

    def pull_call(self) -> dict:
        return self.s.get(cnf={
            **self.call_cnf, **{'command': 'searchItem'}
        })

    def create(self):
        # creating alias
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
                            'content': '\n'.join(self.cnf['content']),
                            # 'updatefreq': module.params['updatefreq_days'],
                        }
                    },
                }
            })

    def update(self):
        # checking if alias changed
        if equal_type(existing=self.alias['type'], configured=self.cnf['type']):
            _before = self.alias['content'].split(',')
            _after = self.cnf['content']
            _before.sort()
            _after.sort()
            self.r['changed'] = _before != _after
            self.r['diff']['before'] = {self.cnf['name']: _before}
            self.r['diff']['after'] = {self.cnf['name']: _after}

            if self.m.params['debug'] and self.r['changed']:
                self.m.warn(self.r['diff'])

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
                                'content': '\n'.join(self.cnf['content']),
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
        if not self.m.check_mode:
            # NOTE: there is currently no practical way to check if the alias is in use..
            alias_deletion = self._delete_call()

            if 'status' in alias_deletion and alias_deletion['status'] == 'failed':
                self.r['changed'] = False
                self.m.warn(f"Unable to delete alias '{self.cnf['name']}' as it is currently referenced!")

        if self.r['changed']:
            self.r['diff']['before'] = {self.cnf['name']: self.alias['content'].split(',')}

            if self.m.params['debug']:
                self.m.warn(self.r['diff'])

    def _delete_call(self) -> dict:
        return self.s.post(cnf={
            **self.call_cnf, **{
                'command': 'delItem',
                'allowed_http_stati': [200, 'failed'],  # allowing 'failed' to catch it with a warning
            }
        })

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
