from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.api import \
    Session
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.alias_helper import \
    validate_values, get_alias, equal_type, alias_in_use_by_rule, compare_aliases
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper import \
    ensure_list
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.rule_obj import Rule


class Alias:
    FIELD_ID = 'name'
    CMDS = {
        'add': 'addItem',
        'del': 'delItem',
        'set': 'setItem',
        'search': 'searchItem',
        'detail': 'getItem',
        'toggle': 'toggleItem',
    }
    API_KEY = 'alias'
    API_MOD = 'firewall'
    API_CONT = 'alias'

    def __init__(
            self, module: AnsibleModule, result: dict, cnf: dict = None,
            session: Session = None, fail: bool = True
    ):
        self.m = module
        self.r = result
        self.s = Session(module=module) if session is None else session
        self.cnf = self.m.params if cnf is None else cnf  # to allow override by alias_multi
        self.fail = fail
        self.exists = False
        self.alias = None
        self.call_cnf = {  # config shared by all calls
            'module': self.API_MOD,
            'controller': self.API_CONT,
        }
        self.existing_aliases = None
        self.existing_rules = None  # used to check if alias is in use

    def process(self):
        if self.cnf['state'] == 'absent':
            if self.exists:
                self.delete()

        else:
            if self.cnf['content'] is not None and len(self.cnf['content']) > 0:
                if self.exists:
                    self.update()

                else:
                    self.create()

            else:
                # allow en-/disabling without providing content
                if self.exists:
                    if self.cnf['enabled']:
                        self.enable()

                    else:
                        self.disable()

    def check(self):
        # pulling alias info if it exists
        if self.existing_aliases is None:
            self.existing_aliases = self.search_call()

        self.alias = get_alias(aliases=self.existing_aliases, name=self.cnf[self.FIELD_ID])
        self.exists = len(self.alias) > 0
        if self.exists:
            self.call_cnf['params'] = [self.alias['uuid']]
            if self.cnf['type'] == 'urltable':
                try:
                    self.alias['updatefreq_days'] = float(self.detail_call()['updatefreq'].strip())

                except ValueError:
                    self.alias['updatefreq_days'] = float(0)

        if not self.exists and self.cnf['state'] == 'present':
            if self.cnf['content'] is None or len(self.cnf['content']) == 0:
                self.m.fail_json('You need to provide values to create an alias!')

    def _error(self, msg: str):
        if self.fail:
            self.m.fail_json(msg)

        else:
            self.m.warn(msg)

    def search_call(self) -> list:
        # returns list of alias-dicts
        return self.s.get(cnf={
            **self.call_cnf, **{'command': self.CMDS['search']}
        })['rows']

    def detail_call(self) -> dict:
        return self.s.get(cnf={
            **self.call_cnf, **{'command': self.CMDS['detail']}
        })[self.API_KEY]

    def create(self):
        # creating alias
        validate_values(error_func=self._error, cnf=self.cnf)
        self.r['changed'] = True
        self.r['diff']['after'] = {self.cnf[self.FIELD_ID]: self.cnf['content']}

        if not self.m.check_mode:
            self.s.post(cnf={
                **self.call_cnf, **{
                    'command': self.CMDS['add'],
                    'data': self._build_request(),
                }
            })

    def update(self):
        # checking if alias changed
        validate_values(error_func=self._error, cnf=self.cnf)

        if equal_type(existing=self.alias['type'], configured=self.cnf['type']):
            self.r['changed'], _before, _after = compare_aliases(
                existing=self.alias, configured=self.cnf,
            )

            if self.cnf['type'] == 'urltable':
                if self.alias['updatefreq_days'] != self.cnf['updatefreq_days']:
                    self.r['changed'] = True
                    _before = {
                        'content': _before,
                        'updatefreq_days': round(self.alias['updatefreq_days'], 1)
                    }
                    _after = {
                        'content': _after,
                        'updatefreq_days': round(self.cnf['updatefreq_days'], 1)
                    }

            self.r['diff']['before'] = {self.cnf[self.FIELD_ID]: _before}
            self.r['diff']['after'] = {self.cnf[self.FIELD_ID]: _after}

            if self.m.params['debug'] and self.r['changed']:
                self.m.warn(f"{self.r['diff']}")

            if self.r['changed'] and not self.m.check_mode:
                # updating alias
                self.s.post(cnf={
                    **self.call_cnf, **{
                        'command': self.CMDS['set'],
                        'data': self._build_request(),
                    }
                })

        else:
            self.r['changed'] = True
            self.m.fail_json(
                f"Unable to update alias '{self.cnf[self.FIELD_ID]}' - it is not of the same type! "
                f"You need to delete the current one first!"
            )

    def _build_request(self) -> dict:
        return {
            self.API_KEY: {
                'name': self.cnf[self.FIELD_ID],
                'description': self.cnf['description'],
                'type': self.cnf['type'],
                'content': '\n'.join(map(str, ensure_list(self.cnf['content']))),
                'updatefreq': self.cnf['updatefreq_days'],
            }
        }

    def delete(self):
        self.r['changed'] = True

        if self.existing_rules is None:
            self.existing_rules = Rule(
                module=self.m,
                result={},
                session=self.s,
            ).search_call()

        if alias_in_use_by_rule(rules=self.existing_rules, alias=self.cnf[self.FIELD_ID]):
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
            self._error(msg=f"Unable to delete alias '{self.cnf[self.FIELD_ID]}' as it is currently referenced!")

        else:
            self.r['diff']['before'] = {self.cnf[self.FIELD_ID]: self.alias['content'].split(',')}

            if self.m.params['debug']:
                self.m.warn(f"{self.r['diff']}")

    def _delete_call(self) -> dict:
        return self.s.post(cnf={**self.call_cnf, **{'command': self.CMDS['del']}})

    def enable(self):
        if self.exists and self.alias['enabled'] != '1':
            self.r['changed'] = True
            self.r['diff']['before'] = {self.cnf[self.FIELD_ID]: {'enabled': False}}
            self.r['diff']['after'] = {self.cnf[self.FIELD_ID]: {'enabled': True}}

            if not self.m.check_mode:
                self._enable_call()

    def _enable_call(self):
        self.s.post(cnf={
            **self.call_cnf, **{
                'command': self.CMDS['toggle'],
                'params': [self.alias['uuid'], 1],
            }
        })

    def disable(self):
        if (self.exists and self.alias['enabled'] != '0') or not self.exists:
            self.r['changed'] = True
            self.r['diff']['before'] = {self.cnf[self.FIELD_ID]: {'enabled': True}}
            self.r['diff']['after'] = {self.cnf[self.FIELD_ID]: {'enabled': False}}

            if not self.m.check_mode:
                self._disable_call()

    def _disable_call(self):
        self.s.post(cnf={
            **self.call_cnf, **{
                'command': 'toggleItem',
                'params': [self.alias['uuid'], 0],
            }
        })

    def reconfigure(self):
        # reload the aliases to apply changes
        if not self.m.check_mode:
            self.s.post(cnf={
                **self.call_cnf, **{'command': 'reconfigure', 'params': []}
            })
