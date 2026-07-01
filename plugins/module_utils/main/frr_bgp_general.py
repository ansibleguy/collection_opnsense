from ansible.module_utils.basic import AnsibleModule

from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.module import GeneralModule


class General(GeneralModule):
    CMDS = {
        'set': 'set',
        'search': 'get',
    }
    API_KEY_PATH = 'bgp'
    API_MOD = 'quagga'
    API_CONT = 'bgp'
    API_CONT_REL = 'service'
    FIELDS_CHANGE = [
        'as_number', 'id', 'graceful', 'enabled', 'networks', 'distance', 'log_neighbor_changes',
        'network_import_check',
    ]
    FIELDS_ALL = FIELDS_CHANGE
    FIELDS_TRANSLATE = {
        'as_number': 'asnumber',
        'id': 'routerid',
        'log_neighbor_changes': 'logneighborchanges',
        'network_import_check': 'networkimportcheck',
    }
    FIELDS_TYPING = {
        'bool': ['enabled', 'graceful', 'network_import_check', 'log_neighbor_changes'],
        'list': ['networks'],
        'int': ['distance', 'as_number'],
    }
    INT_VALIDATIONS = {
        'as_number': {'min': 1, 'max': 4294967295},
        'distance': {'min': 1, 'max': 255},
    }

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None):
        GeneralModule.__init__(self=self, m=module, r=result, s=session)
