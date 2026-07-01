from ansible.module_utils.basic import AnsibleModule

from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.api import Session
from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.module import GeneralModule


class HaproxyGeneralDefaults(GeneralModule):
    CMDS = {
        'set': 'set',
        'search': 'get',
    }
    API_KEY_PATH = 'haproxy.general.defaults'
    API_KEY_PATH_REQ = API_KEY_PATH
    API_MOD = 'haproxy'
    API_CONT = 'settings'
    API_CONT_REL = 'service'
    API_CMD_REL = 'reconfigure'

    FIELDS_TRANSLATE = {
        'max_connections': 'maxConnections',
        'max_connections_servers': 'maxConnectionsServers',
        'timeout_client': 'timeoutClient',
        'timeout_connect': 'timeoutConnect',
        'timeout_check': 'timeoutCheck',
        'timeout_server': 'timeoutServer',
        'custom_options': 'customOptions'
    }

    FIELDS_CHANGE = list(FIELDS_TRANSLATE.keys()) + ['retries', 'redispatch', 'init_addr' ]
    FIELDS_ALL = FIELDS_CHANGE

    FIELDS_TYPING = {
        'int': ['max_connections', 'max_connections_servers', 'retries'],
        'select': ['redispatch'],
        'list': ['init_addr'],
    }

    INT_VALIDATIONS = {
        'max_connections': {'min': 0, 'max': 10000000},
        'max_connections_servers': {'min': 0, 'max': 10000000},
        'retries': {'min': 0, 'max': 100},
    }

    TIMEOUT = 60.0

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None):
        GeneralModule.__init__(self=self, m=module, r=result, s=session)
        