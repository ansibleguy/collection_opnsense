from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.main import \
    is_ip
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.unbound import \
    validate_domain
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.cls import BaseModule


class Domain(BaseModule):
    CMDS = {
        'add': 'addDomainOverride',
        'del': 'delDomainOverride',
        'set': 'setDomainOverride',
        'search': 'get',
        'toggle': 'toggleDomainOverride',
    }
    API_KEY_1 = 'unbound'
    API_KEY_2 = 'domains'
    API_KEY = 'domain'
    API_MOD = 'unbound'
    API_CONT = 'settings'
    API_CONT_REL = 'service'
    API_CMD_REL = 'reconfigure'
    FIELDS_CHANGE = ['domain', 'server', 'description']
    FIELDS_ALL = ['enabled']
    FIELDS_ALL.extend(FIELDS_CHANGE)
    FIELDS_TYPING = {
        'bool': ['enabled'],
    }
    EXIST_ATTR = 'domain'

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None):
        BaseModule.__init__(self=self, m=module, r=result, s=session)
        self.domain = {}
        self.call_cnf = {  # config shared by all calls
            'module': self.API_MOD,
            'controller': self.API_CONT,
        }

    def check(self):
        validate_domain(module=self.m, domain=self.p['domain'])
        if not is_ip(self.p['server']):
            self.m.fail_json(f"Server-value '{self.p['server']}' is not a valid IP-address!")

        self.b.find(match_fields=self.p['match_fields'])
        if self.exists:
            self.call_cnf['params'] = [self.domain['uuid']]

        if self.p['state'] == 'present':
            self.r['diff']['after'] = self.b.build_diff(data=self.p)
