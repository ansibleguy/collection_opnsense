from ipaddress import IPv6Address, IPv4Address, AddressValueError, NetmaskValueError
import validators

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.main import \
    is_ip, validate_port
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.cls import BaseModule


class Syslog(BaseModule):
    CMDS = {
        'add': 'addDestination',
        'del': 'delDestination',
        'set': 'setDestination',
        'search': 'get',
        'toggle': 'toggleDestination',
    }
    API_KEY = 'destination'
    API_KEY_1 = 'syslog'
    API_KEY_2 = 'destinations'
    API_MOD = 'syslog'
    API_CONT = 'settings'
    API_CONT_REL = 'service'
    API_CMD_REL = 'reconfigure'
    FIELDS_CHANGE = [
        'target', 'transport', 'facility', 'program', 'level', 'certificate',
        'port', 'description',
    ]
    FIELDS_ALL = ['rfc5424', 'enabled']
    FIELDS_ALL.extend(FIELDS_CHANGE)
    FIELDS_TRANSLATE = {
        'target': 'hostname',
    }
    FIELDS_TYPING = {
        'bool': ['enabled', 'rfc5424'],
        'list': ['program', 'level', 'facility'],
        'select': ['certificate', 'transport'],
        'int': ['port'],
    }
    EXIST_ATTR = 'dest'
    TIMEOUT = 40.0  # reload using unresolvable dns

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None):
        BaseModule.__init__(self=self, m=module, r=result, s=session)
        self.s = Session(
            module=module,
            timeout=self.TIMEOUT,
        ) if session is None else session
        self.dest = {}
        self.call_cnf = {  # config shared by all calls
            'module': self.API_MOD,
            'controller': self.API_CONT,
        }

    def check(self):
        if not is_ip(self.p['target']) and \
                not validators.domain(self.p['target']):
            self.m.fail_json(
                f"Value of target '{self.p['target']}' is neither "
                f"a valid IP-Address nor a valid domain-name!"
            )

        if self.p['transport'].startswith('tls') and self.p['certificate'] == '':
            self.m.fail_json(
                "You need to provide a certificate to use encrypted transport!"
            )

        if is_ip(self.p['target']):
            if self.p['transport'].find('6') != -1:
                try:
                    IPv6Address(self.p['target'])

                except (AddressValueError, NetmaskValueError):
                    self.m.fail_json(
                        "Target does not match transport ip-protocol (IPv6)!"
                    )

            else:
                try:
                    IPv4Address(self.p['target'])

                except (AddressValueError, NetmaskValueError):
                    self.m.fail_json(
                        "Target does not match transport ip-protocol (IPv4)!"
                    )

        validate_port(module=self.m, port=self.p['port'])

        # checking if item exists
        self.b.find(match_fields=self.p['match_fields'])
        if self.exists:
            self.call_cnf['params'] = [self.dest['uuid']]

        if self.p['state'] == 'present':
            self.r['diff']['after'] = self.b.build_diff(self.p)
