from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.cls import BaseModule


class Rule(BaseModule):
    FIELD_ID = 'description'
    CMDS = {
        'add': 'addUserRule',
        'set': 'setUserRule',
        'del': 'delUserRule',
        'search': 'searchUserRule',
        'detail': 'getUserRule',
        'toggle': 'toggleUserRule',
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

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None):
        BaseModule.__init__(self=self, m=module, r=result, s=session)
        self.rule = {}
        self.exists = False

    def check(self):
        self._search_call()
        self.r['diff']['after'] = self.b.build_diff(data=self.p)

    def get_existing(self) -> list:
        return self._search_call()

    def _search_call(self) -> list:
        # NOTE: workaround for issue with incomplete response-data from 'get' endpoint:
        #   https://github.com/opnsense/core/issues/7094
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
                    # pylint: disable=W0212
                    self.rule = self.b._simplify_existing(
                        self.s.get(cnf={
                            **self.call_cnf,
                            'command': self.CMDS['detail'],
                        })[self.API_KEY]
                    )
                    self.rule['uuid'] = rule['uuid']
                    self.r['diff']['before'] = self.rule

        return existing
