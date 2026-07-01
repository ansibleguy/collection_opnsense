from ansible.module_utils.basic import AnsibleModule

from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.oxlorg.opnsense.plugins.module_utils.helper.validate import \
    is_valid_mac_address, is_ip
from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.module import BaseModule


class Neighbor(BaseModule):
    FIELD_ID = 'description'
    CMDS = {
        'add': 'add_item',
        'del': 'del_item',
        'set': 'set_item',
        'search': 'get',
        'toggle': 'toggleItem',
    }
    API_KEY_PATH = 'neighbor.neighbor'
    API_MOD = 'interfaces'
    API_CONT = 'neighbor_settings'
    FIELDS_CHANGE = ['ethernet_address', 'ip_address']
    FIELDS_ALL = [FIELD_ID]
    FIELDS_ALL.extend(FIELDS_CHANGE)
    FIELDS_TRANSLATE = {
        'description': 'descr',
        'ethernet_address': 'etheraddr',
        'ip_address': 'ipaddress',
    }
    FIELDS_TYPING = {
    }
    EXIST_ATTR = 'neighbor'

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None):
        BaseModule.__init__(self=self, m=module, r=result, s=session)
        self.neighbor = {}

    def check(self) -> None:
        if self.p['state'] == 'present':
            if not is_valid_mac_address(self.p['ethernet_address']):
                self.m.fail_json(
                    "You need to provide an valid 'ethernet_address' to create a neigbor!"
                )
            if not is_ip(self.p['ip_address']):
                self.m.fail_json(
                    "You need to provide an valid 'ip_address' to create a neigbor!"
                )

        self._base_check()
