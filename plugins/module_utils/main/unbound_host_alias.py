from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.main import \
    is_true, to_digit
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.unbound import \
    validate_domain
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.base import Base


class Alias:
    CMDS = {
        'add': 'addHostAlias',
        'del': 'delHostAlias',
        'set': 'setHostAlias',
        'search': 'get',
        'toggle': 'toggleHostAlias',
    }
    API_KEY = 'alias'
    API_MOD = 'unbound'
    API_CONT = 'settings'
    API_CONT_REL = 'service'
    API_CMD_REL = 'reconfigure'
    FIELDS_CHANGE = ['target', 'domain', 'alias',  'description']
    FIELDS_ALL = ['enabled']
    FIELDS_ALL.extend(FIELDS_CHANGE)
    EXIST_ATTR = 'alias'

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None):
        self.m = module
        self.p = module.params
        self.r = result
        self.s = Session(module=module) if session is None else session
        self.exists = False
        self.alias = {}
        self.call_cnf = {  # config shared by all calls
            'module': self.API_MOD,
            'controller': self.API_CONT,
        }
        self.existing_entries = None
        self.existing_hosts = None
        self.target = None
        self.b = Base(instance=self)

    def check(self):
        if self.p['state'] == 'present':
            if self.p['target'] is None:
                self.m.fail_json(
                    "You need to provide a 'target' if you want to create a host-alias!"
                )

            validate_domain(module=self.m, domain=self.p['domain'])

        self.b.find(match_fields=self.p['match_fields'])

        if self.p['state'] == 'present':
            self._find_target()

            if self.target is None:
                self.m.fail_json(f"Alias-target '{self.p['target']}' was not found!")

            self.r['diff']['after'] = self.b.build_diff(data=self.p)

    def _find_target(self):
        if len(self.existing_hosts) > 0:
            for uuid, host in self.existing_hosts.items():
                if f"{host['hostname']}.{host['domain']}" == self.p['target']:
                    self.target = uuid
                    break

    def _search_call(self) -> dict:
        unbound = self.s.get(cnf={
            **self.call_cnf, **{'command': self.CMDS['search']}
        })['unbound']
        self.existing_hosts = unbound['hosts']['host']
        return unbound['aliases'][self.API_KEY]

    @staticmethod
    def _simplify_existing(alias: dict) -> dict:
        # makes processing easier
        simple = {
            'enabled': is_true(alias['enabled']),
            'domain': alias['domain'],
            'uuid': alias['uuid'],
            'alias': alias['hostname'],
            'description': alias['description'],
        }

        if len(alias['host']) > 0:
            simple['target'] = [v['value'] for v in alias['host'].values()][0]

        return simple

    def _build_request(self) -> dict:
        return {
            self.API_KEY: {
                'enabled': to_digit(self.p['enabled']),
                'hostname': self.p['alias'],
                'host': self.target,
                'domain': self.p['domain'],
                'description': self.p['description'],
            }
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
