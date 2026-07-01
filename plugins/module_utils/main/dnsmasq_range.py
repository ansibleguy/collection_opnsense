from ansible.module_utils.basic import AnsibleModule

from ansible_collections.oxlorg.opnsense.plugins.module_utils.helper.validate import \
    is_ip6
from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.module import BaseModule


class Range(BaseModule):
    FIELD_ID = 'description'
    CMDS = {
        'add': 'add_range',
        'del': 'del_range',
        'set': 'set_range',
        'search': 'get',
    }
    API_KEY_PATH = 'dnsmasq.dhcp_ranges'
    API_KEY_PATH_REQ = 'range'
    API_MOD = 'dnsmasq'
    API_CONT = 'settings'
    API_CONT_REL = 'service'
    FIELDS_CHANGE = [
        'interface', 'set_tag', 'start_addr', 'end_addr', 'subnet_mask', 'constructor', 'mode',
        'prefix_len', 'lease_time', 'domain_type', 'domain', 'sync', 'ra_mode', 'ra_priority',
        'ra_mtu', 'ra_interval', 'ra_router_lifetime'
    ]
    FIELDS_BOOL_INVERT = ['sync']
    FIELDS_TRANSLATE = {
        'sync': 'nosync',
    }
    FIELDS_TYPING = {
        'select': ['interface', 'set_tag', 'constructor', 'mode', 'domain_type', 'ra_priority'],
        'list': ['ra_mode'],
        'int': ['prefix_len', 'lease_time', 'ra_mtu', 'ra_interval', 'ra_router_lifetime'],
        'bool': ['sync'],
    }
    FIELDS_ALL = [FIELD_ID]
    FIELDS_ALL.extend(FIELDS_CHANGE)
    EXIST_ATTR = 'option'
    SEARCH_ADDITIONAL = {
        'existing_tag': 'dnsmasq.dhcp_tags',
        'existing_interface': 'dnsmasq.interface',
    }
    INT_VALIDATIONS = {
        'prefix_len': {'min': 1, 'max': 64},
    }

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None):
        BaseModule.__init__(self=self, m=module, r=result, s=session)
        self.option = {}
        self.existing_tag = {}
        self.existing_interface = {}

    def check(self) -> None:
        if self.p['state'] == 'present':
            if is_ip6(self.p['start_addr']):
                pass
            else:
                self.p['prefix_len'] = ''

        self._base_check()

        if self.p['state'] == 'present':
            self.find_single_link(
                field='interface',
                existing=self.existing_interface,
                existing_field_id='value',
            )
            self.find_single_link(
                field='constructor',
                existing=self.existing_interface,
                existing_field_id='value',
            )
            self.find_single_link(
                field='set_tag',
                existing=self.existing_tag,
                existing_field_id='tag',
            )
