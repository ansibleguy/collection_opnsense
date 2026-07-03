from ipaddress import ip_address

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.oxlorg.opnsense.plugins.module_utils.helper.validate import \
    is_ip4, is_ip6
from ansible_collections.oxlorg.opnsense.plugins.module_utils.helper.main import is_unset
from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.module import BaseModule


class Gw(BaseModule):
    FIELD_ID = 'name'
    CMDS = {
        'add': 'add_gateway',
        'del': 'del_gateway',
        'set': 'set_gateway',
        'search': 'search_gateway',
        'detail': 'get_gateway',
        'toggle': 'toggle_gateway',
    }
    API_KEY_PATH = 'gateway_item'
    API_MOD = 'routing'
    API_CONT = 'settings'
    FIELDS_CHANGE = [
        'name', 'interface', 'gateway', 'default_gw', 'far_gw', 'monitor_disable', 'monitor_noroute', 'monitor',
        'force_down', 'priority', 'weight', 'latency_low', 'latency_high', 'loss_low', 'loss_high', 'interval',
        'time_period', 'loss_interval', 'data_length', 'description', 'ip_protocol',
    ]
    FIELDS_ALL = ['enabled']
    FIELDS_ALL.extend(FIELDS_CHANGE)
    FIELDS_BOOL_INVERT = ['enabled']
    FIELDS_TRANSLATE = {
        'description': 'descr',
        'ip_protocol': 'ipprotocol',
        'enabled': 'disabled',
        'default_gw': 'defaultgw',
        'far_gw': 'fargw',
        'latency_low': 'latencylow',
        'latency_high': 'latencyhigh',
        'loss_low': 'losslow',
        'loss_high': 'losshigh',
    }
    FIELDS_TYPING = {
        'bool': ['enabled', 'default_gw', 'far_gw', 'monitor_disable', 'monitor_noroute', 'force_down'],
        'int': [
            'priority', 'weight', 'latency_low', 'latency_high', 'loss_low', 'loss_high', 'interval', 'time_period',
            'loss_interval', 'data_length',
        ],
        'select': ['interface', 'ip_protocol'],
    }
    FIELDS_OPTIONAL = ['far_gw']
    INT_VALIDATIONS = {
        'priority': {'min': 0, 'max': 255},
        'weight': {'min': 1, 'max': 5},
        'latency_low': {'min': 1, 'max': 9999},
        'latency_high': {'min': 1, 'max': 9999},
        'loss_low': {'min': 1, 'max': 99},
        'loss_high': {'min': 1, 'max': 99},
        'interval': {'min': 1, 'max': 9999},
        'time_period': {'min': 1, 'max': 9999},
        'data_length': {'min': 0, 'max': 9999},
    }
    EXIST_ATTR = 'gw'

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None, fail: dict = None):
        BaseModule.__init__(self=self, m=module, r=result, s=session, f=fail)
        self.gw = {}

    def check(self) -> None:
        if self.p['state'] == 'present':
            if not is_unset(self.p['gateway']):
                try:
                    ip_address(self.p['gateway'])

                except ValueError:
                    self.m.fail_json(f"Value '{self.p['gateway']}' is not a valid gateway!")

                if self.p['ip_protocol'] == 'inet' and not is_ip4(self.p['gateway']):
                    self.m.fail_json(f"Gateway '{self.p['gateway']}' is not a valid IPv4-address!")
                elif self.p['ip_protocol'] == 'inet6' and not is_ip6(self.p['gateway']):
                    self.m.fail_json(f"Gateway '{self.p['gateway']}' is not a valid IPv6-address!")

            if self.p['monitor']:
                try:
                    ip_address(self.p['monitor'])

                except ValueError:
                    self.m.fail_json(f"Value '{self.p['monitor']}' is not a valid monitor address!")

            if not self.p['interface']:
                self.m.fail_json('You need to provide a value for the interface!')

        self._base_check()
