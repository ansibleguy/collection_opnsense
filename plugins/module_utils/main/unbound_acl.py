from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.main import \
    validate_str_fields, is_ip_or_network, is_unset
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.cls import BaseModule


class Acl(BaseModule):
    FIELD_ID = 'name'
    CMDS = {
        'add': 'addAcl',
        'del': 'delAcl',
        'set': 'setAcl',
        'search': 'get',
        'toggle': 'toggleAcl',
    }
    API_KEY_PATH = 'unbound.acls.acl'
    API_MOD = 'unbound'
    API_CONT = 'settings'
    API_CONT_REL = 'service'
    API_CMD_REL = 'reconfigure'
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

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None):
        BaseModule.__init__(self=self, m=module, r=result, s=session)
        self.acl = {}

    def check(self) -> None:
        validate_str_fields(module=self.m, data=self.p, field_regex=self.STR_VALIDATIONS, allow_empty=True)

        if self.p['state'] == 'present':
            if is_unset(self.p['networks']):
                self.m.fail_json('You need to provide a network(s) to create an ACL!')

            for net in self.p['networks']:
                if not is_ip_or_network(net):
                    self.m.fail_json(f"It seems you provided an invalid network: '{net}'")

        self._base_check()
