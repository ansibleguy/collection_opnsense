from ansible.module_utils.basic import AnsibleModule
from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.api import Session
from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.module import BaseModule


class HaproxyBackend(BaseModule):
    FIELD_ID = 'name'

    CMDS = {
        'add': 'addBackend',
        'del': 'delBackend',
        'set': 'setBackend',
        'search': 'get',
        'toggle': 'toggleBackend',
    }
    API_KEY_PATH = 'haproxy.backends.backend'
    API_MOD = 'haproxy'
    API_CONT = 'settings'
    API_CONT_REL = 'service'
    API_CMD_REL = 'reconfigure'

    FIELDS_TRANSLATE = {
        'proxy_protocol': 'proxyProtocol',
        'linked_servers': 'linkedServers',
        'linked_fcgi': 'linkedFcgi',
        'linked_resolver': 'linkedResolver',
        'resolver_opts': 'resolverOpts',
        'resolve_prefer': 'resolvePrefer',
        'health_check_enabled': 'healthCheckEnabled',
        'health_check': 'healthCheck',
        'health_check_log_status': 'healthCheckLogStatus',
        'check_interval': 'checkInterval',
        'check_down_interval': 'checkDownInterval',
        'health_check_fall': 'healthCheckFall',
        'health_check_rise': 'healthCheckRise',
        'linked_mailer': 'linkedMailer',
        'http2_enabled': 'http2Enabled',
        'http2_enabled_nontls': 'http2Enabled_nontls',
        'forwarded_header': 'forwardedHeader',
        'forwarded_header_parameters': 'forwardedHeaderParameters',
        'forward_for': 'forwardFor',
        'stickiness_conn_rate_period': 'stickiness_connRatePeriod',
        'stickiness_sess_rate_period': 'stickiness_sessRatePeriod',
        'stickiness_http_req_rate_period': 'stickiness_httpReqRatePeriod',
        'stickiness_http_err_rate_period': 'stickiness_httpErrRatePeriod',
        'stickiness_bytes_in_rate_period': 'stickiness_bytesInRatePeriod',
        'stickiness_bytes_out_rate_period': 'stickiness_bytesOutRatePeriod',
        'basic_auth_enabled': 'basicAuthEnabled',
        'basic_auth_users': 'basicAuthUsers',
        'basic_auth_groups': 'basicAuthGroups',
        'tuning_timeout_connect': 'tuning_timeoutConnect',
        'tuning_timeout_check': 'tuning_timeoutCheck',
        'tuning_timeout_server': 'tuning_timeoutServer',
        'custom_options': 'customOptions',
        'linked_actions': 'linkedActions',
        'linked_errorfiles': 'linkedErrorfiles',
    }

    FIELDS_CHANGE = list(FIELDS_TRANSLATE.keys()) + [
        'enabled', 'name', 'description', 'mode', 'algorithm', 'random_draws',
        'source', 'persistence', 'ba_advertised_protocols', 'persistence_cookiemode',
        'persistence_cookiename', 'persistence_stripquotes', 'stickiness_pattern',
        'stickiness_expire', 'stickiness_size', 'stickiness_cookiename',
        'stickiness_cookielength', 'tuning_retries', 'tuning_defaultserver',
        'tuning_noport', 'tuning_httpreuse', 'tuning_caching'
    ]
    FIELDS_ALL = FIELDS_CHANGE

    FIELDS_TYPING = {
        'bool': [
            'enabled', 'health_check_enabled', 'health_check_log_status',
            'http2_enabled', 'http2_enabled_nontls', 'forwarded_header',
            'forward_for', 'persistence_stripquotes', 'basic_auth_enabled',
            'tuning_noport', 'tuning_caching'
        ],
        'list': [
            'linked_servers', 'resolver_opts', 'ba_advertised_protocols',
            'basic_auth_users', 'basic_auth_groups',
            'linked_actions', 'linked_errorfiles', 'forwarded_header_parameters'
        ],
        'int': [
            'random_draws', 'health_check_fall', 'health_check_rise',
            'stickiness_cookielength', 'tuning_retries'
        ],
        'select': [
            'mode', 'algorithm', 'proxy_protocol', 'linked_fcgi',
            'linked_resolver', 'resolve_prefer', 'health_check',
            'linked_mailer', 'persistence', 'persistence_cookiemode',
            'stickiness_pattern', 'tuning_httpreuse'
        ],
    }

    EXIST_ATTR = 'haproxy_backend'

    SEARCH_ADDITIONAL = {
        'existing_servers': 'haproxy.servers.server',
        'existing_fcgis': 'haproxy.fcgis.fcgi',
        'existing_resolvers': 'haproxy.resolvers.resolver',
        'existing_healthchecks': 'haproxy.healthchecks.healthcheck',
        'existing_mailers': 'haproxy.mailers.mailer',
        'existing_users': 'haproxy.users.user',
        'existing_groups': 'haproxy.groups.group',
        'existing_actions': 'haproxy.actions.action',
        'existing_errorfiles': 'haproxy.errorfiles.errorfile',
    }

    STR_VALIDATIONS = {
        'name': r'^([0-9a-zA-Z._\-]){1,255}$',
    }

    INT_VALIDATIONS = {
        'random_draws': {'min': 2, 'max': 1000},
        'health_check_fall': {'min': 1, 'max': 100},
        'health_check_rise': {'min': 1, 'max': 100},
        'tuning_retries': {'min': 0, 'max': 100},
    }

    TIMEOUT = 30.0

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None):
        BaseModule.__init__(self=self, m=module, r=result, s=session)
        self.haproxy_backend = {}
        # Initialize all existing items that might be referenced
        self.existing_servers = {}
        self.existing_fcgis = {}
        self.existing_resolvers = {}
        self.existing_healthchecks = {}
        self.existing_mailers = {}
        self.existing_users = {}
        self.existing_groups = {}
        self.existing_actions = {}
        self.existing_errorfiles = {}

    def check(self) -> None:
        self._base_check()
        if self.p['state'] == 'present':
            # Validate linked servers
            if self.p.get('linked_servers'):
                self.find_multiple_links(
                    field='linked_servers',
                    existing=self.existing_servers,
                )
            # Validate linked FCGIs
            if self.p.get('linked_fcgi'):
                self.find_single_link(
                    field='linked_fcgi',
                    existing=self.existing_fcgis,
                )
            # Validate linked resolver
            if self.p.get('linked_resolver'):
                self.find_single_link(
                    field='linked_resolver',
                    existing=self.existing_resolvers,
                )
            # Validate health check
            if self.p.get('health_check'):
                self.find_single_link(
                    field='health_check',
                    existing=self.existing_healthchecks,
                )
            # Validate linked mailer
            if self.p.get('linked_mailer'):
                self.find_single_link(
                    field='linked_mailer',
                    existing=self.existing_mailers,
                )
            # Validate basic auth users
            if self.p.get('basic_auth_users'):
                self.find_multiple_links(
                    field='basic_auth_users',
                    existing=self.existing_users,
                )
            # Validate basic auth groups
            if self.p.get('basic_auth_groups'):
                self.find_multiple_links(
                    field='basic_auth_groups',
                    existing=self.existing_groups,
                )
            # Validate linked actions
            if self.p.get('linked_actions'):
                self.find_multiple_links(
                    field='linked_actions',
                    existing=self.existing_actions,
                )
            # Validate linked errorfiles
            if self.p.get('linked_errorfiles'):
                self.find_multiple_links(
                    field='linked_errorfiles',
                    existing=self.existing_errorfiles,
                )
