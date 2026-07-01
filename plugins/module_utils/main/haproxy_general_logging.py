from ansible.module_utils.basic import AnsibleModule

from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.api import Session
from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.module import GeneralModule


class HaproxyGeneralLogging(GeneralModule):
    CMDS = {
        'set': 'set',
        'search': 'get',
    }
    API_KEY_PATH = 'haproxy.general.logging'
    API_KEY_PATH_REQ = API_KEY_PATH
    API_MOD = 'haproxy'
    API_CONT = 'settings'
    API_CONT_REL = 'service'
    API_CMD_REL = 'reconfigure'

    FIELDS_CHANGE = ['host', 'facility', 'level', 'length']
    FIELDS_ALL = FIELDS_CHANGE

    FIELDS_TYPING = {
        'select': ['facility', 'level'],
        'int': ['length'],
    }

    INT_VALIDATIONS = {
        'length': {'min': 64, 'max': 65535},
    }

    TIMEOUT = 60.0

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None):
        GeneralModule.__init__(self=self, m=module, r=result, s=session)
    