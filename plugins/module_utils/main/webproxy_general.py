from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.main import \
    is_true, get_selected, get_selected_list, simplify_translate, to_digit
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.cls import GeneralModule


class General(GeneralModule):
    CMDS = {
        'set': 'set',
        'search': 'get',
    }
    API_KEY = 'general'
    API_KEY_PATH = f'proxy.{API_KEY}'
    API_KEY_1 = 'proxy'
    API_MOD = 'proxy'
    API_CONT = 'settings'
    API_CONT_REL = 'service'
    API_CMD_REL = 'reconfigure'
    FIELDS_CHANGE = [
        'errors', 'icp_port', 'log', 'log_store', 'log_target', 'log_ignore',
        'dns_servers', 'use_via_header', 'handling_forwarded_for',
        'hostname', 'email', 'suppress_version', 'connect_timeout', 'handling_uri_whitespace',
        'pinger', 'enabled',
    ]
    FIELDS_ALL = FIELDS_CHANGE
    FIELDS_TRANSLATE = {
        'errors': 'error_pages',
        'icp_port': 'icpPort',
        'dns_servers': 'alternateDNSservers',
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
    FIELDS_TYPING = {
        'bool': [
            'enabled', 'pinger', 'suppress_version', 'use_via_header',
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
    TIMEOUT = 60.0  # 'disable' taking long

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None):
        GeneralModule.__init__(self=self, m=module, r=result, s=session)

    def _search_call(self) -> dict:
        settings = self.s.get(cnf={
            **self.call_cnf, **{'command': self.CMDS['search']}
        })[self.API_KEY_1][self.API_KEY]

        simple = simplify_translate(
            existing=settings,
            typing=self.FIELDS_TYPING,
            translate=self.FIELDS_TRANSLATE,
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
