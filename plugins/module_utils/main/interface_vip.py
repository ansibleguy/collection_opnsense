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
        'address', 'mode', 'expand', 'bind', 'gateway', 'password', 'vhid',
        'advertising_base', 'advertising_skew', 'description', 'interface',
        'peer', 'peer6',
    ]
    FIELDS_ALL = FIELDS_CHANGE
    FIELDS_TRANSLATE = {
        'address': 'network',
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
        'select': ['mode', 'interface', 'vhid', 'advertising_base', 'advertising_skew'],
        'int': ['vhid', 'advertising_base', 'advertising_skew'],
    }
    INT_VALIDATIONS = {
        'vhid': {'min': 1, 'max': 255},
        'advertising_base': {'min': 1, 'max': 254},
        'advertising_skew': {'min': 0, 'max': 254},
    }
    EXIST_ATTR = 'vip'

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None, fail: dict = None):
        BaseModule.__init__(self=self, m=module, r=result, s=session, f=fail)
        self.vip = {}

    def check(self) -> None:
        if self.p['address'].find('/') == -1:
            self.m.fail_json('The address needs to include a subnet CIDR!')

        self.existing_entries = self.get_existing()
        self._base_check()

    def update(self) -> None:
        self._base_update(enable_switch=False)

    # NOTE: workaround for OPNsense handling 'get' differently than 'add' and 'set'
    #   https://github.com/opnsense/core/issues/7041
    def get_existing(self) -> list:
        existing = []

        for entry in self._base_get_existing():
            entry['address'] = f"{entry['subnet']}/{entry['subnet_bits']}"
            entry.pop('subnet')
            entry.pop('subnet_bits')
            existing.append(entry)
            for field in self.FIELDS_BOOL_INVERT:
                entry[field] = not entry[field]

        return existing
