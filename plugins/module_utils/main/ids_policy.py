from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.cls import BaseModule
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.main.ids_ruleset import Ruleset
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.main import \
    is_unset, is_true, ensure_list


class Policy(BaseModule):
    FIELD_ID = 'description'
    CMDS = {
        'add': 'addPolicy',
        'del': 'delPolicy',
        'set': 'setPolicy',
        'search': 'searchPolicy',
        'detail': 'getPolicy',
        'toggle': 'togglePolicy',
    }
    API_KEY = 'policy'
    API_KEY_PATH = f'policies.{API_KEY}'
    API_MOD = 'ids'
    API_CONT = 'settings'
    API_CONT_REL = 'service'
    API_CMD_REL = 'reconfigure'
    FIELDS_CHANGE = ['priority', 'action', 'rulesets', 'new_action']
    FIELDS_ALL = ['enabled', FIELD_ID]
    FIELDS_ALL.extend(FIELDS_CHANGE)
    FIELDS_TRANSLATE = {
        'priority': 'prio',
    }
    FIELDS_TRANSLATE_SPECIAL = {
        'rules': 'content',
    }
    FIELDS_TYPING = {
        'bool': ['enabled'],
        'select': ['new_action'],
        'list': ['rulesets', 'action'],
        'int': ['priority'],
    }
    FIELDS_IGNORE = ['content']
    EXIST_ATTR = 'policy'
    QUERY_MAX_RULES = 5000

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None):
        BaseModule.__init__(self=self, m=module, r=result, s=session)
        self.policy = {}
        self.exists = False
        self.enabled_rulesets = {}
        self.ruleset_names = {}

    def check(self) -> None:
        self._search_call()
        if self.p['state'] == 'present' and not is_unset(self.p['rulesets']):
            if len(self.enabled_rulesets) == 0:
                self._search_rulesets()

            if len(self.enabled_rulesets) == 0:
                self.m.fail_json("You need to enable rulesets before referencing them!")

            ruleset_uuids = []
            for ruleset in self.p['rulesets']:
                found = False
                for enabled_ruleset, uuid in self.enabled_rulesets.items():
                    if enabled_ruleset == ruleset:
                        found = True
                        ruleset_uuids.append(uuid)

                if not found:
                    self.m.fail_json(
                        f"The ruleset '{ruleset}' was not found! "
                        "You need to enable a ruleset before referencing it. "
                        f"Enabled ones are: {list(self.enabled_rulesets.keys())}"
                    )

            ruleset_uuids.sort()
            self.p['rulesets'] = ruleset_uuids

        self.r['diff']['after'] = self.b.build_diff(data=self.p)

    def get_existing(self) -> list:
        return self._search_call()

    def _search_call(self) -> list:
        # NOTE: workaround for issue with incomplete response-data from 'get' endpoint:
        #   https://github.com/opnsense/core/issues/7094
        existing = self.s.post(cnf={
            **self.call_cnf,
            'command': self.CMDS['search'],
            'data': {'current': 1, 'rowCount': self.QUERY_MAX_RULES, 'sort': self.FIELD_ID, 'searchPhrase': ''},
        })['rows']

        if self.FIELD_ID in self.p:  # list module
            for policy in existing:
                if policy[self.FIELD_ID] == self.p[self.FIELD_ID]:
                    self.exists = True
                    self.call_cnf['params'] = [policy['uuid']]
                    raw_policy = self.s.get(cnf={
                        **self.call_cnf,
                        'command': self.CMDS['detail'],
                    })[self.API_KEY]
                    self.policy['rules'] = self._parse_rules(raw_policy)
                    self.policy = self.b.simplify_existing(raw_policy)
                    self.enabled_rulesets = self._format_ruleset(raw_policy['rulesets'])
                    self.policy['uuid'] = policy['uuid']
                    if 'content' in self.policy:
                        self.policy.pop('content')

                    self.r['diff']['before'] = self.policy

        return existing

    @staticmethod
    def _parse_rules(raw_policy: dict) -> dict:
        parsed = {}

        if 'content' not in raw_policy:
            return parsed

        for key_value, values in raw_policy['content'].items():
            if is_true(values['selected']):
                key, value = key_value.split('.', 1)
                if key in parsed:
                    parsed[key].append(value)
                else:
                    parsed[key] = [value]

        return parsed

    def _build_request(self) -> dict:
        raw_request = self.b.build_request(ignore_fields=['rules'])

        # formatting dynamic rules
        # example: 'policy_content_affected_product: "affected_product.Adobe_Flash,affected_product.Adobe_Reader"'
        raw_request_rules = {}
        raw_request_content = []
        for key, values in self.p['rules'].items():
            fmt_values = [f'{key}.{value}' for value in ensure_list(values)]
            raw_request_rules[f'policy_content_{key}'] = self.b.RESP_JOIN_CHAR.join(fmt_values)
            raw_request_content.extend(fmt_values)

        raw_request[self.API_KEY]['content'] = self.b.RESP_JOIN_CHAR.join(raw_request_content)

        return {
            **raw_request,
            **raw_request_rules,
        }

    def _search_rulesets(self):
        # check if any ruleset is enabled before creating a new policy
        self.enabled_rulesets = self._format_ruleset(
                self.s.get(cnf={
                **self.call_cnf,
                'command': self.CMDS['detail'],
            })[self.API_KEY]['rulesets']
        )

    def _search_ruleset_names(self):
        ruleset_details = self.s.get(cnf={
            **self.call_cnf,
            'command': Ruleset.CMDS['search'],
        })['rows']

        for ruleset in ruleset_details:
            self.ruleset_names[ruleset[Ruleset.FIELD_PK]] = ruleset[Ruleset.FIELD_ID]

    def _format_ruleset(self, rulesets: dict) -> dict:
        if len(self.ruleset_names) == 0:
            self._search_ruleset_names()

        formatted = {}

        for uuid, ruleset in rulesets.items():
            formatted[self.ruleset_names[ruleset['value']]] = uuid

        return formatted
