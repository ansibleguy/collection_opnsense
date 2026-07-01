from ansible.module_utils.basic import AnsibleModule

from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.api import Session
from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.module import BaseModule


class HaproxyGroup(BaseModule):
    FIELD_ID = 'name'

    CMDS = {
        'add': 'addGroup',
        'del': 'delGroup',
        'set': 'setGroup',
        'search': 'get',
        'toggle': 'toggleGroup',
    }
    API_KEY_PATH = 'haproxy.groups.group'
    API_MOD = 'haproxy'
    API_CONT = 'settings'
    API_CONT_REL = 'service'
    API_CMD_REL = 'reconfigure'

    FIELDS_CHANGE = ['enabled', 'name', 'description', 'members', 'add_userlist']
    FIELDS_ALL = FIELDS_CHANGE

    EXIST_ATTR = 'haproxy_group'

    FIELDS_TYPING = {
        'bool': ['enabled', 'add_userlist'],
        'list': ['members']
    }

    SEARCH_ADDITIONAL = {
        'existing_users': 'haproxy.users.user',
    }

    TIMEOUT = 20.0

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None):
        BaseModule.__init__(self=self, m=module, r=result, s=session)
        self.haproxy_group = {}
        self.existing_users = {}

    def check(self) -> None:
        self._base_check()

        if self.p['state'] == 'present':
            self.find_multiple_links(
                field='members',
                existing=self.existing_users,
                existing_field_id='name',
            )
