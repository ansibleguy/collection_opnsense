from ipaddress import ip_network

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.module import BaseModule


class Vip(BaseModule):
    CMDS = {
        'add': 'add_item',
        'del': 'del_item',
        'set': 'set_item',
        'search': 'get',
    }
    API_KEY_PATH = 'vip.vip'
    API_MOD = 'interfaces'
    API_CONT = 'vip_settings'
    FIELDS_CHANGE = [
        'address', 'mode', 'bind', 'gateway', 'password', 'vhid',
        'advertising_base', 'advertising_skew', 'description', 'interface',
        'peer', 'peer6',
    ]
    FIELDS_ALL = ['expand']
    FIELDS_ALL.extend(FIELDS_CHANGE)
    FIELDS_TRANSLATE = {
        'address': ['network', 'address'],
        # 'network': 'subnet',
        # 'network_cidr': 'subnet_bits',
        'expand': 'noexpand',
        'bind': 'nobind',
        'advertising_base': 'advbase',
        'advertising_skew': 'advskew',
        'description': 'descr',
    }
    FIELDS_DIFF_NO_LOG = ['password']
    FIELDS_BOOL_INVERT = ['expand', 'bind']
    FIELDS_TYPING = {
        'bool': ['expand', 'bind'],
        'select': [
            'mode', 'interface', 'vhid', 'advertising_base', 'advertising_skew',
        ],
        'int': ['vhid', 'advertising_base', 'advertising_skew'],  # 'network_cidr'
    }
    FIELDS_OPTIONAL = []
    INT_VALIDATIONS = {
        'vhid': {'min': 1, 'max': 255},
        'advertising_base': {'min': 1, 'max': 254},
        'advertising_skew': {'min': 0, 'max': 254},
        # 'network_cidr': {'min': 0, 'max': 128},
    }
    EXIST_ATTR = 'vip'

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None, fail: dict = None):
        BaseModule.__init__(self=self, m=module, r=result, s=session, f=fail)
        self.vip = {}

    def check(self) -> None:
        if self.p['address'].find('/') == -1:
            self.m.fail_json('The address needs to include a subnet CIDR!')

        try:
            ip_network(self.p['address'], strict=False)
            # self.p['network'] = str(net.network_address)
            # self.p['network_cidr'] = int(net.prefixlen)

        except ValueError as e:
            self.m.fail_json(f'The address needs to be a valid IP+CIDR combination! {e}')

        self.FIELDS_OPTIONAL.append('network')
        self.existing_entries = self.get_existing()
        self._base_check()
        self.FIELDS_OPTIONAL = []

    def update(self) -> None:
        self._base_update(enable_switch=False)

    # NOTE: workaround for OPNsense handling 'get' differently than 'add' and 'set'
    #   https://github.com/opnsense/core/issues/7041
    def get_existing(self) -> list:
        existing = []
        self.FIELDS_OPTIONAL.append('network')

        for entry in self._base_get_existing():
            entry['address'] = entry['address']
            entry.pop('subnet')
            entry.pop('subnet_bits')
            existing.append(entry)

        return existing
