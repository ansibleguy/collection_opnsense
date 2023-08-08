from ansible.module_utils.basic import AnsibleModule, boolean

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.main import \
    validate_port, validate_str_fields, is_unset, is_ip6, is_ip_or_network
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.unbound import \
    validate_domain
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.cls import GeneralModule


# Supported as of OPNsense 23.7
class General(GeneralModule):
    CMDS = {
        'set': 'set',
        'search': 'get',
    }
    API_KEY_PATH = 'unbound.general'
    API_KEY_PATH_REQ = API_KEY_PATH
    API_MOD = 'unbound'
    API_CONT = 'settings'
    API_CONT_REL = 'service'
    API_CMD_REL = 'reconfigureGeneral'
    FIELDS_CHANGE = [
        'enabled', 'port', 'interfaces', 'dnssec', 'dns64', 'dns64_prefix',
        'aaaa_only_mode', 'register_dhcp_leases', 'dhcp_domain',
        'register_dhcp_static_mappings', 'register_ipv6_link_local',
        'register_system_records', 'txt', 'flush_dns_cache', 'local_zone_type',
        'outgoing_interfaces', 'wpad',
    ]
    FIELDS_ALL = FIELDS_CHANGE
    FIELDS_TRANSLATE = {
        'interfaces': 'active_interface',
        'dns64_prefix': 'dns64prefix',
        'aaaa_only_mode': 'noarecords',
        'register_dhcp_leases': 'regdhcp',
        'dhcp_domain': 'regdhcpdomain',
        'register_dhcp_static_mappings': 'regdhcpstatic',
        'register_ipv6_link_local': 'noreglladdr6',
        'register_system_records': 'noregrecords',
        'txt': 'txtsupport',
        'flush_dns_cache': 'cacheflush',
        'local_zone_type': 'local_zone_type',
        'outgoing_interfaces': 'outgoing_interface',
        'wpad': 'enable_wpad',
    }
    FIELDS_BOOL_INVERT = ['register_ipv6_link_local', 'register_system_records']
    FIELDS_TYPING = {
        'bool': [
            'enabled', 'dnssec', 'dns64', 'aaaa_only_mode', 'register_dhcp_leases',
            'register_dhcp_static_mappings', 'register_ipv6_link_local',
            'register_system_records', 'txt', 'flush_dns_cache', 'wpad',
        ],
        'list': [
            'interfaces', 'outgoing_interfaces',
        ],
        'select': ['local_zone_type'],
        'int': ['port'],
    }
    STR_VALIDATIONS = {
        'dns64_prefix': r'^(?:[0-9a-f]{1,4}:)+:/[0-9]{1,3}$',
    }
    SEARCH_ADDITIONAL = {
        'existing_active_interfaces': 'unbound.general.active_interface',
        'existing_outgoing_interfaces': 'unbound.general.outgoing_interface',
    }

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None):
        GeneralModule.__init__(self=self, m=module, r=result, s=session)
        self.existing_active_interfaces = []
        self.existing_outgoing_interfaces = []
        self.invalid_interface = None

    def check(self) -> None:
        # pylint: disable=W0201
        if not is_unset(self.p['port']):
            validate_port(module=self.m, port=self.p['port'])
        if not is_unset(self.p['dhcp_domain']):
            validate_domain(module=self.m, domain=self.p['dhcp_domain'])

        validate_str_fields(module=self.m, data=self.p, field_regex=self.STR_VALIDATIONS,)

        self.settings = self._search_call()

        if not is_unset(self.p['interfaces']):
            if not self._find_active_interfaces(self.existing_active_interfaces, self.p['interfaces']):
                self.m.fail_json(f"Interface '{self.invalid_interface}' was not found!")
        if not is_unset(self.p['outgoing_interfaces']):
            if not self._find_active_interfaces(self.existing_outgoing_interfaces, self.p['outgoing_interfaces']):
                self.m.fail_json(f"Outgoing interface '{self.invalid_interface}' was not found!")

        self._build_diff()

    def _find_active_interfaces(self, existing_interfaces, interfaces) -> bool:
        if len(existing_interfaces) > 0:
            for interface in interfaces:
                if interface not in existing_interfaces:
                    self.invalid_interface = interface
                    return False
        return True
