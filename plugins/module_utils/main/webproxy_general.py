from ansible.module_utils.basic import AnsibleModule

from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.module import GeneralModule


class General(GeneralModule):
    CMDS = {
        'set': 'set',
        'search': 'get',
    }
    API_KEY_PATH = 'proxy.general'
    API_KEY_PATH_REQ = API_KEY_PATH
    API_MOD = 'proxy'
    API_CONT = 'settings'
    API_CONT_REL = 'service'
    FIELDS_CHANGE = [
        'errors', 'icp_port', 'log', 'log_store', 'log_target', 'log_ignore',
        'dns_servers', 'use_via_header', 'handling_forwarded_for',
        'hostname', 'email', 'suppress_version', 'connect_timeout', 'handling_uri_whitespace',
        'pinger', 'enabled',
    ]
    FIELDS_ALL = FIELDS_CHANGE
    FIELDS_TRANSLATE = {
        'errors': 'error_pages',
        'icp_port': 'icpPort',
        'dns_servers': 'alternateDNSservers',
        'handling_forwarded_for': 'forwardedForHandling',
        'handling_uri_whitespace': 'uriWhitespaceHandling',
        'pinger': 'enablePinger',
        'use_via_header': 'useViaHeader',
        'suppress_version': 'suppressVersion',
        'connect_timeout': 'connecttimeout',
        'email': 'VisibleEmail',
        'hostname': 'VisibleHostname',
        'log': ('logging', 'enable', 'accessLog'),
        'log_store': ('logging', 'enable', 'storeLog'),
        'log_target': ('logging', 'target'),
        'log_ignore': ('logging', 'ignoreLogACL'),
    }
    FIELDS_TYPING = {
        'bool': [
            'enabled', 'pinger', 'suppress_version', 'use_via_header', 'log', 'log_store',
        ],
        'list': ['dns_servers', 'log_ignore'],
        'select': [
            'errors', 'handling_forwarded_for', 'handling_uri_whitespace', 'log_target'
        ],
        'int': ['connect_timeout', 'icp_port'],
    }
    INT_VALIDATIONS = {
        'connect_timeout': {'min': 1, 'max': 120},
        'icp_port': {'min': 1, 'max': 65535},
    }
    TIMEOUT = 60.0  # 'disable' taking long

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None):
        GeneralModule.__init__(self=self, m=module, r=result, s=session)
