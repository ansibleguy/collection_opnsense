from ansible.module_utils.basic import AnsibleModule

from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.oxlorg.opnsense.plugins.module_utils.helper.validate import \
    is_ip_or_network, is_unset
from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.module import BaseModule


class Acl(BaseModule):
    FIELD_ID = 'name'
    CMDS = {
        'add': 'addAcl',
        'del': 'delAcl',
        'set': 'setAcl',
        'search': 'get',
        'toggle': 'toggleAcl',
    }
    API_KEY_PATH = 'acl.acls.acl'
    API_MOD = 'bind'
    API_CONT = 'acl'
    API_CONT_REL = 'service'
    FIELDS_CHANGE = ['networks']
    FIELDS_ALL = ['enabled', FIELD_ID]
    FIELDS_ALL.extend(FIELDS_CHANGE)
    FIELDS_TYPING = {
        'bool': ['enabled'],
        'list': ['networks'],
    }
    STR_VALIDATIONS = {
        'name': r'^(?!any$|localhost$|localnets$|none$)[0-9a-zA-Z_\-]{1,32}$'
    }
    EXIST_ATTR = 'acl'

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None, fail: dict = None):
        BaseModule.__init__(self=self, m=module, r=result, s=session, f=fail)
        self.acl = {}

    def check(self) -> None:
        if self.p['state'] == 'present':
            if is_unset(self.p['networks']):
                self.m.fail_json('You need to provide at networks to create an ACL!')

            for net in self.p['networks']:
                if not is_ip_or_network(net):
                    self.m.fail_json(
                        f"It seems you provided an invalid network: '{net}'"
                    )

        self._base_check()
