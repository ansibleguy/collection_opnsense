from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.cls import BaseModule
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.main import is_unset


class Rule(BaseModule):
    FIELD_ID = 'description'
    CMDS = {
        'add': 'addPACRule',
        'set': 'setPACRule',
        'del': 'delPACRule',
        'search': 'get',
    }
    API_KEY_PATH = 'proxy.pac.rule'
    API_MOD = 'proxy'
    API_CONT = 'settings'
    API_CONT_REL = 'service'
    API_CMD_REL = 'reconfigure'
    FIELDS_CHANGE = ['matches', 'proxies', 'join_type', 'match_type']
    FIELDS_ALL = [FIELD_ID]
    FIELDS_ALL.extend(FIELDS_CHANGE)
    FIELDS_TYPING = {
        'list': ['matches', 'proxies'],
        'select': ['join_type', 'match_type'],
    }
    EXIST_ATTR = 'rule'
    SEARCH_ADDITIONAL = {
        'existing_matches': 'proxy.pac.match',
        'existing_proxies': 'proxy.pac.proxy',
    }

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None):
        BaseModule.__init__(self=self, m=module, r=result, s=session)
        self.rule = {}
        self.existing_matches = {}
        self.existing_proxies = {}

    def check(self) -> None:
        if self.p['state'] == 'present' and \
                (is_unset(self.p['proxies']) or is_unset(self.p['matches'])):
            self.m.fail_json(
                'You need to provide at least one proxy and match to create a rule!'
            )

        self.b.find(match_fields=[self.FIELD_ID])

        if self.p['state'] == 'present':
            self.b.find_multiple_links(
                field='matches',
                existing=self.existing_matches,
            )
            self.b.find_multiple_links(
                field='proxies',
                existing=self.existing_proxies,
            )

            self.r['diff']['after'] = self.b.build_diff(data=self.p)
