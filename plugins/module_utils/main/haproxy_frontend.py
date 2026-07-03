from ansible.module_utils.basic import AnsibleModule
from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.api import Session
from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.module import BaseModule


class HaproxyFrontend(BaseModule):
    FIELD_ID = 'name'

    CMDS = {
        'add': 'addFrontend',
        'del': 'delFrontend',
        'set': 'setFrontend',
        'search': 'get',
        'toggle': 'toggleFrontend',
    }
    API_KEY_PATH = 'haproxy.frontends.frontend'
    API_MOD = 'haproxy'
    API_CONT = 'settings'
    API_CONT_REL = 'service'
    API_CMD_REL = 'reconfigure'

    FIELDS_TRANSLATE = {
        'bind_options': 'bindOptions',
        'default_backend': 'defaultBackend',
        'ssl_custom_options': 'ssl_customOptions',
        'ssl_advanced_enabled': 'ssl_advancedEnabled',
        'ssl_bind_options': 'ssl_bindOptions',
        'ssl_min_version': 'ssl_minVersion',
        'ssl_max_version': 'ssl_maxVersion',
        'ssl_cipher_list': 'ssl_cipherList',
        'ssl_cipher_suites': 'ssl_cipherSuites',
        'ssl_hsts_enabled': 'ssl_hstsEnabled',
        'ssl_hsts_include_sub_domains': 'ssl_hstsIncludeSubDomains',
        'ssl_hsts_preload': 'ssl_hstsPreload',
        'ssl_hsts_max_age': 'ssl_hstsMaxAge',
        'ssl_client_auth_enabled': 'ssl_clientAuthEnabled',
        'ssl_client_auth_verify': 'ssl_clientAuthVerify',
        'ssl_client_auth_cas': 'ssl_clientAuthCAs',
        'ssl_client_auth_crls': 'ssl_clientAuthCRLs',
        'http2_enabled': 'http2Enabled',
        'http2_enabled_nontls': 'http2Enabled_nontls',
        'forwarded_header': 'forwardedHeader',
        'forward_for': 'forwardFor',
        'basic_auth_enabled': 'basicAuthEnabled',
        'basic_auth_users': 'basicAuthUsers',
        'basic_auth_groups': 'basicAuthGroups',
        'tuning_max_connections': 'tuning_maxConnections',
        'tuning_timeout_client': 'tuning_timeoutClient',
        'tuning_timeout_http_req': 'tuning_timeoutHttpReq',
        'tuning_timeout_http_keep_alive': 'tuning_timeoutHttpKeepAlive',
        'linked_cpu_affinity_rules': 'linkedCpuAffinityRules',
        'logging_dont_log_null': 'logging_dontLogNull',
        'logging_dont_log_normal': 'logging_dontLogNormal',
        'logging_log_separate_errors': 'logging_logSeparateErrors',
        'logging_detailed_log': 'logging_detailedLog',
        'logging_socket_stats': 'logging_socketStats',
        'stickiness_data_types': 'stickiness_dataTypes',
        'stickiness_conn_rate_period': 'stickiness_connRatePeriod',
        'stickiness_sess_rate_period': 'stickiness_sessRatePeriod',
        'stickiness_http_req_rate_period': 'stickiness_httpReqRatePeriod',
        'stickiness_http_err_rate_period': 'stickiness_httpErrRatePeriod',
        'stickiness_bytes_in_rate_period': 'stickiness_bytesInRatePeriod',
        'stickiness_bytes_out_rate_period': 'stickiness_bytesOutRatePeriod',
        'connection_behaviour': 'connectionBehaviour',
        'custom_options': 'customOptions',
        'linked_actions': 'linkedActions',
        'linked_errorfiles': 'linkedErrorfiles',
    }

    FIELDS_CHANGE = list(FIELDS_TRANSLATE.keys()) + [
        'enabled', 'name', 'description', 'bind', 'mode', 'ssl_enabled',
        'ssl_certificates', 'ssl_default_certificate', 'advertised_protocols',
        'tuning_shards', 'stickiness_pattern', 'stickiness_expire', 'stickiness_size',
        'stickiness_counter', 'stickiness_counter_key', 'stickiness_length',
        'prometheus_enabled', 'prometheus_path'
    ]
    FIELDS_ALL = FIELDS_CHANGE

    FIELDS_TYPING = {
        'bool': [
            'enabled', 'ssl_enabled', 'ssl_advanced_enabled', 'ssl_hsts_enabled',
            'ssl_hsts_include_sub_domains', 'ssl_hsts_preload', 'ssl_client_auth_enabled',
            'http2_enabled', 'http2_enabled_nontls', 'forwarded_header', 'forward_for',
            'basic_auth_enabled', 'logging_dont_log_null', 'logging_dont_log_normal',
            'logging_log_separate_errors', 'logging_detailed_log', 'logging_socket_stats',
            'stickiness_counter', 'prometheus_enabled'
        ],
        'list': [
            'bind', 'ssl_certificates', 'ssl_bind_options', 'ssl_client_auth_cas',
            'ssl_client_auth_crls', 'advertised_protocols', 'basic_auth_users',
            'basic_auth_groups', 'linked_cpu_affinity_rules', 'stickiness_data_types',
            'linked_actions', 'linked_errorfiles'
        ],
        'int': [
            'ssl_hsts_max_age', 'tuning_max_connections', 'tuning_shards',
            'stickiness_length'
        ],
        'select': [
            'mode', 'default_backend', 'ssl_default_certificate', 'ssl_min_version',
            'ssl_max_version', 'ssl_client_auth_verify', 'stickiness_pattern',
            'connection_behaviour'
        ],
    }
    FIELDS_OPTIONAL = ['forwarded_header']

    EXIST_ATTR = 'haproxy_frontend'

    SEARCH_ADDITIONAL = {
        'existing_backends': 'haproxy.backends.backend',
        'existing_actions': 'haproxy.actions.action',
        'existing_errorfiles': 'haproxy.errorfiles.errorfile',
        'existing_users': 'haproxy.users.user',
        'existing_groups': 'haproxy.groups.group',
        'existing_cpus': 'haproxy.cpus.cpu',
    }

    STR_VALIDATIONS = {
        'name': r'^([0-9a-zA-Z._\-]){1,255}$',
    }

    INT_VALIDATIONS = {
        'ssl_hsts_max_age': {'min': 1, 'max': 1000000000},
        'tuning_max_connections': {'min': 0, 'max': 10000000},
        'tuning_shards': {'min': 2, 'max': 1000},
        'stickiness_length': {'min': 1, 'max': 16384},
    }

    TIMEOUT = 30.0

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None):
        BaseModule.__init__(self=self, m=module, r=result, s=session)
        self.haproxy_frontend = {}
        # Initialize existing items that might be referenced
        self.existing_backends = {}
        self.existing_actions = {}
        self.existing_errorfiles = {}
        self.existing_users = {}
        self.existing_groups = {}
        self.existing_cpus = {}

    def check(self) -> None:
        self._base_check()
        if self.p['state'] == 'present':
            # Validate default backend
            if self.p.get('default_backend'):
                self.find_single_link(
                    field='default_backend',
                    existing=self.existing_backends,
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
            # Validate linked CPU affinity rules
            if self.p.get('linked_cpu_affinity_rules'):
                self.find_multiple_links(
                    field='linked_cpu_affinity_rules',
                    existing=self.existing_cpus,
                )
