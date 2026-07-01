from ansible.module_utils.basic import AnsibleModule

from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.module import GeneralModule


class General(GeneralModule):
    CMDS = {
        'set': 'set',
        'search': 'get'
    }
    API_KEY_PATH = 'dnsmasq'
    API_MOD = 'dnsmasq'
    API_CONT = 'settings'
    API_CONT_REL = 'service'
    FIELDS_CHANGE = [
        'enabled', 'interfaces', 'regdhcp', 'regdhcpstatic', 'domain_needed', 'port', 'dnssec',
        'resolve_etc_hosts', 'dhcpfirst', 'strict_order', 'strictbind', 'forward_private_reverse', 'log_queries',
        'ident', 'regdhcpdomain', 'dns_forward_max', 'cache_size', 'local_ttl', 'resolv_system',
        'add_mac', 'add_subnet', 'add_subnet', 'dhcp_disable_interfaces', 'dhcp_fqdn', 'dhcp_domain',
        'dhcp_local', 'dhcp_lease_max', 'dhcp_authoritative', 'dhcp_reply_delay', 'dhcp_default_fw_rules',
        'dhcp_enable_ra', 'dhcp_hasync',
    ]
    FIELDS_ALL = FIELDS_CHANGE
    FIELDS_TRANSLATE = {
        'enabled': 'enable',
        'interfaces': 'interface',
        'resolve_etc_hosts': 'no_hosts',
        'ident': 'no_ident',
        'resolv_system': 'no_resolv',
        'forward_private_reverse': 'no_private_reverse',
        'dhcp_disable_interfaces': ('dhcp', 'no_interface'),
        'dhcp_fqdn': ('dhcp', 'fqdn'),
        'dhcp_domain': ('dhcp', 'domain'),
        'dhcp_local': ('dhcp', 'local'),
        'dhcp_lease_max': ('dhcp', 'lease_max'),
        'dhcp_authoritative': ('dhcp', 'authoritative'),
        'dhcp_default_fw_rules': ('dhcp', 'default_fw_rules'),
        'dhcp_reply_delay': ('dhcp', 'reply_delay'),
        'dhcp_enable_ra': ('dhcp', 'enable_ra'),
        'dhcp_hasync': ('dhcp', 'nosync'),
    }
    FIELDS_BOOL_INVERT = ['resolve_etc_hosts', 'ident', 'forward_private_reverse', 'dhcp_hasync']
    FIELDS_TYPING = {
        'bool': [
            'enabled','regdhcp','regdhcpstatic','domain_needed', 'dnssec', 'resolve_etc_hosts', 'dhcpfirst',
            'strict_order', 'strictbind', 'forward_private_reverse', 'log_queries', 'ident', 'resolv_system',
            'add_subnet', 'add_subnet', 'dhcp_fqdn', 'dhcp_local', 'dhcp_authoritative', 'dhcp_default_fw_rules',
            'dhcp_enable_ra', 'dhcp_hasync',
        ],
        'int': ['port', 'dns_forward_max', 'cache_size', 'local_ttl', 'dhcp_lease_max', 'dhcp_reply_delay'],
        'list': ['interfaces', 'dhcp_disable_interfaces'],
        'str': ['regdhcpdomain'],
        'select': ['add_mac'],
    }
    SEARCH_ADDITIONAL = {
        'existing_interfaces': 'dnsmasq.interface',
    }
    INT_VALIDATIONS = {
        'port': {'min': 0, 'max': 65535},
        'dns_forward_max': {'min': 0},
        'cache_size': {'min': 0},
        'local_ttl': {'min': 0},
        'dhcp_lease_max': {'min': 0},
        'dhcp_reply_delay': {'min': 0, 'max': 60},
    }

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None):
        GeneralModule.__init__(self=self, m=module, r=result, s=session)
        self.existing_interfaces = {}

    def check(self) -> None:
        self._base_check()

        self.find_multiple_links(
            field='interfaces',
            existing_field_id='value',
            existing=self.existing_interfaces,
            fail_soft=False, fail=False,
        )
        self.find_multiple_links(
            field='dhcp_disable_interfaces',
            existing_field_id='value',
            existing=self.existing_interfaces,
            fail_soft=False, fail=False,
        )
