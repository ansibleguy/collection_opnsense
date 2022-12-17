from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.main import \
    validate_int_fields
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.cls import BaseModule


class Vlan(BaseModule):
    FIELD_ID = 'description'
    CMDS = {
        'add': 'addItem',
        'del': 'delItem',
        'set': 'setItem',
        'search': 'get',
    }
    API_KEY = 'vlan'
    API_KEY_1 = 'vlan'
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
        self.call_cnf = {  # config shared by all calls
            'module': self.API_MOD,
            'controller': self.API_CONT,
        }

    def check(self):
        if self.p['state'] == 'present':
            if self.p['interface'] is None:
                self.m.fail_json("You need to provide an 'interface' to create a vlan!")

            if self.p['vlan'] is None:
                self.m.fail_json("You need to provide a 'vlan' to create a vlan-interface!")

        validate_int_fields(module=self.m, data=self.p, field_minmax=self.INT_VALIDATIONS)

        self.b.find(match_fields=[self.FIELD_ID])
        if self.exists:
            self.call_cnf['params'] = [self.vlan['uuid']]

        if self.p['state'] == 'present':
            self.r['diff']['after'] = self.b.build_diff(data=self.p)

    def update(self):
        self.b.update(enable_switch=False)
