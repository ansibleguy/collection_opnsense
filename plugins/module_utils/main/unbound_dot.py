from ansible.module_utils.basic import AnsibleModule

from ansible_collections.oxlorg.opnsense.plugins.module_utils.helper.validate import \
    is_ip, valid_hostname, is_true, is_unset
from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.oxlorg.opnsense.plugins.module_utils.helper.unbound import \
    validate_domain
from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.module import BaseModule


class DnsOverTls(BaseModule):
    CMDS = {
        'add': 'addDot',
        'del': 'delDot',
        'set': 'setDot',
        'search': 'get',
        'toggle': 'toggleDot',
    }
    API_KEY_PATH = 'unbound.dots.dot'
    API_MOD = 'unbound'
    API_CONT = 'settings'
    API_CONT_REL = 'service'
    FIELDS_CHANGE = ['domain', 'target', 'port', 'verify']
    FIELDS_ALL = ['type', 'enabled']
    FIELDS_ALL.extend(FIELDS_CHANGE)
    FIELDS_TRANSLATE = {
        'target': 'server',
    }
    FIELDS_TYPING = {
        'bool': ['enabled'],
        'int': ['port'],
    }
    EXIST_ATTR = 'dot'
    INT_VALIDATIONS = {
        'port': {'min': 1, 'max': 65535},
    }

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None, fail: dict = None):
        BaseModule.__init__(self=self, m=module, r=result, s=session, f=fail)
        self.dot = {}

    def check(self) -> None:
        if not is_unset(self.p['domain']):
            validate_domain(module=self.m, domain=self.p['domain'])

        if not is_unset(self.p['verify']) and \
                not is_ip(self.p['verify']) and \
                not valid_hostname(self.p['verify']):
            self.m.fail_json(
                f"Verify-value '{self.p['verify']}' is neither a valid IP-Address "
                f"nor a valid hostname!"
            )

        if is_unset(self.p['domain']):
            self.find(match_fields=['target'])

        else:
            self.find(match_fields=['domain', 'target'])

        self._base_check()

    def search_call(self) -> list:
        dots = []
        raw = self.search()

        if len(raw) > 0:
            for uuid, dot in raw.items():
                if is_true(dot['type']['dot']['selected']):
                    dot.pop('type')
                    dot['uuid'] = uuid
                    dots.append(dot)

        return dots
