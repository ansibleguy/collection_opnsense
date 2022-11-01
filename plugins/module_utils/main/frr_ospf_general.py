from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.main import \
    is_true, validate_int_fields, get_selected_list, get_selected
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.base import Base


class General:
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
    INT_VALIDATIONS = {
        'cost': {'min': 1, 'max': 4294967},
        'originate_metric': {'min': 0, 'max': 16777214},
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
            'carp': is_true(settings['carp_demote']),
            'id': settings['routerid'],
            'cost': settings['costreference'],
            'passive_ints': get_selected_list(settings['passiveinterfaces']),
            'redistribute': get_selected_list(settings['redistribute']),
            'redistribute_map': get_selected(settings['redistributemap']),
            'originate': is_true(settings['originate']),
            'originate_always': is_true(settings['originatealways']),
            'originate_metric': settings['originatemetric'],
        }

    def get_existing(self) -> dict:
        return self._search_call()

    def update(self):
        self.b.update()

    def reload(self):
        self.b.reload()
