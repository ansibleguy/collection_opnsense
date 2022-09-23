from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.main import \
    is_ip, is_true
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.unbound import \
    validate_domain
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.base import Base


class Domain:
    CMDS = {
        'add': 'addDomainOverride',
        'del': 'delDomainOverride',
        'set': 'setDomainOverride',
        'search': 'get',
    }
    API_KEY_1 = 'unbound'
    API_KEY_2 = 'domains'
    API_KEY = 'domain'
    API_MOD = 'unbound'
    API_CONT = 'settings'
    API_CONT_REL = 'service'
    API_CMD_REL = 'reconfigure'
    FIELDS_CHANGE = ['domain', 'server', 'description', 'enabled']
    FIELDS_ALL = FIELDS_CHANGE
    FIELDS_TRANSLATE = {
        'target': 'server',
    }
    EXIST_ATTR = 'domain'

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None):
        self.m = module
        self.p = module.params
        self.r = result
        self.s = Session(module=module) if session is None else session
        self.exists = False
        self.domain = {}
        self.call_cnf = {  # config shared by all calls
            'module': self.API_MOD,
            'controller': self.API_CONT,
        }
        self.existing_entries = None
        self.b = Base(instance=self)

    def check(self):
        validate_domain(module=self.m, domain=self.p['domain'])
        if not is_ip(self.p['server']):
            self.m.fail_json(f"Server-value '{self.p['server']}' is not a valid IP-address!")

        self.b.find(match_fields=self.p['match_fields'])
        if self.exists:
            self.call_cnf['params'] = [self.domain['uuid']]

        if self.p['state'] == 'present':
            self.r['diff']['after'] = self.b.build_diff(data=self.p)

    @staticmethod
    def _simplify_existing(domain: dict) -> dict:
        # makes processing easier
        return {
            'enabled': is_true(domain['enabled']),
            'uuid': domain['uuid'],
            'domain': domain['domain'],
            'server': domain['server'],
            'description': domain['description'],
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
