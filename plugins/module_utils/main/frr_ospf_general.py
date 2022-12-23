from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.main import \
    validate_int_fields, simplify_translate
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.cls import BaseModule


class General(BaseModule):
    CMDS = {
        'set': 'set',
        'search': 'get',
    }
    API_KEY = 'ospf'
    API_MOD = 'quagga'
    API_CONT = 'ospfsettings'
    API_CONT_REL = 'service'
    API_CMD_REL = 'reconfigure'
    FIELDS_CHANGE = [
        'carp', 'id', 'cost', 'enabled', 'passive_ints', 'redistribute',
        'redistribute_map', 'originate', 'originate_always', 'originate_metric',
    ]
    FIELDS_ALL = FIELDS_CHANGE
    FIELDS_TRANSLATE = {
        'carp': 'carp_demote',
        'id': 'routerid',
        'cost': 'costreference',
        'originate_always': 'originatealways',
        'originate_metric': 'originatemetric',
        'passive_ints': 'passiveinterfaces',
        'redistribute_map': 'redistributemap',
    }
    FIELDS_TYPING = {
        'bool': ['enabled', 'carp', 'originate', 'originate_always'],
        'list': ['passive_ints', 'redistribute'],
        'select': ['redistribute_map'],
        'int': ['originate_metric', 'cost'],
    }
    FIELDS_IGNORE = ['prefixlists', 'routemaps', 'networks', 'interfaces']
    INT_VALIDATIONS = {
        'cost': {'min': 1, 'max': 4294967},
        'originate_metric': {'min': 0, 'max': 16777214},
    }
    EXIST_ATTR = 'settings'

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None):
        BaseModule.__init__(self=self, m=module, r=result, s=session)
        self.settings = {}
        self.call_cnf = {
            'module': self.API_MOD,
            'controller': self.API_CONT,
        }

    def check(self):
        validate_int_fields(module=self.m, data=self.p, field_minmax=self.INT_VALIDATIONS)

        self.settings = self._search_call()
        self.r['diff']['before'] = self.b.build_diff(self.settings)
        self.r['diff']['after'] = self.b.build_diff({
            k: v for k, v in self.p.items() if k in self.settings
        })

    def process(self):
        self.update()

    def _search_call(self) -> dict:
        return simplify_translate(
            existing=self.s.get(cnf={
                **self.call_cnf, **{'command': self.CMDS['search']}
            })[self.API_KEY],
            translate=self.FIELDS_TRANSLATE,
            typing=self.FIELDS_TYPING,
            ignore=self.FIELDS_IGNORE,
        )

    def get_existing(self) -> dict:
        return self._search_call()

    def update(self):
        self.b.update(enable_switch=False)
