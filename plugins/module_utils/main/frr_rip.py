from ansible.module_utils.basic import AnsibleModule

from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.module import GeneralModule


class Rip(GeneralModule):
    CMDS = {
        'set': 'set',
        'search': 'get',
    }
    API_KEY_PATH = 'rip'
    API_MOD = 'quagga'
    API_CONT = 'rip'
    API_CONT_REL = 'service'
    FIELDS_CHANGE = [
        'version', 'metric', 'passive_ints', 'enabled', 'networks',
        'redistribute',
    ]
    FIELDS_ALL = FIELDS_CHANGE
    FIELDS_TRANSLATE = {
        'passive_ints': 'passiveinterfaces',
        'metric': 'defaultmetric',
    }
    FIELDS_TYPING = {
        'bool': ['enabled'],
        'list': ['passive_ints', 'networks', 'redistribute'],
        'int': ['version'],
    }
    INT_VALIDATIONS = {
        'version': {'min': 1, 'max': 2},
        'metric': {'min': 1, 'max': 16},
    }

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None):
        GeneralModule.__init__(self=self, m=module, r=result, s=session)
