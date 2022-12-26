from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.handler import \
    ModuleSoftError
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.main import \
    validate_int_fields, is_unset
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.cls import BaseModule


class TMPL(BaseModule):
    FIELD_ID = 'name'
    CMDS = {
        'add': 'addItem',
        'del': 'delItem',
        'set': 'setItem',
        'search': 'get',
        'toggle': 'toggleItem',
    }
    API_KEY_PATH = 'category.sub_category.stuff'
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
            if is_unset(self.p['value']):
                self.m.fail_json('You need to provide values to create stuff!')

    def _error(self, msg: str):
        # for special handling of errors
        if self.fail:
            self.m.fail_json(msg)

        else:
            self.m.warn(msg)
            raise ModuleSoftError

    # @staticmethod
    # def _simplify_existing(stuff: dict) -> dict:
    #     return {
    #         'enabled': is_true(stuff['enabled']),
    #         'description': stuff['description'],
    #         'uuid': stuff['uuid'],
    #         'param1': stuff['param1'],
    #         'param2': stuff['param2'],
    #     }
