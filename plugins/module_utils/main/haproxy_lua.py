from ansible.module_utils.basic import AnsibleModule

from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.api import Session
from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.module import BaseModule


class HaproxyLua(BaseModule):
    FIELD_ID = 'name'

    CMDS = {
        'add': 'addLua',
        'del': 'delLua',
        'set': 'setLua',
        'search': 'get',
        'toggle': 'toggleLua',
    }
    API_KEY_PATH = 'haproxy.luas.lua'
    API_MOD = 'haproxy'
    API_CONT = 'settings'
    API_CONT_REL = 'service'
    API_CMD_REL = 'reconfigure'

    FIELDS_CHANGE = ['enabled', 'name', 'description', 'preload', 'filename_scheme', 'content']
    FIELDS_ALL = FIELDS_CHANGE

    EXIST_ATTR = 'haproxy_lua'

    FIELDS_TYPING = {
        'bool': ['enabled', 'preload'],
        'select': ['filename_scheme'],
    }

    STR_VALIDATIONS = {
        'name': r'^[^\t^,^;^\.^\[^\]^\{^\}]{1,255}$',
    }

    TIMEOUT = 20.0

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None):
        BaseModule.__init__(self=self, m=module, r=result, s=session)
        self.haproxy_lua = {}
