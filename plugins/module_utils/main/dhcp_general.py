from ansible.module_utils.basic import AnsibleModule

from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.module import GeneralModule


class General(GeneralModule):
    CMDS = {
        'set': 'set',
        'search': 'get'
    }
    API_KEY_PATH = 'dhcpv4.general'
    API_KEY_PATH_REQ = API_KEY_PATH
    API_MOD = 'kea'
    API_CONT = 'dhcpv4'
    API_CONT_REL = 'service'
    FIELDS_CHANGE = [
        'enabled', 'interfaces', 'socket_type', 'fw_rules', 'lifetime'
    ]
    FIELDS_ALL = FIELDS_CHANGE
    FIELDS_TRANSLATE = {
        'lifetime': 'valid_lifetime',
        'fw_rules': 'fwrules',
        'socket_type': 'dhcp_socket_type',
    }
    FIELDS_TYPING = {
        'bool': ['enabled', 'fw_rules'],
        'int': ['lifetime'],
        'list': ['interfaces'],
        'select': ['socket_type'],
    }
    INT_VALIDATIONS = {
        'lifetime': {'min': 0},
    }

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None):
        GeneralModule.__init__(self=self, m=module, r=result, s=session)
