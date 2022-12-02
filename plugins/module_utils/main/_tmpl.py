from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.main import \
    is_true, validate_int_fields, simplify_translate
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.base import Base


class TMPL:
    FIELD_ID = 'name'
    CMDS = {
        'add': 'addItem',
        'del': 'delItem',
        'set': 'setItem',
        'search': 'get',
        'detail': 'getItem',
        'toggle': 'toggleItem',
    }
    API_KEY = 'stuff'
    API_KEY_1 = 'category'
    # API_KEY_2 = 'sub-category'
    API_MOD = 'API_Module'
    API_CONT = 'API_Controller'
    API_CONT_REL = 'API_Controller_reload'  # if other
    API_CMD_REL = 'reconfigure'
    FIELDS_CHANGE = []
    FIELDS_ALL = []
    FIELDS_ALL.extend(FIELDS_CHANGE)
    FIELDS_TRANSLATE = {
        'field1': 'apifield1',
    }
    FIELDS_BOOL_INVERT = []
    FIELDS_TYPING = {
        'bool': [],
        'list': [],
        'select': [],
    }
    INT_VALIDATIONS = {
        'field1': {'min': 1, 'max': 100},
    }
    EXIST_ATTR = 'stuff'

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None):
        self.m = module
        self.p = module.params
        self.r = result
        self.s = Session(module=module) if session is None else session
        self.exists = False
        self.stuff = {}
        self.call_cnf = {  # config shared by all calls
            'module': self.API_MOD,
            'controller': self.API_CONT,
        }
        self.existing_entries = None
        self.b = Base(instance=self)

    def check(self):
        # custom argument validation
        validate_int_fields(module=self.m, data=self.p, field_minmax=self.INT_VALIDATIONS)

        self.b.find(match_fields=[])  # todo: match_fields
        if self.exists:
            self.call_cnf['params'] = [self.stuff['uuid']]

        if self.p['state'] == 'present':
            self.r['diff']['after'] = self.b.build_diff(data=self.p)

        # basic validation of conditional parameters
        if not self.exists and self.p['state'] == 'present':
            if self.p['value'] is None or len(self.p['value']) == 0:
                self.m.fail_json('You need to provide values to create stuff!')

    def _error(self, msg: str):
        # for special handling of errors
        self.m.fail_json(msg)

    def detail_call(self) -> dict:
        # return base_detail(self)
        return self.s.get(cnf={
            **self.call_cnf, **{'command': self.CMDS['detail']}
        })['stuff']

    @staticmethod
    def _simplify_existing(stuff: dict) -> dict:
        # makes processing easier
        return {
            'enabled': is_true(stuff['enabled']),
            'description': stuff['description'],
            'uuid': stuff['uuid'],
            'param1': stuff['param1'],
            'param2': stuff['param2'],
        }

    def _simplify_existing(self, acl: dict) -> dict:
        # makes processing easier
        return simplify_translate(
            existing=acl,
            translate=self.FIELDS_TRANSLATE,
            typing=self.FIELDS_TYPING,
        )

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
