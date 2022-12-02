from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.main import \
    simplify_translate
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.base import Base


class Blocklist:
    CMDS = {
        'set': 'set',
        'search': 'get',
    }
    API_KEY = 'dnsbl'
    API_MOD = 'bind'
    API_CONT = 'dnsbl'
    API_CONT_REL = 'service'
    API_CMD_REL = 'reconfigure'
    FIELDS_CHANGE = [
        'safe_google', 'safe_duckduckgo', 'safe_youtube', 'safe_bing', 'enabled',
        'exclude', 'block'
    ]
    FIELDS_ALL = FIELDS_CHANGE
    FIELDS_TRANSLATE = {
        'block': 'type',
        'exclude': 'whitelists',
        'safe_google': 'forcesafegoogle',
        'safe_duckduckgo': 'forcesafeduckduckgo',
        'safe_youtube': 'forcesafeyoutube',
        'safe_bing': 'forcestrictbing',
    }
    FIELDS_BOOL_INVERT = ['ipv6', 'prefetch']
    FIELDS_TYPING = {
        'bool': [
            'safe_google', 'safe_duckduckgo', 'safe_youtube', 'safe_bing', 'enabled',
        ],
        'list': ['exclude', 'block'],
    }
    EXIST_ATTR = 'settings'

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None):
        self.m = module
        self.p = module.params
        self.r = result
        self.s = Session(module=module) if session is None else session
        self.exists = False
        self.settings = {}
        self.call_cnf = {  # config shared by all calls
            'module': self.API_MOD,
            'controller': self.API_CONT,
        }
        self.existing_entries = None
        self.b = Base(instance=self)

    def check(self):
        self.settings = self._search_call()
        self.r['diff']['before'] = self.settings
        self.r['diff']['after'] = {
            k: v for k, v in self.p.items() if k in self.settings
        }

    def _search_call(self) -> dict:
        return simplify_translate(
            existing=self.s.get(cnf={
                **self.call_cnf, **{'command': self.CMDS['search']}
            })[self.API_KEY],
            translate=self.FIELDS_TRANSLATE,
            typing=self.FIELDS_TYPING,
            bool_invert=self.FIELDS_BOOL_INVERT,
        )

    def process(self):
        self.update()

    def get_existing(self) -> dict:
        return self._search_call()

    def update(self):
        self.b.update()

    def reload(self):
        self.b.reload()
