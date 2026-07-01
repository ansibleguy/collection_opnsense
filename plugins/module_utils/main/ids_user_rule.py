from ansible.module_utils.basic import AnsibleModule

from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.module import BaseModule


class Rule(BaseModule):
    FIELD_ID = 'description'
    CMDS = {
        'add': 'add_user_rule',
        'set': 'set_user_rule',
        'del': 'del_user_rule',
        'search': 'search_user_rule',
        'detail': 'get_user_rule',
        'toggle': 'toggle_user_rule',
    }
    API_KEY = 'rule'
    API_KEY_PATH = f'userDefinedRules.{API_KEY}'
    API_MOD = 'ids'
    API_CONT = 'settings'
    API_CONT_REL = 'service'
    API_CMD_REL = 'reloadRules'
    FIELDS_CHANGE = ['source_ip', 'destination_ip', 'ssl_fingerprint', 'action', 'bypass']
    FIELDS_ALL = ['enabled', FIELD_ID]
    FIELDS_ALL.extend(FIELDS_CHANGE)
    FIELDS_TRANSLATE = {
        'source_ip': 'source',
        'destination_ip': 'destination',
        'ssl_fingerprint': 'fingerprint',
    }
    FIELDS_TYPING = {
        'bool': ['enabled', 'bypass'],
        'select': ['action'],
    }
    EXIST_ATTR = 'rule'
    QUERY_MAX_RULES = 5000

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None, fail: dict = None):
        BaseModule.__init__(self=self, m=module, r=result, s=session, f=fail)
        self.rule = {}
        self.exists = False

    def check(self):
        self.search_call()
        self.r['diff']['after'] = self.build_diff(data=self.p)

    def get_existing(self) -> list:
        return self.search_call()

    def search_call(self) -> list:
        existing = self.s.post(cnf={
            **self.call_cnf,
            'command': self.CMDS['search'],
            'data': {'current': 1, 'rowCount': self.QUERY_MAX_RULES, 'sort': self.FIELD_ID},
        })['rows']

        if self.FIELD_ID in self.p:  # list module
            for rule in existing:
                if rule[self.FIELD_ID] == self.p[self.FIELD_ID]:
                    self.exists = True
                    self.call_cnf['params'] = [rule['uuid']]
                    self.rule = self.simplify_existing(
                        self.s.get(cnf={
                            **self.call_cnf,
                            'command': self.CMDS['detail'],
                        })[self.API_KEY]
                    )
                    self.rule['uuid'] = rule['uuid']
                    self.r['diff']['before'] = self.rule

        return existing
