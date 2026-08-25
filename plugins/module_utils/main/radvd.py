from typing import Callable

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.module import BaseModule
from ansible_collections.oxlorg.opnsense.plugins.module_utils.helper.main import \
    is_unset
from ansible_collections.oxlorg.opnsense.plugins.module_utils.helper.validate import \
    is_ip6, is_ip6_network, is_valid_domain


class Radvd(BaseModule):
    FIELD_ID = 'interface'
    CMDS = {
        'add': 'add_entry',
        'del': 'del_entry',
        'set': 'set_entry',
        'search': 'search_entry',
        'detail': 'get_entry',
        'toggle': 'toggle_entry',
    }
    API_KEY_PATH = 'entries'
    API_MOD = 'radvd'
    API_CONT = 'settings'
    API_CONT_REL = 'service'
    API_CMD_REL = 'reconfigure'
    FIELDS_CHANGE = [
        'base6_interface', 'mode', 'deprecate_prefix', 'remove_adv_on_exit',
        'remove_route', 'routes', 'rdnss', 'dnssl', 'dns', 'min_rtr_adv_interval',
        'max_rtr_adv_interval', 'adv_dnssl_lifetime', 'adv_default_lifetime',
        'adv_link_mtu', 'adv_preferred_lifetime', 'adv_ra_src_address',
        'adv_rdnss_lifetime', 'adv_route_lifetime', 'adv_valid_lifetime',
        'adv_default_preference', 'nat64prefix',
    ]
    FIELDS_ALL = [FIELD_ID, 'enabled']
    FIELDS_ALL.extend(FIELDS_CHANGE)
    FIELDS_TRANSLATE = {
        'base6_interface': 'Base6Interface',
        'deprecate_prefix': 'DeprecatePrefix',
        'remove_adv_on_exit': 'RemoveAdvOnExit',
        'remove_route': 'RemoveRoute',
        'rdnss': 'RDNSS',
        'dnssl': 'DNSSL',
        'min_rtr_adv_interval': 'MinRtrAdvInterval',
        'max_rtr_adv_interval': 'MaxRtrAdvInterval',
        'adv_dnssl_lifetime': 'AdvDNSSLLifetime',
        'adv_default_lifetime': 'AdvDefaultLifetime',
        'adv_link_mtu': 'AdvLinkMTU',
        'adv_preferred_lifetime': 'AdvPreferredLifetime',
        'adv_ra_src_address': 'AdvRASrcAddress',
        'adv_rdnss_lifetime': 'AdvRDNSSLifetime',
        'adv_route_lifetime': 'AdvRouteLifetime',
        'adv_valid_lifetime': 'AdvValidLifetime',
        'adv_default_preference': 'AdvDefaultPreference',
    }
    FIELDS_TYPING = {
        'bool': ['enabled', 'dns'],
        'int': [
            'min_rtr_adv_interval', 'max_rtr_adv_interval', 'adv_dnssl_lifetime',
            'adv_default_lifetime', 'adv_link_mtu', 'adv_preferred_lifetime',
            'adv_rdnss_lifetime', 'adv_route_lifetime', 'adv_valid_lifetime',
        ],
        'list': ['routes', 'rdnss', 'dnssl'],
        'select': [
            'interface', 'base6_interface', 'mode', 'deprecate_prefix',
            'remove_adv_on_exit', 'remove_route', 'adv_ra_src_address',
            'adv_default_preference',
        ],
    }
    INT_VALIDATIONS = {
        'min_rtr_adv_interval': {'min': 3},
        'max_rtr_adv_interval': {'min': 4, 'max': 1800},
        'adv_dnssl_lifetime': {'min': 1, 'max': 4294967295},
        'adv_link_mtu': {'min': 1280, 'max': 65535},
        'adv_preferred_lifetime': {'min': 1, 'max': 4294967295},
        'adv_rdnss_lifetime': {'min': 1, 'max': 4294967295},
        'adv_route_lifetime': {'min': 1, 'max': 4294967295},
        'adv_valid_lifetime': {'min': 1, 'max': 4294967295},
    }
    EXIST_ATTR = 'entry'

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None, fail: dict = None):
        BaseModule.__init__(self=self, m=module, r=result, s=session, f=fail)
        self.entry = {}

    def check(self) -> None:
        if self.p['state'] == 'present':
            if is_unset(self.p['interface']):
                self.m.fail_json("You need to provide an 'interface' to create a radvd entry!")

            self._validate_list('routes', is_ip6_network, 'valid IPv6 network')
            self._validate_list('rdnss', is_ip6, 'valid IPv6 address')
            self._validate_list('dnssl', is_valid_domain, 'valid DNS domain')

            if not is_unset(self.p['nat64prefix']) and not is_ip6_network(self.p['nat64prefix']):
                self.m.fail_json(
                    f"The nat64prefix value '{self.p['nat64prefix']}' is not a valid IPv6 network!"
                )

        self._base_check()

    def _validate_list(self, field: str, validator: Callable, description: str) -> None:
        for value in self.p[field]:
            if not validator(value):
                self.m.fail_json(
                    f"The {field} value '{value}' is not a {description}!"
                )
