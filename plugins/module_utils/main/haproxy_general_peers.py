from ansible.module_utils.basic import AnsibleModule

from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.api import Session
from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.module import GeneralModule


class HaproxyGeneralPeers(GeneralModule):
    CMDS = {
        'set': 'set',
        'search': 'get',
    }
    API_KEY_PATH = 'haproxy.general.peers'
    API_KEY_PATH_REQ = API_KEY_PATH
    API_MOD = 'haproxy'
    API_CONT = 'settings'
    API_CONT_REL = 'service'
    API_CMD_REL = 'reconfigure'

    FIELDS_CHANGE = ['enabled', 'name1', 'listen1', 'port1', 'name2', 'listen2', 'port2']
    FIELDS_ALL = FIELDS_CHANGE

    FIELDS_TYPING = {
        'bool': ['enabled'],
        'int': ['port1', 'port2'],
    }

    INT_VALIDATIONS = {
        'port1': {'min': 1, 'max': 65535},
        'port2': {'min': 1, 'max': 65535},
    }

    TIMEOUT = 60.0

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None):
        GeneralModule.__init__(self=self, m=module, r=result, s=session)
