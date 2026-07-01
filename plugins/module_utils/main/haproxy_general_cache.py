from ansible.module_utils.basic import AnsibleModule

from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.api import Session
from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.module import GeneralModule


class HaproxyGeneralCache(GeneralModule):
    CMDS = {
        'set': 'set',
        'search': 'get',
    }
    API_KEY_PATH = 'haproxy.general.cache'
    API_KEY_PATH_REQ = API_KEY_PATH
    API_MOD = 'haproxy'
    API_CONT = 'settings'
    API_CONT_REL = 'service'
    API_CMD_REL = 'reconfigure'

    FIELDS_TRANSLATE = {
        'total_max_size': 'totalMaxSize',
        'max_age': 'maxAge',
        'max_object_size': 'maxObjectSize',
        'process_vary': 'processVary',
        'max_secondary_entries': 'maxSecondaryEntries',
    }

    FIELDS_CHANGE = list(FIELDS_TRANSLATE.keys()) + ['enabled']
    FIELDS_ALL = FIELDS_CHANGE

    FIELDS_TYPING = {
        'bool': ['enabled', 'process_vary'],
        'int': ['total_max_size', 'max_age', 'max_object_size', 'max_secondary_entries'],
    }

    INT_VALIDATIONS = {
        'total_max_size': {'min': 1, 'max': 4095},
        'max_age': {'min': 1, 'max': 3600},
        'max_object_size': {'min': 1, 'max': 2146435072},
        'max_secondary_entries': {'min': 1},
    }

    TIMEOUT = 60.0

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None):
        GeneralModule.__init__(self=self, m=module, r=result, s=session)
