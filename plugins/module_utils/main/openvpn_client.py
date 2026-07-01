from ansible.module_utils.basic import AnsibleModule

from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.oxlorg.opnsense.plugins.module_utils.helper.translate import \
    get_key_by_value_from_selection, get_key_by_value_end_from_selection
from ansible_collections.oxlorg.opnsense.plugins.module_utils.helper.validate import \
    is_unset
from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.module import BaseModule


class Client(BaseModule):
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
    FIELDS_CHANGE = [
        'remote', 'protocol', 'port', 'address', 'mode', 'log_level', 'keepalive_interval', 'keepalive_timeout',
        'carp_depend_on', 'certificate', 'ca', 'key', 'authentication', 'username', 'password', 'renegotiate_time',
        'network_local', 'network_remote', 'options', 'mtu', 'fragment_size', 'mss_fix', 'verify_remote_certificate',
        'http_proxy',
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
        'verify_remote_certificate': 'remote_cert_tls',
        'http_proxy': 'http-proxy',
    }
    FIELDS_TYPING = {
        'bool': ['enabled', 'mss_fix', 'verify_remote_certificate'],
        'list': ['network_local', 'network_remote', 'options', 'remote'],
        'select': [
            'certificate', 'ca', 'key', 'authentication', 'carp_depend_on', 'log_level',
            'mode', 'protocol', 'role',
        ],
        'select_opt_list_idx': ['log_level'],
        'int': ['fragment_size', 'mtu'],
    }
    INT_VALIDATIONS = {
        'mtu': {'min': 60, 'max': 65535},
        'fragment_size': {'min': 0, 'max': 65528},
    }
    EXIST_ATTR = 'instance'
    FIELDS_DIFF_EXCLUDE = ['vpnid', 'role']

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None, fail: dict = None):
        BaseModule.__init__(self=self, m=module, r=result, s=session, f=fail)
        self.instance = {}

    def check(self) -> None:
        self.p['role'] = 'client'

        if self.p['state'] == 'present':
            if is_unset(self.p['remote']):
                self.m.fail_json(
                    "You need to provide a 'remote' target to create an openvpn-client!"
                )

            if is_unset(self.p['certificate']) and is_unset(self.p['ca']):
                self.m.fail_json(
                    "You need to either provide a 'certificate' or 'ca' to create an openvpn-client!"
                )

        self._base_check()

        if not is_unset(self.p['ca']):
            self.p['ca'] = get_key_by_value_from_selection(
                selection=self.raw['ca'],
                value=self.p['ca'],
            )

        if not is_unset(self.p['certificate']):
            self.p['certificate'] = get_key_by_value_from_selection(
                selection=self.raw[self.FIELDS_TRANSLATE['certificate']],
                value=self.p['certificate'],
            )

        if not is_unset(self.p['key']):
            self.p['key'] = get_key_by_value_end_from_selection(
                selection=self.raw[self.FIELDS_TRANSLATE['key']],
                value=self.p['key'],
            )

        if self.p['state'] == 'present':
            if 'before' in self.r['diff'] and 'mode' in self.r['diff']['before']:
                self.r['diff']['before']['mode'] = self.r['diff']['before']['mode'].lower()
                self.instance['mode'] = self.r['diff']['before']['mode']

            self.r['diff']['after'] = self.build_diff(data=self.p)
            self.r['changed'] = self.r['diff']['before'] != self.r['diff']['after']
