from ansible.module_utils.basic import AnsibleModule

from ansible_collections.oxlorg.opnsense.plugins.module_utils.helper.main import \
    is_unset
from ansible_collections.oxlorg.opnsense.plugins.module_utils.helper.translate import \
    get_key_by_value_from_selection
from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.module import BaseModule


class User(BaseModule):
    FIELD_ID = 'name'
    CMDS = {
        'add': 'add',
        'del': 'del',
        'set': 'set',
        'search': 'search',
        'detail': 'get',
    }
    API_KEY_PATH = 'user'
    API_MOD = 'auth'
    API_CONT = 'user'
    FIELDS_CHANGE = [
        'enabled', 'description', 'email', 'comment', 'landing_page', 'language', 'shell', 'expires',
        'authorized_keys'
    ]
    FIELDS_TYPING = {
        'bool': ['scrambled_password', 'enabled'],
        'select': ['shell', 'language'],
        'list': ['privilege', 'membership'],
    }
    FIELDS_TRANSLATE = {
        'authorized_keys': 'authorizedkeys',
        'description': 'descr',
        'enabled': 'disabled',
        'privilege': 'priv',
        'membership': 'group_memberships'
    }
    FIELDS_BOOL_INVERT = ['enabled']
    FIELDS_DIFF_NO_LOG = ['otp_seed', 'password', 'scrambled_password', 'apikeys']
    FIELDS_ALL = ['name', 'password', 'scrambled_password', 'privilege', 'membership']
    FIELDS_ALL.extend(FIELDS_CHANGE)
    EXIST_ATTR = 'user'

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None):
        BaseModule.__init__(self=self, m=module, r=result, s=session)
        self.user = {}

    def check(self) -> None:
        if (
            self.p['update_password'] == 'always' and
            not (is_unset(self.p['password']) and is_unset(self.p['scrambled_password']))
        ):
            self.FIELDS_CHANGE = self.FIELDS_CHANGE + ['password', 'scrambled_password']

        self._base_check()

        if not is_unset(self.p['membership']) or self.p['membership'] == []:
            self.FIELDS_CHANGE = self.FIELDS_CHANGE + ['membership']
            self.p['membership'] = [
                get_key_by_value_from_selection(self.raw['group_memberships'], g)
                for g in self.p['membership']
            ]
        if not is_unset(self.p['privilege']) or self.p['privilege'] == []:
            self.FIELDS_CHANGE = self.FIELDS_CHANGE + ['privilege']

    def create(self) -> None:
        if is_unset(self.p['password']) and is_unset(self.p['scrambled_password']):
            self.p['scrambled_password'] = True

        self._base_create()

    def update(self) -> None:
        self._base_update(enable_switch=False)

    def delete(self) -> None:
        if self.user['scope'] == 'system':
            self.m.fail_json(f"Not allowed to delete system user {self.user['name']}")

        self._base_delete()
