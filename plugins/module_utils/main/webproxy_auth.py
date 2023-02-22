from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.cls import GeneralModule


class General(GeneralModule):
    CMDS = {
        'set': 'set',
        'search': 'get',
    }
    API_KEY_PATH = 'proxy.forward.authentication'
    API_KEY_PATH_REQ = API_KEY_PATH
    API_MOD = 'proxy'
    API_CONT = 'settings'
    API_CONT_REL = 'service'
    API_CMD_REL = 'reconfigure'
    FIELDS_CHANGE = ['method', 'group', 'prompt', 'ttl_h', 'processes']
    FIELDS_ALL = FIELDS_CHANGE
    FIELDS_TRANSLATE = {
        'group': 'authEnforceGroup',
        'prompt': 'realm',
        'ttl_h': 'credentialsttl',
        'processes': 'children',
    }
    FIELDS_TYPING = {
        'int': ['ttl_h', 'processes'],
        'select': ['method', 'group'],
    }
    STR_LEN_VALIDATIONS = {
        'prompt': {'min': 0, 'max': 255}
    }

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None):
        GeneralModule.__init__(self=self, m=module, r=result, s=session)
