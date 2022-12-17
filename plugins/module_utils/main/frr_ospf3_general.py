from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.main import \
    is_true, get_selected_list
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.cls import BaseModule


class General(BaseModule):
    CMDS = {
        'set': 'set',
        'search': 'get',
    }
    API_KEY = 'ospf6'
    API_MOD = 'quagga'
    API_CONT = 'ospf6settings'
    API_CONT_REL = 'service'
    API_CMD_REL = 'reconfigure'
    FIELDS_CHANGE = [
        'carp', 'id', 'enabled', 'redistribute',
    ]
    FIELDS_ALL = FIELDS_CHANGE
    FIELDS_TRANSLATE = {
        'carp': 'carp_demote',
        'id': 'routerid',
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
        self.settings = self._search_call()
        self.r['diff']['before'] = self.settings
        self.r['diff']['after'] = {
            k: v for k, v in self.p.items() if k in self.settings
        }

    def _search_call(self) -> dict:
        settings = self.s.get(cnf={
            **self.call_cnf, **{'command': self.CMDS['search']}
        })[self.API_KEY]

        return {
            'enabled': is_true(settings['enabled']),
            'carp': is_true(settings['carp_demote']),
            'id': settings['routerid'],
            'redistribute': get_selected_list(settings['redistribute']),
        }

    def update(self):
        self.b.update(enable_switch=False)
