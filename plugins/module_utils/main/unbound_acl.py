from ansible.module_utils.basic import AnsibleModule

from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.oxlorg.opnsense.plugins.module_utils.helper.validate import \
    is_ip_or_network, is_unset
from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.module import BaseModule


class Acl(BaseModule):
    FIELD_ID = 'name'
    CMDS = {
        'add': 'add_acl',
        'del': 'del_acl',
        'set': 'set_acl',
        'search': 'get',
        'toggle': 'toggle_acl',
    }
    API_KEY_PATH = 'unbound.acls.acl'
    API_MOD = 'unbound'
    API_CONT = 'settings'
    API_CONT_REL = 'service'
    FIELDS_CHANGE = ['action', 'networks', 'description']
    FIELDS_ALL = ['enabled', FIELD_ID]
    FIELDS_ALL.extend(FIELDS_CHANGE)
    FIELDS_TYPING = {
        'bool': ['enabled'],
        'select': ['action'],
        'list': ['networks'],
    }
    STR_VALIDATIONS = {
        'description': r'^.{0,255}$',
    }
    EXIST_ATTR = 'acl'

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None, fail: dict = None):
        BaseModule.__init__(self=self, m=module, r=result, s=session, f=fail)
        self.acl = {}

    def check(self) -> None:
        if self.p['state'] == 'present':
            if is_unset(self.p['networks']):
                self.m.fail_json('You need to provide a network(s) to create an ACL!')

            for net in self.p['networks']:
                if not is_ip_or_network(net):
                    self.m.fail_json(f"It seems you provided an invalid network: '{net}'")

        self._base_check()
