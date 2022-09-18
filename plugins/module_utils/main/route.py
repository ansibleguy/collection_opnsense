from ipaddress import ip_network

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.main import \
    is_true, to_digit
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.base import Base


class Route:
    FIELD_ID = 'uuid'
    CMDS = {
        'add': 'addroute',
        'del': 'delroute',
        'set': 'setroute',
        'search': 'searchroute',
    }
    API_KEY = 'route'
    API_MOD = 'routes'
    API_CONT = 'routes'
    API_CMD_REL = 'reconfigure'
    FIELDS_CHANGE = ['network', 'gateway', 'description', 'enabled']
    FIELDS_ALL = FIELDS_CHANGE
    EXIST_ATTR = 'route'

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None):
        self.m = module
        self.p = module.params
        self.r = result
        self.s = Session(module=module) if session is None else session
        self.exists = False
        self.route = {}
        self.call_cnf = {  # config shared by all calls
            'module': self.API_MOD,
            'controller': self.API_CONT,
        }
        self.existing_entries = None
        self.b = Base(instance=self)

    def check(self):
        try:
            ip_network(self.p['network'])

        except ValueError:
            self.m.fail_json(f"Value '{self.p['network']}' is not a valid network!")

        self.b.find(match_fields=self.p['match_fields'])

        if self.p['state'] == 'present':
            self.r['diff']['after'] = self.b.build_diff(data=self.p)

    def _search_call(self) -> list:
        return self.s.get(cnf={
            **self.call_cnf, **{'command': self.CMDS['search']}
        })['rows']

    @staticmethod
    def _simplify_existing(route: dict) -> dict:
        # makes processing easier
        return {
            'uuid': route['uuid'],
            'network': route['network'],
            'gateway': route['gateway'].rsplit('-', 1)[0].strip(),
            'description': route['descr'],
            'enabled': not is_true(route['disabled']),
        }

    def _build_request(self) -> dict:
        return {
            self.API_KEY: {
                'network': self.p['network'],
                'gateway': self.p['gateway'],
                'descr': self.p['description'],
                'disabled': to_digit(not self.p['enabled']),
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
