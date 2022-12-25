from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.cls import GeneralModule


class General(GeneralModule):
    CMDS = {
        'set': 'set',
        'search': 'get',
    }
    API_KEY_PATH = 'proxy.forward'
    API_KEY_PATH_REQ = API_KEY_PATH
    API_MOD = 'proxy'
    API_CONT = 'settings'
    API_CONT_REL = 'service'
    API_CMD_REL = 'reconfigure'
    FIELDS_CHANGE = [
        'interfaces', 'port', 'port_ssl', 'transparent', 'ssl_inspection',
        'ssl_inspection_sni_only', 'ssl_ca', 'ssl_exclude', 'ssl_cache_mb',
        'ssl_workers', 'allow_interface_subnets', 'snmp', 'port_snmp',
        'snmp_password', 'interfaces_ftp', 'port_ftp', 'transparent_ftp',
    ]
    FIELDS_ALL = FIELDS_CHANGE
    FIELDS_TRANSLATE = {
        'port_ssl': 'sslbumpport',
        'transparent': 'transparentMode',
        'ssl_inspection': 'sslbump',
        'ssl_inspection_sni_only': 'sslurlonly',
        'ssl_ca': 'sslcertificate',
        'ssl_exclude': 'sslnobumpsites',
        'ssl_cache_mb': 'ssl_crtd_storage_max_size',
        'ssl_workers': 'sslcrtd_children',
        'allow_interface_subnets': 'addACLforInterfaceSubnets',
        'snmp': 'snmp_enable',
        'port_snmp': 'snmp_port',
        'interfaces_ftp': 'ftpInterfaces',
        'port_ftp': 'ftpPort',
        'transparent_ftp': 'ftpTransparentMode',
    }
    FIELDS_TYPING = {
        'bool': [
            'transparent_ftp', 'snmp', 'allow_interface_subnets', 'ssl_inspection_sni_only',
            'ssl_inspection', 'transparent',
        ],
        'list': ['interfaces', 'ssl_exclude', 'interfaces_ftp'],
        'int': ['port', 'port_ssl', 'ssl_cache_mb', 'ssl_workers', 'port_snmp'],
        'select': ['ssl_ca'],
    }
    FIELDS_IGNORE = ['acl', 'icap', 'authentication']
    INT_VALIDATIONS = {
        'ssl_workers': {'min': 1, 'max': 32},
        'ssl_cache_mb': {'min': 1, 'max': 65535},
        'port': {'min': 1, 'max': 65535},
        'port_ssl': {'min': 1, 'max': 65535},
        'port_snmp': {'min': 1, 'max': 65535},
    }
    FIELDS_DIFF_EXCLUDE = ['snmp_password']

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None):
        GeneralModule.__init__(self=self, m=module, r=result, s=session)
