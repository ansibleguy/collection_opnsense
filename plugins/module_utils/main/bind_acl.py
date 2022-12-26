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
    API_KEY_PATH = 'acl.acls.acl'
    API_MOD = 'bind'
    API_CONT = 'acl'
    API_CONT_REL = 'service'
    API_CMD_REL = 'reconfigure'
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

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None):
        BaseModule.__init__(self=self, m=module, r=result, s=session)
        self.acl = {}

    def check(self):
        validate_str_fields(
            module=self.m, data=self.p,
            field_regex=self.STR_VALIDATIONS,
        )

        if self.p['state'] == 'present':
            if is_unset(self.p['networks']):
                self.m.fail_json('You need to provide at networks to create an ACL!')

            for net in self.p['networks']:
                if not is_ip_or_network(net):
                    self.m.fail_json(
                        f"It seems you provided an invalid network: '{net}'"
                    )

        self.b.find(match_fields=[self.FIELD_ID])
        if self.exists:
            self.call_cnf['params'] = [self.acl['uuid']]

        if self.p['state'] == 'present':
            self.r['diff']['after'] = self.b.build_diff(data=self.p)
