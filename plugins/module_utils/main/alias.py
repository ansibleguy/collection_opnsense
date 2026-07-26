from ansible.module_utils.basic import AnsibleModule

from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.handler import \
    ModuleSoftError
from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.oxlorg.opnsense.plugins.module_utils.helper.alias import \
    validate_values, filter_builtin_alias, build_updatefreq
from ansible_collections.oxlorg.opnsense.plugins.module_utils.helper.main import \
    is_unset
from ansible_collections.oxlorg.opnsense.plugins.module_utils.helper.translate import \
    get_simple_existing, simplify_translate
from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.module import BaseModule


class Alias(BaseModule):
    FIELD_ID = 'name'
    CMDS = {
        'add': 'add_item',
        'del': 'del_item',
        'set': 'set_item',
        'search': 'get',
        'toggle': 'toggleItem',
    }
    API_KEY_PATH = 'alias.aliases.alias'
    API_MOD = 'firewall'
    API_CONT = 'alias'
    FIELDS_CHANGE = ['content', 'description', 'statistics']
    FIELDS_ALL = ['name', 'type', 'enabled']
    FIELDS_ALL.extend(FIELDS_CHANGE)
    FIELDS_ALL.extend([
        'updatefreq_days', 'interface', 'path_expression',
        'url_auth_type', 'url_username', 'url_password',
    ])
    FIELDS_DIFF_NO_LOG = ['url_password']
    FIELDS_TRANSLATE = {
        'statistics': 'counters',
        'updatefreq_days': 'updatefreq',
        'url_auth_type': 'authtype',
        'url_username': 'username',
        'url_password': 'password',
    }
    FIELDS_TYPING = {
        'bool': ['enabled', 'statistics'],
        'select': ['type', 'interface'],
    }
    EXIST_ATTR = 'alias'
    JOIN_CHAR = '\n'
    TIMEOUT = 20.0
    MAX_ALIAS_LEN = 32

    def __init__(
            self, module: AnsibleModule, result: dict, multi: dict = None,
            session: Session = None, fail: dict = None,
    ):
        BaseModule.__init__(self=self, m=module, r=result, s=session, f=fail, multi=multi)
        self.alias = {}

    def check(self) -> None:
        if self.p['type'] == 'urltable':
            self.FIELDS_CHANGE = self.FIELDS_CHANGE + ['updatefreq_days']
            self.p['updatefreq_days'] = build_updatefreq(self.p['updatefreq_days'], default=True)

        elif self.p['type'] == 'urljson':
            self.FIELDS_CHANGE = self.FIELDS_CHANGE + ['updatefreq_days', 'path_expression']
            self.p['updatefreq_days'] = build_updatefreq(self.p['updatefreq_days'], default=True)

        elif self.p['type'] == 'dynipv6host':
            if is_unset(self.p['interface']):
                self.m.fail_json('You need to provide an interface to create a dynipv6host alias!')

            self.FIELDS_CHANGE = self.FIELDS_CHANGE + ['interface']

        if len(self.p['name']) > self.MAX_ALIAS_LEN:
            self._error(
                f"Alias name '{self.p['name']}' is invalid - "
                f"must be shorter than {self.MAX_ALIAS_LEN} characters",
            )

        self.find(match_fields=[self.FIELD_ID])

        if self.p['state'] == 'present':
            validate_values(error_func=self._error, cnf=self.p, existing_entries=self.existing_entries)

        self._base_check()

    def simplify_existing(self, alias: dict) -> dict:
        simple = {}

        if isinstance(alias['content'], dict):
            simple['content'] = [item for item in alias['content'].keys() if item != '']

        else:
            # if function is re-applied
            return alias

        simple = {
            **simplify_translate(
                existing=alias,
                typing=self.FIELDS_TYPING,
                translate=self.FIELDS_TRANSLATE,
            ),
            **simple,
        }

        if simple['type'] in ['urltable', 'urljson']:
            simple['updatefreq_days'] = build_updatefreq(alias['updatefreq'], default=False)

        return simple

    def update(self) -> None:
        # checking if alias changed
        if self.alias['type'] == self.p['type']:
            self._base_update()

        else:
            self.r['changed'] = True
            self._error(
                msg=f"Unable to update alias '{self.p[self.FIELD_ID]}' - it is not of the same type! "
                    f"You need to delete the current one first!",
                verification=False,
            )

    def delete(self) -> None:
        response = self._base_delete()

        if 'in_use' in response:
            self._error(
                msg=f"Unable to delete alias '{self.p[self.FIELD_ID]}' as it is currently referenced!",
                verification=False,
            )

    def _error(self, msg: str, verification: bool = True) -> None:
        if (verification and self.fail_verify) or (not verification and self.fail_process):
            self.m.fail_json(msg)

        else:
            self.m.warn(msg)
            raise ModuleSoftError

    def get_existing(self) -> list:
        return filter_builtin_alias(
            get_simple_existing(
                entries=self.search(),
                simplify_func=self.simplify_existing,
            )
        )
