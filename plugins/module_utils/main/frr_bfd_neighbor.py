from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.main import \
    is_true, is_ip_or_network
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.base import Base


class Neighbor:
    FIELD_ID = 'ip'
    CMDS = {
        'add': 'addNeighbor',
        'del': 'delNeighbor',
        'set': 'setNeighbor',
        'search': 'searchNeighbor',
        'toggle': 'toggleNeighbor',
    }
    API_KEY = 'neighbor'
    API_KEY_1 = 'neighbors'
    API_MOD = 'quagga'
    API_CONT = 'bfd'
    FIELDS_CHANGE = ['description', 'enabled']
    FIELDS_ALL = [FIELD_ID]
    FIELDS_ALL.extend(FIELDS_CHANGE)
    EXIST_ATTR = 'neighbor'
    FIELDS_TRANSLATE = {
        'ip': 'address',
    }

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None):
        self.m = module
        self.p = module.params
        self.r = result
        self.s = Session(module=module) if session is None else session
        self.exists = False
        self.neighbor = {}
        self.call_cnf = {  # config shared by all calls
            'module': self.API_MOD,
            'controller': self.API_CONT,
        }
        self.existing_entries = None
        self.b = Base(instance=self)

    def check(self):
        if not is_ip_or_network(self.p[self.FIELD_ID]):
            self.m.fail_json(f"Value '{self.p[self.FIELD_ID]}' is not a valid IP address!")

        self.b.find(match_fields=[self.FIELD_ID])
        if self.exists:
            self.call_cnf['params'] = [self.neighbor['uuid']]

        if self.p['state'] == 'present':
            self.r['diff']['after'] = self.b.build_diff(data=self.p)

    @staticmethod
    def _simplify_existing(neighbor: dict) -> dict:
        # makes processing easier
        return {
            'enabled': is_true(neighbor['enabled']),
            'description': neighbor['description'],
            'uuid': neighbor['uuid'],
            'ip': neighbor['address'],
        }

    def process(self):
        self.b.process()

    def _search_call(self) -> list:
        return self.s.get(cnf={
            **self.call_cnf, **{'command': self.CMDS['search']}
        })['rows']

    def get_existing(self) -> list:
        return self.b.get_existing()

    def create(self):
        self.b.create()

    def update(self):
        self.b.update()

    def delete(self):
        self.b.delete()

    def enable(self):
        self.b.enable()

    def disable(self):
        self.b.disable()
