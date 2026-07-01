from ansible.module_utils.basic import AnsibleModule

from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.oxlorg.opnsense.plugins.module_utils.helper.validate import \
    is_ip, is_unset
from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.module import BaseModule


class Vxlan(BaseModule):
    FIELD_ID = 'id'
    CMDS = {
        'add': 'add_item',
        'del': 'del_item',
        'set': 'set_item',
        'search': 'get',
    }
    API_KEY_PATH = 'vxlan.vxlan'
    API_MOD = 'interfaces'
    API_CONT = 'vxlan_settings'
    FIELDS_CHANGE = ['interface', 'local', 'local_port', 'remote', 'remote_port', 'group']
    FIELDS_ALL = [FIELD_ID]
    FIELDS_ALL.extend(FIELDS_CHANGE)
    FIELDS_TRANSLATE = {
        # 'name': 'deviceId',  # can't be configured
        'id': 'vxlanid',
        'local': 'vxlanlocal',
        'local_port': 'vxlanlocalport',
        'remote': 'vxlanremote',
        'remote_port': 'vxlanremoteport',
        'group': 'vxlangroup',
        'interface': 'vxlandev',
    }
    FIELDS_TYPING = {
        'select': ['interface'],
        'int': ['id', 'local_port', 'remote_port'],
    }
    INT_VALIDATIONS = {
        'id': {'min': 0, 'max': 16777215},
        'local_port': {'min': 1, 'max': 65535},
        'remote_port': {'min': 1, 'max': 65535},
    }
    FIELDS_IP = ['local', 'remote', 'group']
    EXIST_ATTR = 'vxlan'

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None, fail: dict = None):
        BaseModule.__init__(self=self, m=module, r=result, s=session, f=fail)
        self.vxlan = {}

    def check(self) -> None:
        if self.p['state'] == 'present':
            if is_unset(self.p['local']):
                self.m.fail_json("You need to provide a 'local' ip to create a vxlan!")

            for field in self.FIELDS_IP:
                if not is_unset(self.p[field]) and not is_ip(self.p[field]):
                    self.m.fail_json(
                        f"Value '{self.p[field]}' is not a valid IP-address!"
                    )

        self._base_check()

    def update(self) -> None:
        self._base_update(enable_switch=False)
