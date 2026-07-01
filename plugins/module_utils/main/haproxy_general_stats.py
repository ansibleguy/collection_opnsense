from ansible.module_utils.basic import AnsibleModule

from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.api import Session
from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.module import GeneralModule


class HaproxyGeneralStats(GeneralModule):
    CMDS = {
        'set': 'set',
        'search': 'get',
    }
    API_KEY_PATH = 'haproxy.general.stats'
    API_KEY_PATH_REQ = API_KEY_PATH
    API_MOD = 'haproxy'
    API_CONT = 'settings'
    API_CONT_REL = 'service'
    API_CMD_REL = 'reconfigure'

    FIELDS_TRANSLATE = {
        'remote_enabled': 'remoteEnabled',
        'remote_bind': 'remoteBind',
        'auth_enabled': 'authEnabled',
        'allowed_users': 'allowedUsers',
        'allowed_groups': 'allowedGroups',
        'custom_options': 'customOptions'
    }

    FIELDS_CHANGE = list(FIELDS_TRANSLATE.keys())
    FIELDS_CHANGE += ['enabled', 'port', 'users', 'prometheus_enabled', 'prometheus_bind', 'prometheus_path']
    FIELDS_ALL = FIELDS_CHANGE

    FIELDS_TYPING = {
        'bool': ['enabled', 'remote_enabled', 'auth_enabled', 'prometheus_enabled'],
        'int': ['port'],
        'list': ['remote_bind', 'users', 'allowed_users', 'allowed_groups', 'prometheus_bind'],
    }

    INT_VALIDATIONS = {
        'port': {'min': 1024, 'max': 65535},
    }

    SEARCH_ADDITIONAL = {
        'existing_users': 'haproxy.users.user',
        'existing_groups': 'haproxy.groups.group',
    }

    TIMEOUT = 60.0

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None):
        GeneralModule.__init__(self=self, m=module, r=result, s=session)
        self.existing_users = {}
        self.existing_groups = {}

    def check(self) -> None:
        self._base_check()

        self.find_multiple_links(
            field='allowed_users',
            existing=self.existing_users,
            existing_field_id='name',
        )
        self.find_multiple_links(
            field='allowed_groups',
            existing=self.existing_groups,
            existing_field_id='name',
        )
