from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.main import \
    validate_int_fields
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.cls import BaseModule


class Client(BaseModule):
    FIELD_ID = 'description'
    CMDS = {
        'add': 'addItem',
        'del': 'delItem',
        'set': 'setItem',
        'search': 'get',
        'toggle': 'toggleItem',
    }
    API_KEY_PATH = 'openvpn.Instances.Instance'
    API_MOD = 'openvpn'
    API_CONT = 'instances'
    API_CONT_REL = 'service'
    API_CMD_REL = 'reconfigure'
    FIELDS_CHANGE = []
    FIELDS_ALL = ['enabled', FIELD_ID]
    FIELDS_ALL.extend(FIELDS_CHANGE)
    FIELDS_TRANSLATE = {
        'protocol': 'proto',
        'address': 'local',
        'mode': 'dev_type',
        'log_level': 'verb',
        'certificate': 'cert',
        'ca': 'ca',
        'authentication': 'auth',
        'renegotiate_time': 'reneg-sec',
        'network_local': 'push_route',
        'network_remote': 'route',
        'options': 'various_flags',
        'mtu': 'tun_mtu',
        'fragment_size': 'fragment',
        'mss_fix': 'mssfix',
    }
    FIELDS_BOOL_INVERT = []
    FIELDS_TYPING = {
        'bool': ['enabled', 'mss_fix'],
        'list': ['network_local', 'network_remote', 'options'],
        'select': [
            'certificate', 'ca', 'tls_key', 'authentication', 'carp_depend_on', 'log_level',
            'mode', 'protocol',
        ],
        'int': ['fragment_size', 'mtu'],
    }
    INT_VALIDATIONS = {
        'mtu': {'min': 60, 'max': 65535},
        'fragment_size': {'min': 0, 'max': 65528},
    }
    EXIST_ATTR = 'instance'

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None):
        BaseModule.__init__(self=self, m=module, r=result, s=session)
        self.instance = {}

    def check(self) -> None:
        self.p['role'] = 'client'
        self.p['log_level'] = f"o{self.p['log_level']}"

        if self.p['state'] == 'present':
            validate_int_fields(module=self.m, data=self.p, field_minmax=self.INT_VALIDATIONS)

        self._base_check()
