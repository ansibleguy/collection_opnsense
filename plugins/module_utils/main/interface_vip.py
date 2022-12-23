from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.main import \
    validate_int_fields
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.cls import BaseModule


class Vip(BaseModule):
    CMDS = {
        'add': 'addItem',
        'del': 'delItem',
        'set': 'setItem',
        'search': 'get',
    }
    API_KEY = 'vip'
    API_KEY_1 = 'vip'
    API_MOD = 'interfaces'
    API_CONT = 'vip_settings'
    API_CMD_REL = 'reconfigure'
    FIELDS_CHANGE = [
        'address', 'mode', 'cidr', 'expand', 'bind', 'gateway', 'password', 'vhid',
        'advertising_base', 'advertising_skew', 'description', 'interface',
    ]
    FIELDS_ALL = FIELDS_CHANGE
    FIELDS_ALL.extend(FIELDS_CHANGE)
    FIELDS_TRANSLATE = {
        'address': 'subnet',
        'cidr': 'subnet_bits',
        'expand': 'noexpand',
        'bind': 'nobind',
        'advertising_base': 'advbase',
        'advertising_skew': 'advskew',
        'description': 'descr',
    }
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

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None):
        BaseModule.__init__(self=self, m=module, r=result, s=session)
        self.vip = {}
        self.call_cnf = {
            'module': self.API_MOD,
            'controller': self.API_CONT,
        }

    def check(self):
        validate_int_fields(module=self.m, data=self.p, field_minmax=self.INT_VALIDATIONS)

        self.b.find(match_fields=self.p['match_fields'])
        if self.exists:
            self.call_cnf['params'] = [self.vip['uuid']]

        if self.p['state'] == 'present':
            self.r['diff']['after'] = self.b.build_diff(data=self.p)

    def update(self):
        self.b.update(enable_switch=False)
