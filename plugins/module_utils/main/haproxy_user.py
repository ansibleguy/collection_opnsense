from ansible.module_utils.basic import AnsibleModule

from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.api import Session
from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.module import BaseModule


class HaproxyUser(BaseModule):
    FIELD_ID = 'name'

    CMDS = {
        'add': 'addUser',
        'del': 'delUser',
        'set': 'setUser',
        'search': 'get',
        'toggle': 'toggleUser',
    }
    API_KEY_PATH = 'haproxy.users.user'
    API_MOD = 'haproxy'
    API_CONT = 'settings'
    API_CONT_REL = 'service'
    API_CMD_REL = 'reconfigure'

    FIELDS_CHANGE = ['enabled', 'name', 'description', 'password']
    FIELDS_ALL = FIELDS_CHANGE

    FIELDS_DIFF_NO_LOG = ['password']

    EXIST_ATTR = 'haproxy_user'

    FIELDS_TYPING = {
        'bool': ['enabled'],
    }

    TIMEOUT = 20.0

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None):
        BaseModule.__init__(self=self, m=module, r=result, s=session)
        self.haproxy_user = {}
