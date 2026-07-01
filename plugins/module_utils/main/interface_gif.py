from ansible.module_utils.basic import AnsibleModule

from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.module import BaseModule


class Gif(BaseModule):
    FIELD_ID = 'description'
    CMDS = {
        'add': 'add_item',
        'del': 'del_item',
        'set': 'set_item',
        'search': 'get',
        'toggle': 'toggleItem',
    }
    API_KEY_PATH = 'gif.gif'
    API_MOD = 'interfaces'
    API_CONT = 'gif_settings'
    FIELDS_CHANGE = [
        'local', 'remote', 'tunnel_local', 'tunnel_remote', 'tunnel_remote_net', 'ingress_filtering', 'ecn_friendly',
    ]
    FIELDS_ALL = [FIELD_ID]
    FIELDS_ALL.extend(FIELDS_CHANGE)
    FIELDS_TRANSLATE = {
        'description': 'descr',
        'local': 'local-addr',
        'remote': 'remote-addr',
        'tunnel_local': 'tunnel-local-addr',
        'tunnel_remote': 'tunnel-remote-addr',
        'tunnel_remote_net': 'tunnel-remote-net',
        'ingress_filtering': 'link2',
        'ecn_friendly': 'link1',
    }
    FIELDS_BOOL_INVERT = ['ingress_filtering']
    FIELDS_TYPING = {
        'bool': ['ingress_filtering', 'ecn_friendly'],
        'list': [],
        'select': [],
        'int': ['tunnel_remote_net'],
    }
    INT_VALIDATIONS = {
        'tunnel_remote_net': {'min': 1, 'max': 128},
    }
    EXIST_ATTR = 'gif'

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None):
        BaseModule.__init__(self=self, m=module, r=result, s=session)
        self.gif = {}
