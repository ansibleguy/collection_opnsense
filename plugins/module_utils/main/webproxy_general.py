from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.main import \
    validate_int_fields, is_true, get_selected, get_selected_list, simplify_translate, \
    to_digit
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.cls import BaseModule


class General(BaseModule):
    CMDS = {
        'set': 'set',
        'search': 'get',
    }
    API_KEY_1 = 'proxy'
    API_KEY = 'general'
    API_MOD = 'proxy'
    API_CONT = 'settings'
    API_CONT_REL = 'service'
    API_CMD_REL = 'reconfigure'
    FIELDS_CHANGE = [
        'errors', 'icp_port', 'log', 'log_store', 'log_target', 'log_ignore',
        'dns_servers', 'dns_prio_ipv4', 'use_via_header', 'handling_forwarded_for',
        'hostname', 'email', 'suppress_version', 'connect_timeout', 'handling_uri_whitespace',
        'pinger', 'enabled',
    ]
    FIELDS_ALL = FIELDS_CHANGE
    FIELDS_TRANSLATE = {
        'errors': 'error_pages',
        'icp_port': 'icpPort',
        'dns_servers': 'alternateDNSservers',
        'dns_prio_ipv4': 'dnsV4First',
        'handling_forwarded_for': 'forwardedForHandling',
        'handling_uri_whitespace': 'uriWhitespaceHandling',
        'pinger': 'enablePinger',
        'use_via_header': 'useViaHeader',
        'suppress_version': 'suppressVersion',
        'connect_timeout': 'connecttimeout',
        'email': 'VisibleEmail',
        'hostname': 'VisibleHostname',
    }
    FIELDS_TRANSLATE_SPECIAL = {
        'log': 'accessLog',
        'log_store': 'storeLog',
        'log_target': 'target',
        'log_ignore': 'ignoreLogACL',
    }
    FIELDS_BOOL_INVERT = []
    FIELDS_TYPING = {
        'bool': [
            'enabled', 'pinger', 'suppress_version', 'use_via_header', 'dns_prio_ipv4',
        ],
        'list': ['dns_servers'],  # log_ignore = special handling
        'select': [
            'errors', 'handling_forwarded_for', 'handling_uri_whitespace'
        ],
        'int': ['connect_timeout', 'icp_port'],
    }
    FIELDS_IGNORE = ['logging', 'cache', 'traffic', 'parentproxy']
    INT_VALIDATIONS = {
        'connect_timeout': {'min': 1, 'max': 120},
        'icp_port': {'min': 1, 'max': 65535},
    }
    EXIST_ATTR = 'settings'
    TIMEOUT = 60.0

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None):
        BaseModule.__init__(self=self, m=module, r=result, s=session)
        self.settings = {}
        self.call_cnf = {
            'module': self.API_MOD,
            'controller': self.API_CONT,
        }
        self.s = Session(
            module=module,
            timeout=self.TIMEOUT,
        ) if session is None else session

    def check(self):
        validate_int_fields(module=self.m, data=self.p, field_minmax=self.INT_VALIDATIONS)

        self.settings = self._search_call()
        self.r['diff']['before'] = self.b.build_diff(self.settings)
        self.r['diff']['after'] = self.b.build_diff({
            k: v for k, v in self.p.items() if k in self.settings
        })

    def _search_call(self) -> dict:
        settings = self.s.get(cnf={
            **self.call_cnf, **{'command': self.CMDS['search']}
        })[self.API_KEY_1][self.API_KEY]

        simple = simplify_translate(
            existing=settings,
            typing=self.FIELDS_TYPING,
            translate=self.FIELDS_TRANSLATE,
            bool_invert=self.FIELDS_BOOL_INVERT,
            ignore=self.FIELDS_IGNORE,
        )

        simple['log'] = is_true(
            settings['logging']['enable'][self.FIELDS_TRANSLATE_SPECIAL['log']]
        )
        simple['log_store'] = is_true(
            settings['logging']['enable'][self.FIELDS_TRANSLATE_SPECIAL['log_store']]
        )
        simple['log_target'] = get_selected(
            settings['logging'][self.FIELDS_TRANSLATE_SPECIAL['log_target']]
        )
        simple['log_ignore'] = get_selected_list(
            settings['logging'][self.FIELDS_TRANSLATE_SPECIAL['log_ignore']]
        )

        return simple

    def get_existing(self) -> dict:
        return self._search_call()

    def _build_request(self) -> dict:
        raw_request = self.b.build_request(
            ignore_fields=['log', 'log_store', 'log_target', 'log_ignore']
        )
        raw_request[self.API_KEY]['logging'] = {
            'enable': {
                self.FIELDS_TRANSLATE_SPECIAL['log']: to_digit(self.p['log']),
                self.FIELDS_TRANSLATE_SPECIAL['log_store']: to_digit(self.p['log_store']),
            },
            self.FIELDS_TRANSLATE_SPECIAL['log_target']: self.p['log_target'],
            self.FIELDS_TRANSLATE_SPECIAL['log_ignore']: self.b.RESP_JOIN_CHAR.join(
                self.p['log_ignore']
            ),
        }

        return {self.API_KEY_1: raw_request}

    def update(self):
        self.b.update(enable_switch=False)
