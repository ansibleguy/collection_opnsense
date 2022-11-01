from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.main import \
    is_true, validate_int_fields, get_selected
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.base import Base


class Interface:
    CMDS = {
        'add': 'addInterface',
        'del': 'delInterface',
        'set': 'setInterface',
        'search': 'get',
        'toggle': 'toggleInterface',
    }
    API_KEY = 'interface'
    API_KEY_1 = 'ospf'
    API_KEY_2 = 'interfaces'
    API_MOD = 'quagga'
    API_CONT = 'ospfsettings'
    API_CONT_REL = 'service'
    API_CMD_REL = 'reconfigure'
    FIELDS_CHANGE = [
        'interface', 'area', 'auth_type', 'auth_key', 'auth_key_id', 'cost',
        'hello_interval', 'dead_interval', 'retransmit_interval', 'transmit_delay',
        'priority', 'network_type', 'enabled', 'carp_depend_on', 'cost_demoted',
    ]
    FIELDS_ALL = FIELDS_CHANGE
    INT_VALIDATIONS = {
        'cost': {'min': 1, 'max': 65535},
        'hello_interval': {'min': 0, 'max': 4294967295},
        'dead_interval': {'min': 0, 'max': 4294967295},
        'retransmit_interval': {'min': 0, 'max': 4294967295},
        'transmit_delay': {'min': 0, 'max': 4294967295},
        'priority': {'min': 0, 'max': 4294967295},
        'cost_demoted': {'min': 1, 'max': 65535},
        'auth_key_id': {'min': 1, 'max': 255},
    }
    FIELDS_TRANSLATE = {
        'interface': 'interfacename',
        'hello_interval': 'hellointerval',
        'dead_interval': 'deadinterval',
        'retransmit_interval': 'retransmitinterval',
        'transmit_delay': 'transmitdelay',
        'network_type': 'networktype',
        'auth_type': 'authtype',
        'auth_key': 'authkey',
        'auth_key_id': 'authkey_id',
    }
    EXIST_ATTR = 'int'

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None):
        self.m = module
        self.p = module.params
        self.r = result
        self.s = Session(module=module) if session is None else session
        self.exists = False
        self.int = {}
        self.call_cnf = {  # config shared by all calls
            'module': self.API_MOD,
            'controller': self.API_CONT,
        }
        self.existing_entries = None
        self.b = Base(instance=self)

    def check(self):
        if self.p['state'] == 'present':
            if self.p['area'] in ['', None]:
                self.m.fail_json(
                    'To create a OSPF interface you need to provide its area!'
                )

            if self.p['auth_type'] not in ['', None] and self.p['auth_key'] in ['', None]:
                self.m.fail_json(
                    'You need to provide an authentication-key if you enable authentication!'
                )

            validate_int_fields(module=self.m, data=self.p, field_minmax=self.INT_VALIDATIONS)

        self.b.find(match_fields=self.p['match_fields'])
        if self.exists:
            self.call_cnf['params'] = [self.int['uuid']]

        if self.p['state'] == 'present':
            self.r['diff']['after'] = self.b.build_diff(data=self.p)

    @staticmethod
    def _simplify_existing(interface: dict) -> dict:
        # makes processing easier
        return {
            'enabled': is_true(interface['enabled']),
            'interface': get_selected(interface['interfacename']),
            'carp_depend_on': get_selected(interface['carp_depend_on']),
            'network_type': get_selected(interface['networktype']),
            'uuid': interface['uuid'],
            'hello_interval': interface['hellointerval'],
            'dead_interval': interface['deadinterval'],
            'retransmit_interval': interface['retransmitinterval'],
            'transmit_delay': interface['transmitdelay'],
            'area': interface['area'],
            'cost': interface['cost'],
            'cost_demoted': interface['cost_demoted'],
            'priority': interface['priority'],
            'auth_type': get_selected(interface['authtype']),
            'auth_key': interface['authkey'],
            'auth_key_id': interface['authkey_id'],
        }

    def process(self):
        self.b.process()

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
