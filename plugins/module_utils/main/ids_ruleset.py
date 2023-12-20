from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.cls import BaseModule
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.main import \
    is_true, to_digit


class Ruleset(BaseModule):
    FIELD_PK = 'filename'
    FIELD_ID = 'description'
    CMDS = {
        'set': 'setRuleset',
        'search': 'listRulesets',
        'toggle': 'toggleRuleset',
    }
    API_KEY_PATH = 'rulesets.ruleset'
    API_MOD = 'ids'
    API_CONT = 'settings'
    API_CONT_REL = 'service'
    API_CMD_REL = 'updateRules'
    FIELDS_CHANGE = ['enabled']
    FIELDS_COPY = [FIELD_PK, 'documentation_url']
    FIELDS_ALL = [FIELD_ID]
    FIELDS_ALL.extend(FIELDS_COPY)
    FIELDS_ALL.extend(FIELDS_CHANGE)
    FIELDS_TYPING = {
        'bool': ['enabled'],
    }
    EXIST_ATTR = 'ruleset'
    QUERY_MAX_RULES = 1000

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None):
        BaseModule.__init__(self=self, m=module, r=result, s=session)
        self.ruleset = {}
        self.exists = False
        self.existing_rulesets_desc = []

    def check(self) -> None:
        self._search_call()
        if not self.exists:
            self.m.fail_json(
                f"The provided ruleset '{self.p[self.FIELD_ID]}' was not found! "
                f"Available ones are: '{self.existing_rulesets_desc}'"
            )

        self.r['diff']['after'] = self.b.build_diff(data=self.p)
        self.r['changed'] = self.r['diff']['before'] != self.r['diff']['after']

    def process(self) -> None:
        if self.r['changed']:
            self.toggle()

    def _search_call(self) -> list:
        existing = self.s.post(cnf={
            **self.call_cnf,
            'command': self.CMDS['search'],
            'data': {'current': 1, 'rowCount': self.QUERY_MAX_RULES, 'sort': self.FIELD_PK, 'searchPhrase': ''},
        })['rows']

        if self.FIELD_ID in self.p:  # list module
            for ruleset in existing:
                self.existing_rulesets_desc.append(ruleset[self.FIELD_ID])

                if ruleset[self.FIELD_ID] == self.p[self.FIELD_ID]:
                    self.exists = True
                    for field in self.FIELDS_COPY:
                        self.ruleset[field] = ruleset[field]
                        self.p[field] = ruleset[field]

                    self.ruleset[self.FIELD_ID] = ruleset[self.FIELD_ID]
                    self.ruleset['enabled'] = is_true(ruleset['enabled'])
                    self.r['diff']['before'] = self.ruleset

        return existing

    def toggle(self) -> None:
        if not self.m.check_mode:
            self.s.post(cnf={
                **self.call_cnf, **{
                    'command': self.CMDS['toggle'],
                    'params': [self.p[self.FIELD_PK], to_digit(self.p['enabled'])],
                }
            })
