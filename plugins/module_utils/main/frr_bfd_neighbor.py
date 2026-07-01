from ansible.module_utils.basic import AnsibleModule

from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.oxlorg.opnsense.plugins.module_utils.helper.validate import \
    is_ip_or_network
from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.module import BaseModule


class Neighbor(BaseModule):
    FIELD_ID = 'ip'
    CMDS = {
        'add': 'addNeighbor',
        'del': 'delNeighbor',
        'set': 'setNeighbor',
        'search': 'get',
        'toggle': 'toggleNeighbor',
    }
    API_KEY_PATH = 'bfd.neighbors.neighbor'
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

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None, fail: dict = None):
        BaseModule.__init__(self=self, m=module, r=result, s=session, f=fail)
        self.neighbor = {}

    def check(self) -> None:
        if not is_ip_or_network(self.p[self.FIELD_ID]):
            self.m.fail_json(f"Value '{self.p[self.FIELD_ID]}' is not a valid IP address!")

        self._base_check()
