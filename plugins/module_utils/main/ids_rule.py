from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.cls import BaseModule


class Rule(BaseModule):
    FIELD_PK = 'sid'
    CMDS = {
        'set': 'setRule',
        'search': 'searchinstalledrules',
        'toggle': 'toggleRule',
    }
    API_KEY_PATH = 'rules.rule'
    API_MOD = 'ids'
    API_CONT = 'settings'
    API_CONT_REL = 'service'
    API_CMD_REL = 'reconfigure'
    FIELDS_CHANGE = ['action']
    FIELDS_ALL = ['enabled']
    FIELDS_ALL.extend(FIELDS_CHANGE)
    FIELDS_TYPING = {
        'bool': ['enabled'],
        'select': ['action'],
        'int': ['sid'],
    }
    EXIST_ATTR = 'rule'
    QUERY_MAX_RULES = 5000

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None):
        BaseModule.__init__(self=self, m=module, r=result, s=session)
        self.rule = {}

    def check(self) -> None:
        self._search_call()
        self.r['diff']['after'] = self.b.build_diff(data=self.p)
        self.r['changed'] = self.r['diff']['before'] != self.r['diff']['after']

    def process(self) -> None:
        if self.rule['action'] != self.p['action']:
            self.r['changed'] = True
            self.update()

        if self.rule['enabled'] != self.p['enabled']:
            self.r['changed'] = True
            self.toggle()

    def _search_call(self) -> list:
        existing = self.s.post(cnf={
            **self.call_cnf,
            'command': self.CMDS['search'],
            'data': {'current': 1, 'rowCount': self.QUERY_MAX_RULES, 'sort': 'sid'},
        })['rows']

        if 'sid' in self.p:
            for rule in existing:
                if rule['sid'] == self.p['sid']:
                    self.rule['sid'] = rule['sid']
                    self.rule['enabled'] = rule['status'] == 'enabled'
                    self.rule['action'] = rule['action']
                    self.r['diff']['before'] = self.rule

        return existing

    def toggle(self) -> None:
        if not self.m.check_mode:
            self.s.post(cnf={
                **self.call_cnf, **{
                    'command': self.CMDS['toggle'],
                    'params': [self.p['sid']],
                }
            })

    def update(self) -> None:
        if not self.m.check_mode:
            self.s.post(cnf={
                **self.call_cnf, **{
                    'command': self.CMDS['set'],
                    'params': [self.p['sid']],
                    'data': {'action': self.p['action']}
                }
            })
