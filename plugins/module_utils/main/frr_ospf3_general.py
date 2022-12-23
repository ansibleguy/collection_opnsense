from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.main import \
    is_true, get_selected_list, simplify_translate
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
    FIELDS_TYPING = {
        'bool': ['enabled', 'carp'],
        'list': ['redistribute'],
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
        self.settings = self._search_call()
        self.r['diff']['before'] = self.b.build_diff(self.settings)
        self.r['diff']['after'] = self.b.build_diff({
            k: v for k, v in self.p.items() if k in self.settings
        })

    def _search_call(self) -> dict:
        return simplify_translate(
            existing=self.s.get(cnf={
                **self.call_cnf, **{'command': self.CMDS['search']}
            })[self.API_KEY],
            translate=self.FIELDS_TRANSLATE,
            typing=self.FIELDS_TYPING,
        )

    def get_existing(self) -> dict:
        return self._search_call()

    def update(self):
        self.b.update(enable_switch=False)
