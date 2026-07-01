from ipaddress import IPv6Address, IPv4Address, AddressValueError, NetmaskValueError

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.oxlorg.opnsense.plugins.module_utils.helper.validate import \
    is_ip, is_unset, is_valid_domain
from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.module import BaseModule


class Syslog(BaseModule):
    CMDS = {
        'add': 'add_destination',
        'del': 'del_destination',
        'set': 'set_destination',
        'search': 'get',
        'toggle': 'toggle_destination',
    }
    API_KEY_PATH = 'syslog.destinations.destination'
    API_MOD = 'syslog'
    API_CONT = 'settings'
    API_CONT_REL = 'service'
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
    INT_VALIDATIONS = {
        'port': {'min': 1, 'max': 65535},
    }

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None, fail: dict = None):
        BaseModule.__init__(self=self, m=module, r=result, s=session, f=fail)
        self.dest = {}

    def check(self) -> None:
        if not is_ip(self.p['target']) and \
                not is_valid_domain(self.p['target']):
            self.m.fail_json(
                f"Value of target '{self.p['target']}' is neither "
                f"a valid IP-Address nor a valid domain-name!"
            )

        if self.p['transport'].startswith('tls') and is_unset(self.p['certificate']):
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

        self._base_check()
