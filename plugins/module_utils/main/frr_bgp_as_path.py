from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.main import \
    is_true, validate_int_fields, get_selected
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.base import Base


class AsPath:
    FIELD_ID = 'description'
    CMDS = {
        'add': 'addAspath',
        'del': 'delAspath',
        'set': 'setAspath',
        'search': 'get',
        'toggle': 'toggleAspath',
    }
    API_KEY = 'aspath'
    API_KEY_1 = 'bgp'
    API_KEY_2 = 'aspaths'
    API_MOD = 'quagga'
    API_CONT = 'bgp'
    API_CONT_REL = 'service'
    API_CMD_REL = 'reconfigure'
    FIELDS_CHANGE = ['number', 'action', 'as_pattern']
    FIELDS_ALL = [FIELD_ID, 'enabled']
    FIELDS_ALL.extend(FIELDS_CHANGE)
    FIELDS_TRANSLATE = {
        'as_pattern': 'as',
    }
    INT_VALIDATIONS = {
        'number': {'min': 10, 'max': 99},
    }
    EXIST_ATTR = 'as_path'

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None):
        self.m = module
        self.p = module.params
        self.r = result
        self.s = Session(module=module) if session is None else session
        self.exists = False
        self.as_path = {}
        self.call_cnf = {  # config shared by all calls
            'module': self.API_MOD,
            'controller': self.API_CONT,
        }
        self.b = Base(instance=self)
        self.existing_entries = None

    def check(self):
        if self.p['state'] == 'present':
            if self.p['number'] in ['', None] or self.p['as_pattern'] in ['', None] \
                    or self.p['action'] in ['', None]:
                self.m.fail_json(
                    'To create a BGP as-path you need to provide a number, '
                    'as_pattern and action!'
                )

            validate_int_fields(module=self.m, data=self.p, field_minmax=self.INT_VALIDATIONS)

        self.b.find(match_fields=[self.FIELD_ID])
        if self.exists:
            self.call_cnf['params'] = [self.as_path['uuid']]

        if self.p['state'] == 'present':
            self.r['diff']['after'] = self.b.build_diff(data=self.p)

    def process(self):
        self.b.process()

    @staticmethod
    def _simplify_existing(as_path: dict) -> dict:
        # makes processing easier
        return {
            'description': as_path['description'],
            'number': as_path['number'],
            'as_pattern': as_path['as'],
            'action': get_selected(as_path['action']),
            'enabled': is_true(as_path['enabled']),
            'uuid': as_path['uuid'],
        }

    def get_existing(self) -> list:
        return self.b.get_existing()

    def create(self):
        self.b.create()

    def update(self):
        self.b.update()

    def delete(self):
        self.b.delete()

    def reload(self):
        self.b.reload()
