from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.main import \
    validate_int_fields, simplify_translate
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.cls import BaseModule


class Rip(BaseModule):
    CMDS = {
        'set': 'set',
        'search': 'get',
    }
    API_KEY = 'rip'
    API_MOD = 'quagga'
    API_CONT = 'rip'
    API_CONT_REL = 'service'
    API_CMD_REL = 'reconfigure'
    FIELDS_CHANGE = [
        'version', 'metric', 'passive_ints', 'enabled', 'networks',
        'redistribute',
    ]
    FIELDS_ALL = FIELDS_CHANGE
    FIELDS_TRANSLATE = {
        'passive_ints': 'passiveinterfaces',
        'metric': 'defaultmetric',
    }
    FIELDS_TYPING = {
        'bool': ['enabled'],
        'list': ['passive_ints', 'networks', 'redistribute'],
        'int': ['version'],
    }
    INT_VALIDATIONS = {
        'version': {'min': 1, 'max': 2},
        'metric': {'min': 1, 'max': 16},
    }
    EXIST_ATTR = 'settings'

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None):
        BaseModule.__init__(self=self, m=module, r=result, s=session)
        self.settings = {}
        self.call_cnf = {  # config shared by all calls
            'module': self.API_MOD,
            'controller': self.API_CONT,
        }

    def check(self):
        validate_int_fields(module=self.m, data=self.p, field_minmax=self.INT_VALIDATIONS)

        self.settings = self._search_call()
        self.r['diff']['before'] = self.settings
        self.r['diff']['after'] = {
            k: v for k, v in self.p.items() if k in self.settings
        }

    def process(self):
        self.update()

    def _search_call(self) -> dict:
        return simplify_translate(
            existing=self.s.get(cnf={
                **self.call_cnf, **{'command': self.CMDS['search']}
            })[self.API_KEY],
            translate=self.FIELDS_TRANSLATE,
            typing=self.FIELDS_TYPING,
            # ignore=self.FIELDS_IGNORE,
        )

    def get_existing(self) -> dict:
        return self._search_call()

    def update(self):
        self.b.update(enable_switch=False)
