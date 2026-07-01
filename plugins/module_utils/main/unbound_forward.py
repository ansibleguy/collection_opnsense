from ansible.module_utils.basic import AnsibleModule

from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.oxlorg.opnsense.plugins.module_utils.helper.unbound import \
    validate_domain
from ansible_collections.oxlorg.opnsense.plugins.module_utils.helper.validate import \
    is_true, is_unset
from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.module import BaseModule


class Forward(BaseModule):
    CMDS = {
        'add': 'addForward',
        'del': 'delForward',
        'set': 'setForward',
        'search': 'get',
        'toggle': 'toggleForward',
    }
    API_KEY_PATH = 'unbound.dots.dot'
    API_MOD = 'unbound'
    API_CONT = 'settings'
    API_CONT_REL = 'service'
    FIELDS_CHANGE = ['domain', 'target', 'port', 'forward_tcp', 'description']
    FIELDS_ALL = ['type', 'enabled']
    FIELDS_ALL.extend(FIELDS_CHANGE)
    FIELDS_TRANSLATE = {
        'target': 'server',
        'forward_tcp': 'forward_tcp_upstream',
    }
    FIELDS_TYPING = {
        'bool': ['enabled', 'forward_tcp'],
        'int': ['port'],
    }
    STR_LEN_VALIDATIONS = {
        'description': {'min': 0, 'max': 255},
    }
    INT_VALIDATIONS = {
        'port': {'min': 1, 'max': 65535},
    }
    EXIST_ATTR = 'fwd'

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None, fail: dict = None):
        BaseModule.__init__(self=self, m=module, r=result, s=session, f=fail)
        self.fwd = {}

    def check(self) -> None:
        if not is_unset(self.p['domain']):
            validate_domain(module=self.m, domain=self.p['domain'])

        self.find(match_fields=['domain', 'target'])
        self._base_check()

    def search_call(self) -> list:
        fwds = []
        raw = self.search()

        if len(raw) > 0:
            for uuid, dot in raw.items():
                if is_true(dot['type']['forward']['selected']):
                    dot.pop('type')
                    dot['uuid'] = uuid
                    fwds.append(dot)

        return fwds
