from ansible.module_utils.basic import AnsibleModule

from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.module import BaseModule


class Gre(BaseModule):
    FIELD_ID = 'description'
    CMDS = {
        'add': 'add_item',
        'del': 'del_item',
        'set': 'set_item',
        'search': 'get',
        'toggle': 'toggleItem',
    }
    API_KEY_PATH = 'gre.gre'
    API_MOD = 'interfaces'
    API_CONT = 'gre_settings'
    FIELDS_CHANGE = ['local', 'remote', 'tunnel_local', 'tunnel_remote', 'tunnel_remote_net']
    FIELDS_ALL = [FIELD_ID]
    FIELDS_ALL.extend(FIELDS_CHANGE)
    FIELDS_TRANSLATE = {
        'description': 'descr',
        'local': 'local-addr',
        'remote': 'remote-addr',
        'tunnel_local': 'tunnel-local-addr',
        'tunnel_remote': 'tunnel-remote-addr',
        'tunnel_remote_net': 'tunnel-remote-net',
    }
    FIELDS_TYPING = {
        'bool': [],
        'list': [],
        'select': [],
        'int': ['tunnel_remote_net'],
    }
    INT_VALIDATIONS = {
        'tunnel_remote_net': {'min': 1, 'max': 128},
    }
    EXIST_ATTR = 'gre'

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None, fail: dict = None):
        BaseModule.__init__(self=self, m=module, r=result, s=session, f=fail)
        self.gre = {}
