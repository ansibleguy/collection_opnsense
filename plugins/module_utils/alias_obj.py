from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.api import \
    Session
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.alias_helper import \
    validate_values, alias_in_use_by_rule, filter_builtin_alias
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper import \
    ensure_list, get_matching, get_simple_existing, is_true, get_selected
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.rule_obj import Rule


class Alias:
    FIELD_ID = 'name'
    CMDS = {
        'add': 'addItem',
        'del': 'delItem',
        'set': 'setItem',
        'search': 'get',
        'toggle': 'toggleItem',
    }
    API_KEY = 'alias'
    API_MOD = 'firewall'
    API_CONT = 'alias'
    API_CMD_REL = 'reconfigure'
    CHANGE_CHECK_FIELDS = ['enabled', 'content', 'description']

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

                else:
                    self._error('You need to provide values to create an alias!')

    def check(self):
        # pulling alias info if it exists
        if self.existing_aliases is None:
            self.existing_aliases = self.search_call()

        self.alias = get_matching(
            module=self.m, existing_items=self.existing_aliases,
            compare_item=self.cnf, match_fields=[self.FIELD_ID],
            simplify_func=self.simplify_existing,
        )

        if self.alias is not None:
            self.exists = True
            self.call_cnf['params'] = [self.alias['uuid']]

    def _error(self, msg: str):
        if self.fail:
            self.m.fail_json(msg)

        else:
            self.m.warn(msg)

    def get_existing(self) -> list:
        return filter_builtin_alias(
            get_simple_existing(
                entries=self.search_call(),
                simplify_func=self.simplify_existing,
            )
        )

    def search_call(self) -> dict:
        # returns list of alias-dicts
        return self.s.get(cnf={
            **self.call_cnf, **{'command': self.CMDS['search']}
        })['alias']['aliases'][self.API_KEY]

    @staticmethod
    def simplify_existing(alias: dict) -> dict:
        # makes processing easier
        simple = {
            'uuid': alias['uuid'],
            'name': alias['name'],
            'content': list(alias['content'].keys()),
            'description': alias['description'],
            'type': get_selected(alias['type']),
            'enabled': is_true(alias['enabled']),
        }

        if simple['type'] == 'urltable':
            try:
                simple['updatefreq_days'] = float(alias['updatefreq'])

            except ValueError:
                simple['updatefreq_days'] = float(0)

        return simple

    def create(self):
        # creating alias
        validate_values(error_func=self._error, cnf=self.cnf)
        self.r['changed'] = True
        self.r['diff']['after'] = {self.cnf[self.FIELD_ID]: self._build_diff(self.cnf)}

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

        if self.alias['type'] == self.cnf['type']:
            _before = self._build_diff(data=self.alias)
            _after = self._build_diff(data=self.cnf)

            for field in self.CHANGE_CHECK_FIELDS:
                if _before[field] != _after[field]:
                    self.r['changed'] = True
                    break

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
            self._error(
                f"Unable to update alias '{self.cnf[self.FIELD_ID]}' - it is not of the same type! "
                f"You need to delete the current one first!"
            )

    def _build_diff(self, data: dict) -> dict:
        diff = {
            # 'name': data['name'],  # as it is the FIELD_ID
            'type': data['type'],
            'enabled': data['enabled'],
            'content': data['content'],
            'description': data['description'],
        }
        if self.alias is not None and 'uuid' in self.alias:
            diff['uuid'] = self.alias['uuid']

        else:
            diff['uuid'] = None

        diff['content'].sort()

        if data['type'] == 'urltable':
            diff['updatefreq_days'] = round(data['updatefreq_days'], 1)

        return diff

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
            self.r['diff']['before'] = {self.cnf[self.FIELD_ID]: self.alias['content']}

            if self.m.params['debug']:
                self.m.warn(f"{self.r['diff']}")

    def _delete_call(self) -> dict:
        return self.s.post(cnf={**self.call_cnf, **{'command': self.CMDS['del']}})

    def enable(self):
        if self.exists and not self.alias['enabled']:
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
        if self.exists and self.alias['enabled']:
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

    def reload(self):
        # reload the aliases to apply changes
        if not self.m.check_mode:
            self.s.post(cnf={
                **self.call_cnf, **{'command': self.API_CMD_REL, 'params': []}
            })
