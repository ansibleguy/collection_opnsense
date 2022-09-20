from ipaddress import IPv6Address, IPv4Address, AddressValueError, NetmaskValueError
import validators

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.main import \
    is_ip, get_matching, validate_port, get_selected, get_selected_list, is_true
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.base import Base


class Syslog:
    CMDS = {
        'add': 'addDestination',
        'del': 'delDestination',
        'set': 'setDestination',
        'search': 'get',
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
        'port', 'description', 'enabled',
    ]
    FIELDS_ALL = ['rfc5424']
    FIELDS_ALL.extend(FIELDS_CHANGE)
    FIELDS_TRANSLATE = {
        'target': 'hostname',
    }
    EXIST_ATTR = 'dest'
    TIMEOUT = 40.0  # reload using unresolvable dns

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None):
        self.m = module
        self.p = module.params
        self.r = result
        self.s = Session(module=module, timeout=self.TIMEOUT) if session is None else session
        self.exists = False
        self.dest = {}
        self.call_cnf = {  # config shared by all calls
            'module': self.API_MOD,
            'controller': self.API_CONT,
        }
        self.existing_entries = None
        self.b = Base(instance=self)

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
            self.p['program'].sort()
            self.p['level'].sort()
            self.p['facility'].sort()

    @staticmethod
    def _simplify_existing(dest: dict) -> dict:
        # makes processing easier
        return {
            'enabled': is_true(dest['enabled']),
            'rfc5424': is_true(dest['rfc5424']),
            'target': dest['hostname'],
            'description': dest['description'],
            'port': int(dest['port']),
            'uuid': dest['uuid'],
            'certificate': get_selected(data=dest['certificate']),
            'transport': get_selected(data=dest['transport']),
            'program': get_selected_list(data=dest['program']),
            'level': get_selected_list(data=dest['level']),
            'facility': get_selected_list(data=dest['facility']),
        }

    def get_existing(self) -> list:
        return self.b.get_existing()

    def create(self):
        self.b.create()

    def update(self):
        self.b.update()

    def process(self):
        self.b.process()

    def delete(self):
        self.b.delete()

    def reload(self):
        self.b.reload()
