from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.main import \
    is_ip_or_network
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.cls import BaseModule


class Neighbor(BaseModule):
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
    FIELDS_CHANGE = ['description']
    FIELDS_ALL = [FIELD_ID, 'enabled']
    FIELDS_ALL.extend(FIELDS_CHANGE)
    EXIST_ATTR = 'neighbor'
    FIELDS_TRANSLATE = {
        'ip': 'address',
    }
    FIELDS_TYPING = {
        'bool': ['enabled'],
    }

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None):
        BaseModule.__init__(self=self, m=module, r=result, s=session)
        self.neighbor = {}
        self.call_cnf = {  # config shared by all calls
            'module': self.API_MOD,
            'controller': self.API_CONT,
        }

    def check(self):
        if not is_ip_or_network(self.p[self.FIELD_ID]):
            self.m.fail_json(f"Value '{self.p[self.FIELD_ID]}' is not a valid IP address!")

        self.b.find(match_fields=[self.FIELD_ID])
        if self.exists:
            self.call_cnf['params'] = [self.neighbor['uuid']]

        if self.p['state'] == 'present':
            self.r['diff']['after'] = self.b.build_diff(data=self.p)

    def _search_call(self) -> list:
        return self.s.get(cnf={
            **self.call_cnf, **{'command': self.CMDS['search']}
        })['rows']
