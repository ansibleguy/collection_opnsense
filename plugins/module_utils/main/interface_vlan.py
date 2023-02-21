from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.main import \
    validate_int_fields, is_unset
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.cls import BaseModule


class Vlan(BaseModule):
    FIELD_ID = 'description'
    CMDS = {
        'add': 'addItem',
        'del': 'delItem',
        'set': 'setItem',
        'search': 'get',
    }
    API_KEY_PATH = 'vlan.vlan'
    API_MOD = 'interfaces'
    API_CONT = 'vlan_settings'
    API_CMD_REL = 'reconfigure'
    FIELDS_CHANGE = ['interface', 'vlan', 'priority']
    FIELDS_ALL = [FIELD_ID]
    FIELDS_ALL.extend(FIELDS_CHANGE)
    FIELDS_TRANSLATE = {
        # 'name': 'vlanif',  # can't be configured
        'interface': 'if',
        'vlan': 'tag',
        'priority': 'pcp',
        'description': 'descr',
    }
    FIELDS_TYPING = {
        'select': ['interface', 'priority'],
        'int': ['vlan', 'priority'],
    }
    INT_VALIDATIONS = {
        'vlan': {'min': 1, 'max': 4096},
        'priority': {'min': 0, 'max': 7},
    }
    EXIST_ATTR = 'vlan'

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None):
        BaseModule.__init__(self=self, m=module, r=result, s=session)
        self.vlan = {}

    def check(self) -> None:
        if self.p['state'] == 'present':
            if is_unset(self.p['interface']):
                self.m.fail_json("You need to provide an 'interface' to create a vlan!")

            if is_unset(self.p['vlan']):
                self.m.fail_json("You need to provide a 'vlan' to create a vlan-interface!")

            validate_int_fields(module=self.m, data=self.p, field_minmax=self.INT_VALIDATIONS)

        self._base_check()

    def update(self) -> None:
        self.b.update(enable_switch=False)
