from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.main import \
    is_true, validate_int_fields, get_selected_list
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.base import Base


class Rip:
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
    INT_VALIDATIONS = {
        'version': {'min': 1, 'max': 2},
        'metric': {'min': 1, 'max': 16},
    }
    EXIST_ATTR = 'settings'

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None):
        self.m = module
        self.p = module.params
        self.r = result
        self.s = Session(module=module) if session is None else session
        self.exists = False
        self.settings = {}
        self.call_cnf = {  # config shared by all calls
            'module': self.API_MOD,
            'controller': self.API_CONT,
        }
        self.b = Base(instance=self)

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
        settings = self.s.get(cnf={
            **self.call_cnf, **{'command': self.CMDS['search']}
        })[self.API_KEY]

        return {
            'enabled': is_true(settings['enabled']),
            'version': int(settings['version']),
            'metric': settings['defaultmetric'],
            'passive_ints': get_selected_list(settings['passiveinterfaces']),
            'networks': get_selected_list(settings['networks']),
            'redistribute': get_selected_list(settings['redistribute']),
        }

    def get_existing(self) -> dict:
        return self._search_call()

    def update(self):
        self.b.update(enable_switch=False)

    def reload(self):
        self.b.reload()
