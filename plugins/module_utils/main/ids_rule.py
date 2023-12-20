from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.cls import BaseModule
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.main import \
    to_digit


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
    API_CMD_REL = 'reloadRules'
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
        self.exists = False

    def check(self) -> None:
        self._search_call()
        if not self.exists:
            self.m.fail_json(f"The provided rule '{self.p[self.FIELD_PK]}' was not found!")

        self.r['diff']['after'] = self.b.build_diff(data=self.p)
        self.r['changed'] = self.r['diff']['before'] != self.r['diff']['after']

    def process(self) -> None:
        if self.rule['action'] != self.p['action']:
            self.update()

        if self.rule['enabled'] != self.p['enabled']:
            self.toggle()

    def _search_call(self) -> list:
        # NOTE: workaround for issue with incomplete response-data from 'get' endpoint:
        #   https://github.com/opnsense/core/issues/7094
        existing = self.s.post(cnf={
            **self.call_cnf,
            'command': self.CMDS['search'],
            'data': {'current': 1, 'rowCount': self.QUERY_MAX_RULES, 'sort': self.FIELD_PK},
        })['rows']

        if self.FIELD_PK in self.p:  # list module
            for rule in existing:
                if rule[self.FIELD_PK] == self.p[self.FIELD_PK]:
                    self.exists = True
                    self.rule[self.FIELD_PK] = rule[self.FIELD_PK]
                    self.rule['enabled'] = rule['status'] == 'enabled'
                    self.rule['action'] = rule['action']
                    self.r['diff']['before'] = self.rule

        return existing

    def toggle(self) -> None:
        if not self.m.check_mode:
            self.s.post(cnf={
                **self.call_cnf, **{
                    'command': self.CMDS['toggle'],
                    'params': [self.p[self.FIELD_PK], to_digit(self.p['enabled'])],
                }
            })

    def update(self) -> None:
        if not self.m.check_mode:
            self.s.post(cnf={
                **self.call_cnf, **{
                    'command': self.CMDS['set'],
                    'params': [self.p[self.FIELD_PK]],
                    'data': {'action': self.p['action']}
                }
            })
