from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.cls import BaseModule
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.main import \
    is_true


class Rule(BaseModule):
    FIELD_ID = 'sid'
    CMDS = {
        'add': 'addPolicyRule',
        'del': 'delPolicyRule',
        'set': 'setPolicyRule',
        'search': 'searchPolicyRule',
        'detail': 'getPolicyRule',
        'toggle': 'togglePolicyRule',
    }
    API_KEY_PATH = 'policies.rule'
    API_MOD = 'ids'
    API_CONT = 'settings'
    API_CONT_REL = 'service'
    API_CMD_REL = 'reconfigure'
    FIELDS_CHANGE = ['action']
    FIELDS_ALL = ['enabled', FIELD_ID]
    FIELDS_ALL.extend(FIELDS_CHANGE)
    FIELDS_TYPING = {
        'bool': ['enabled'],
        'select': ['action'],
        'int': ['sid'],
    }
    EXIST_ATTR = 'rule'
    QUERY_MAX_RULES = 1000

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None):
        BaseModule.__init__(self=self, m=module, r=result, s=session)
        self.rule = {}
        self.exists = False

    def check(self) -> None:
        self._search_call()
        self.r['diff']['after'] = self.b.build_diff(data=self.p)
        self.r['changed'] = self.r['diff']['before'] != self.r['diff']['after']

    def _search_call(self) -> list:
        existing = self.s.post(cnf={
            **self.call_cnf,
            'command': self.CMDS['search'],
            'data': {'current': 1, 'rowCount': self.QUERY_MAX_RULES, 'sort': self.FIELD_ID},
        })['rows']

        if self.FIELD_ID in self.p:  # list module
            for rule in existing:
                if int(rule[self.FIELD_ID]) == self.p[self.FIELD_ID]:
                    self.exists = True
                    self.rule['uuid'] = rule['uuid']
                    self.call_cnf['params'] = [self.rule['uuid']]
                    self.rule[self.FIELD_ID] = int(rule[self.FIELD_ID])
                    self.rule['enabled'] = is_true(rule['enabled'])
                    self.rule['action'] = rule['action'].lower()
                    self.r['diff']['before'] = self.rule

        return existing
