from ansible.module_utils.basic import AnsibleModule
from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.api import Session
from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.module import BaseModule


class HaproxyServer(BaseModule):
    FIELD_ID = 'name'

    CMDS = {
        'add': 'addServer',
        'del': 'delServer',
        'set': 'setServer',
        'search': 'get',
        'toggle': 'toggleServer',
    }
    API_KEY_PATH = 'haproxy.servers.server'
    API_MOD = 'haproxy'
    API_CONT = 'settings'
    API_CONT_REL = 'service'
    API_CMD_REL = 'reconfigure'

    FIELDS_TRANSLATE = {
        'service_name': 'serviceName',
        'linked_resolver': 'linkedResolver',
        'resolver_opts': 'resolverOpts',
        'resolve_prefer': 'resolvePrefer',
        'ssl_enabled': 'ssl',
        'ssl_sni': 'sslSNI',
        'ssl_verify_cert': 'sslVerify',
        'ssl_ca': 'sslCA',
        'ssl_crl': 'sslCRL',
        'ssl_client_certificate': 'sslClientCertificate',
        'max_connections': 'maxConnections',
        'check_interval': 'checkInterval',
        'check_down_interval': 'checkDownInterval',
    }

    FIELDS_CHANGE = list(FIELDS_TRANSLATE.keys()) + [
        'enabled', 'name', 'description', 'address', 'port', 'checkport',
        'mode', 'type', 'number', 'weight', 'source', 'advanced',
        'multiplexer_protocol', 'unix_socket'
    ]
    FIELDS_ALL = FIELDS_CHANGE

    FIELDS_TYPING = {
        'bool': ['enabled', 'ssl_enabled', 'ssl_verify_cert'],
        'list': ['resolver_opts', 'ssl_ca'],
        'int': ['port', 'checkport', 'max_connections', 'weight'],
        'select': [
            'mode', 'multiplexer_protocol', 'type', 'linked_resolver',
            'resolve_prefer', 'ssl_crl', 'ssl_client_certificate', 'unix_socket'
        ],
    }

    EXIST_ATTR = 'haproxy_server'

    SEARCH_ADDITIONAL = {
        'existing_resolvers': 'haproxy.resolvers.resolver',
    }

    STR_VALIDATIONS = {
        'name': r'^([0-9a-zA-Z._\-]){1,255}$',
    }

    INT_VALIDATIONS = {
        'port': {'min': 1, 'max': 65535},
        'checkport': {'min': 1, 'max': 65535},
        'max_connections': {'min': 0, 'max': 10000000},
        'weight': {'min': 0, 'max': 256},
    }

    TIMEOUT = 20.0

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None):
        BaseModule.__init__(self=self, m=module, r=result, s=session)
        self.haproxy_server = {}
        # Initialize existing items that might be referenced
        self.existing_resolvers = {}

    def check(self) -> None:
        self._base_check()
        if self.p['state'] == 'present':
            # Validate linked resolver
            if self.p.get('linked_resolver'):
                self.find_single_link(
                    field='linked_resolver',
                    existing=self.existing_resolvers,
                )
