from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.main import \
    validate_int_fields, is_unset, get_key_by_value_from_selection, get_key_by_value_end_from_selection
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.cls import BaseModule


class Server(BaseModule):
    FIELD_ID = 'name'
    CMDS = {
        'add': 'add',
        'del': 'del',
        'set': 'set',
        'search': 'search',
        'detail': 'get',
        'toggle': 'toggle',
    }
    API_KEY_PATH = 'instance'
    API_MOD = 'openvpn'
    API_CONT = 'instances'
    API_CONT_REL = 'service'
    API_CMD_REL = 'reconfigure'
    FIELDS_CHANGE = [
        'protocol', 'port', 'address', 'mode', 'log_level', 'keepalive_interval', 'keepalive_timeout',
        'certificate', 'ca', 'key', 'authentication', 'renegotiate_time', 'network_local', 'network_remote',
        'options', 'mtu', 'fragment_size', 'mss_fix', 'server_ip4', 'server_ip6', 'max_connections',
        'topology', 'crl', 'verify_client_cert', 'cert_depth', 'data_ciphers', 'data_cipher_fallback',
        'ocsp', 'auth_mode', 'auth_group', 'user_as_cn', 'user_cn_strict', 'auth_token_time', 'push_options',
        'redirect_gateway', 'route_metric', 'register_dns', 'domain', 'domain_list', 'dns_servers',
        'ntp_servers',
    ]
    FIELDS_ALL = ['role', 'enabled', 'vpnid', FIELD_ID]
    FIELDS_ALL.extend(FIELDS_CHANGE)
    FIELDS_TRANSLATE = {
        'name': 'description',
        'protocol': 'proto',
        'address': 'local',
        'mode': 'dev_type',
        'log_level': 'verb',
        'certificate': 'cert',
        'authentication': 'auth',
        'renegotiate_time': 'reneg-sec',
        'network_local': 'push_route',
        'network_remote': 'route',
        'options': 'various_flags',
        'mtu': 'tun_mtu',
        'fragment_size': 'fragment',
        'mss_fix': 'mssfix',
        'key': 'tls_key',
        'server_ip4': 'server',
        'server_ip6': 'server_ipv6',
        'auth_mode': 'authmode',
        'auth_group': 'local_group',
        'max_connections': 'maxclients',
        'user_as_cn': 'username_as_common_name',
        'user_cn_strict': 'strictusercn',
        'auth_token_time': 'auth-gen-token',
        'push_options': 'various_push_flags',
        'domain': 'dns_domain',
        'domain_list': 'dns_domain_search',
        'ocsp': 'use_ocsp',
        'data_ciphers': 'data-ciphers',
        'data_cipher_fallback': 'data-ciphers-fallback',
    }
    FIELDS_BOOL_INVERT = []
    FIELDS_TYPING = {
        'bool': ['enabled', 'mss_fix', 'ocsp', 'user_as_cn', 'user_cn_strict', 'register_dns'],
        'list': [
            'network_local', 'network_remote', 'options', 'data_ciphers', 'auth_mode', 'push_options',
            'redirect_gateway', 'domain_list', 'dns_servers', 'ntp_servers',
        ],
        'select': [
            'certificate', 'ca', 'key', 'authentication', 'carp_depend_on', 'log_level',
            'mode', 'protocol', 'role', 'topology', 'crl', 'verify_client_cert', 'cert_depth',
            'data_cipher_fallback', 'auth_group',
        ],
        'select_opt_list_idx': ['log_level'],
        'int': ['fragment_size', 'mtu', 'route_metric'],
    }
    INT_VALIDATIONS = {
        'mtu': {'min': 60, 'max': 65535},
        'fragment_size': {'min': 0, 'max': 65528},
        'route_metric': {'min': 0, 'max': 65535},
    }
    EXIST_ATTR = 'instance'
    FIELDS_DIFF_EXCLUDE = ['vpnid', 'role']

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None):
        BaseModule.__init__(self=self, m=module, r=result, s=session)
        self.instance = {}

    def check(self) -> None:
        self.p['role'] = 'server'

        if self.p['state'] == 'present':
            validate_int_fields(module=self.m, data=self.p, field_minmax=self.INT_VALIDATIONS)

            if is_unset(self.p['server_ip4']) and is_unset(self.p['server_ip6']):
                self.m.fail_json(
                    "You need to either provide a 'server_ip4' or 'server_ip6' network to create an openvpn-server!"
                )

            if is_unset(self.p['certificate']) and is_unset(self.p['ca']):
                self.m.fail_json(
                    "You need to either provide a 'certificate' or 'ca' to create an openvpn-server!"
                )


        self._base_check()

        if not is_unset(self.p['ca']):
            self.p['ca'] = get_key_by_value_from_selection(
                selection=self.b.raw['ca'],
                value=self.p['ca'],
            )

        if not is_unset(self.p['certificate']):
            self.p['certificate'] = get_key_by_value_from_selection(
                selection=self.b.raw[self.FIELDS_TRANSLATE['certificate']],
                value=self.p['certificate'],
            )

        if not is_unset(self.p['crl']):
            self.p['crl'] = get_key_by_value_from_selection(
                selection=self.b.raw[self.FIELDS_TRANSLATE['crl']],
                value=self.p['crl'],
            )

        if not is_unset(self.p['key']):
            self.p['key'] = get_key_by_value_end_from_selection(
                selection=self.b.raw[self.FIELDS_TRANSLATE['key']],
                value=self.p['key'],
            )

        if self.p['state'] == 'present':
            self.r['diff']['after'] = self.b.build_diff(data=self.p)
