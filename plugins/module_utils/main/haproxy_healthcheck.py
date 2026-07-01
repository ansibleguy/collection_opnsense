from ansible.module_utils.basic import AnsibleModule
from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.api import Session
from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.module import BaseModule


class HaproxyHealthcheck(BaseModule):
    FIELD_ID = 'name'

    CMDS = {
        'add': 'addHealthcheck',
        'del': 'delHealthcheck',
        'set': 'setHealthcheck',
        'search': 'get',
        'toggle': 'toggleHealthcheck',
    }
    API_KEY_PATH = 'haproxy.healthchecks.healthcheck'
    API_MOD = 'haproxy'
    API_CONT = 'settings'
    API_CONT_REL = 'service'
    API_CMD_REL = 'reconfigure'

    FIELDS_TRANSLATE = {
        'ssl_sni': 'sslSNI',
        'http_expression_enabled': 'http_expressionEnabled',
        'tcp_send_value': 'tcp_sendValue',
        'tcp_match_type': 'tcp_matchType',
        'tcp_match_value': 'tcp_matchValue',
    }

    FIELDS_CHANGE = list(FIELDS_TRANSLATE.keys()) + [
        'name', 'description', 'type', 'interval', 'ssl', 'checkport',
        'http_method', 'http_uri', 'http_version', 'http_host', 'http_expression',
        'http_negate', 'http_value', 'tcp_enabled', 'tcp_negate', 'agent_port',
        'mysql_user', 'mysql_post41', 'pgsql_user', 'smtp_domain', 'esmtp_domain'
    ]
    FIELDS_ALL = FIELDS_CHANGE

    FIELDS_TYPING = {
        'bool': [
            'http_expression_enabled', 'http_negate', 'tcp_enabled', 'tcp_negate',
            'mysql_post41'
        ],
        'int': ['checkport', 'agent_port'],
        'select': [
            'type', 'ssl', 'http_method', 'http_version', 'http_expression',
            'tcp_match_type'
        ],
    }

    EXIST_ATTR = 'haproxy_healthcheck'

    STR_VALIDATIONS = {
        'name': r'^[^\t^,^;^\.^\[^\]^\{^\}]{1,255}$',
    }

    INT_VALIDATIONS = {
        'checkport': {'min': 1, 'max': 65535},
        'agent_port': {'min': 1, 'max': 65535},
    }

    TIMEOUT = 20.0

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None):
        BaseModule.__init__(self=self, m=module, r=result, s=session)
        self.haproxy_healthcheck = {}
