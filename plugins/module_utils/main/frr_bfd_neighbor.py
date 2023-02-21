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
    API_KEY_PATH = 'neighbors.neighbor'
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

    def check(self) -> None:
        if not is_ip_or_network(self.p[self.FIELD_ID]):
            self.m.fail_json(f"Value '{self.p[self.FIELD_ID]}' is not a valid IP address!")

        self._base_check()

    def _search_call(self) -> list:
        return self.s.get(cnf={
            **self.call_cnf, **{'command': self.CMDS['search']}
        })['rows']
