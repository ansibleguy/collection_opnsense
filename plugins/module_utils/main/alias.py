from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.alias import \
    validate_values, alias_in_use_by_rule, filter_builtin_alias
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.main import \
    get_simple_existing, is_true, get_selected
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.main.rule import Rule
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.base import Base


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
    API_KEY_1 = 'alias'
    API_KEY_2 = 'aliases'
    API_MOD = 'firewall'
    API_CONT = 'alias'
    API_CMD_REL = 'reconfigure'
    FIELDS_CHANGE = ['enabled', 'content', 'description']
    FIELDS_ALL = ['name', 'type']
    FIELDS_ALL.extend(FIELDS_CHANGE)
    FIELDS_TRANSLATE = {
        'updatefreq_days': 'updatefreq',
    }
    EXIST_ATTR = 'alias'
    JOIN_CHAR = '\n'
    TIMEOUT = 20.0

    def __init__(
            self, module: AnsibleModule, result: dict, cnf: dict = None,
            session: Session = None, fail: bool = True
    ):
        self.m = module
        self.r = result
        self.s = Session(module=module, timeout=self.TIMEOUT) if session is None else session
        self.p = self.m.params if cnf is None else cnf  # to allow override by alias_multi
        self.fail = fail
        self.exists = False
        self.alias = {}
        self.call_cnf = {  # config shared by all calls
            'module': self.API_MOD,
            'controller': self.API_CONT,
        }
        self.existing_entries = None
        self.existing_rules = None  # used to check if alias is in use
        self.b = Base(instance=self)

    def check(self):
        if self.p['state'] == 'present':
            validate_values(error_func=self._error, cnf=self.p)

        self.b.find(match_fields=[self.FIELD_ID])

        if self.p['state'] == 'present':
            self.r['diff']['after'] = self.b.build_diff(data=self.p)

    @staticmethod
    def simplify_existing(alias: dict) -> dict:
        # makes processing easier
        simple = {
            'uuid': alias['uuid'],
            'name': alias['name'],
            'content': [item for item in alias['content'].keys() if item != ''],
            'description': alias['description'],
            'type': get_selected(alias['type']),
            'enabled': is_true(alias['enabled']),
        }

        if simple['type'] == 'urltable':
            try:
                simple['updatefreq_days'] = round(float(alias['updatefreq']), 1)

            except ValueError:
                simple['updatefreq_days'] = float(0)

        return simple

    def update(self):
        # checking if alias changed
        if self.alias['type'] == self.p['type']:
            self.b.update()

        else:
            self.r['changed'] = True
            self._error(
                f"Unable to update alias '{self.p[self.FIELD_ID]}' - it is not of the same type! "
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

        if alias_in_use_by_rule(rules=self.existing_rules, alias=self.p[self.FIELD_ID]):
            # this is to fix lacking server-side checks for the automation-rules
            # see: https://forum.opnsense.org/index.php?topic=30077.msg145259#msg145259
            alias_deletion = 'in_use'

        else:
            if not self.m.check_mode:
                # broad 'in-use' validation will be done on the server-side
                alias_deletion = self._delete_call()

            else:
                alias_deletion = ''

        if 'in_use' in alias_deletion:
            self.r['changed'] = False
            self._error(msg=f"Unable to delete alias '{self.p[self.FIELD_ID]}' as it is currently referenced!")

        else:
            self.r['diff']['before'] = {self.p[self.FIELD_ID]: self.alias['content']}

            if self.m.params['debug']:
                self.m.warn(f"{self.r['diff']}")

    def _delete_call(self) -> dict:
        return self.s.post(cnf={**self.call_cnf, **{'command': self.CMDS['del']}})

    def _error(self, msg: str):
        if self.fail:
            self.m.fail_json(msg)

        else:
            self.m.warn(msg)

    def get_existing(self) -> list:
        return filter_builtin_alias(
            get_simple_existing(
                entries=self.b.search(),
                simplify_func=self.simplify_existing,
            )
        )

    def search_call(self) -> list:
        return self.b.search()

    def process(self):
        self.b.process()

    def create(self):
        self.b.create()

    def reload(self):
        self.b.reload()

    def enable(self):
        self.b.enable()

    def disable(self):
        self.b.disable()
