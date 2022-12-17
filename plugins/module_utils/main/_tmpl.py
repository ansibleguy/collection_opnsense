from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.handler import \
    ModuleSoftError
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.main import \
    validate_int_fields
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.cls import BaseModule


class TMPL(BaseModule):
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
    FIELDS_ALL = ['enabled']
    FIELDS_ALL.extend(FIELDS_CHANGE)
    FIELDS_TRANSLATE = {
        'field1': 'apifield1',
    }
    FIELDS_BOOL_INVERT = []
    FIELDS_TYPING = {
        'bool': ['enabled'],
        'list': [],
        'select': [],
        'int': [],
    }
    INT_VALIDATIONS = {
        'field1': {'min': 1, 'max': 100},
    }
    EXIST_ATTR = 'stuff'

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None):
        BaseModule.__init__(self=self, m=module, r=result, s=session)
        self.fail = False
        self.stuff = {}
        self.call_cnf = {  # config shared by all calls
            'module': self.API_MOD,
            'controller': self.API_CONT,
        }

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
        if self.fail:
            self.m.fail_json(msg)

        else:
            self.m.warn(msg)
            raise ModuleSoftError

    def detail_call(self) -> dict:
        # return base_detail(self)
        return self.s.get(cnf={
            **self.call_cnf, **{'command': self.CMDS['detail']}
        })['stuff']

    # @staticmethod
    # def _simplify_existing(stuff: dict) -> dict:
    #     return {
    #         'enabled': is_true(stuff['enabled']),
    #         'description': stuff['description'],
    #         'uuid': stuff['uuid'],
    #         'param1': stuff['param1'],
    #         'param2': stuff['param2'],
    #     }
