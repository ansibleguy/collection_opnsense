from ansible.module_utils.basic import AnsibleModule

from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.cls import BaseModule


class Peer(BaseModule):
    CMDS = {
        'add': 'add_peer',
        'del': 'del_peer',
        'set': 'set_peer',
        'search': 'search_peer',
        'detail': 'get_peer',
    }
    API_KEY = 'peer'
    API_KEY_PATH = 'peer'
    API_MOD = 'kea'
    API_CONT = 'dhcpv4'
    API_CONT_REL = 'service'
    FIELDS_CHANGE = [
        'name', 'role', 'url',
    ]
    FIELDS_ALL = FIELDS_CHANGE
    FIELDS_TYPING = {
        'select': ['role'],
    }
    FIELD_ID = 'name'
    EXIST_ATTR = 'peer'

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None, fail: dict = None):
        BaseModule.__init__(self=self, m=module, r=result, s=session, f=fail)
        self.peer = {}
