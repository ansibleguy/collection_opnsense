from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.main import \
    validate_int_fields, get_selected, is_ip
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.base import Base


class Vxlan:
    FIELD_ID = 'id'
    CMDS = {
        'add': 'addItem',
        'del': 'delItem',
        'set': 'setItem',
        'search': 'get',
    }
    API_KEY = 'vxlan'
    API_KEY_1 = 'vxlan'
    API_MOD = 'interfaces'
    API_CONT = 'vxlan_settings'
    API_CMD_REL = 'reconfigure'
    FIELDS_CHANGE = ['interface', 'local', 'remote', 'group']
    FIELDS_ALL = [FIELD_ID]
    FIELDS_ALL.extend(FIELDS_CHANGE)
    FIELDS_TRANSLATE = {
        # 'name': 'deviceId',  # can't be configured
        'id': 'vxlanid',
        'local': 'vxlanlocal',
        'remote': 'vxlanremote',
        'group': 'vxlangroup',
        'interface': 'vxlandev',
    }
    INT_VALIDATIONS = {
        'id': {'min': 0, 'max': 16777215},
    }
    FIELDS_IP = ['local', 'remote', 'group']
    EXIST_ATTR = 'vxlan'

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None):
        self.m = module
        self.p = module.params
        self.r = result
        self.s = Session(module=module) if session is None else session
        self.exists = False
        self.vxlan = {}
        self.call_cnf = {  # config shared by all calls
            'module': self.API_MOD,
            'controller': self.API_CONT,
        }
        self.existing_entries = None
        self.b = Base(instance=self)

    def check(self):
        if self.p['state'] == 'present':
            if self.p['local'] is None:
                self.m.fail_json("You need to provide a 'local' ip to create a vxlan!")

            for field in self.FIELDS_IP:
                if self.p[field] is not None and not is_ip(self.p[field]):
                    self.m.fail_json(
                        f"Value '{self.p[field]}' is not a valid IP-address!"
                    )

        validate_int_fields(module=self.m, data=self.p, field_minmax=self.INT_VALIDATIONS)

        self.b.find(match_fields=[self.FIELD_ID])
        if self.exists:
            self.call_cnf['params'] = [self.vxlan['uuid']]

        if self.p['state'] == 'present':
            self.r['diff']['after'] = self.b.build_diff(data=self.p)

    @staticmethod
    def _simplify_existing(vxlan: dict) -> dict:
        # makes processing easier
        return {
            'uuid': vxlan['uuid'],
            'id': int(vxlan['vxlanid']),
            'interface': get_selected(vxlan['vxlandev']),
            'local': vxlan['vxlanlocal'],
            'remote': vxlan['vxlanremote'],
            'group': vxlan['vxlangroup'],
        }

    def process(self):
        self.b.process()

    def _search_call(self) -> list:
        return self.b.search()

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

    def reload(self):
        self.b.reload()
