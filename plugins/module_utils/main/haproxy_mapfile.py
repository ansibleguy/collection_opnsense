from ansible.module_utils.basic import AnsibleModule
from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.api import Session
from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.module import BaseModule
from ansible_collections.oxlorg.opnsense.plugins.module_utils.helper.main import \
    is_unset


class HaproxyMapfile(BaseModule):
    FIELD_ID = 'name'

    CMDS = {
        'add': 'addMapfile',
        'del': 'delMapfile',
        'set': 'setMapfile',
        'search': 'get',
        'toggle': 'toggleMapfile',
    }
    API_KEY_PATH = 'haproxy.mapfiles.mapfile'
    API_MOD = 'haproxy'
    API_CONT = 'settings'
    API_CONT_REL = 'service'
    API_CMD_REL = 'reconfigure'

    FIELDS_CHANGE = ['name', 'description', 'content']
    FIELDS_ALL = FIELDS_CHANGE

    EXIST_ATTR = 'haproxy_mapfile'

    FIELDS_TYPING = {}

    STR_VALIDATIONS = {
        'name': r'^[^\t^,^;^\.^\[^\]^\{^\}]{1,255}$',
        'description': r'^.{1,255}$',
    }

    TIMEOUT = 20.0

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None):
        BaseModule.__init__(self=self, m=module, r=result, s=session)
        self.haproxy_mapfile = {}

    def check(self) -> None:
        if self.p['state'] == 'present':
            if is_unset(self.p['content']):
                self.m.fail_json("You need to provide a 'content' to create a haproxy_mapfile!")

        self._base_check()
