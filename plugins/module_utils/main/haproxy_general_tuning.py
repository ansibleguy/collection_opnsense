from ansible.module_utils.basic import AnsibleModule

from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.api import Session
from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.module import GeneralModule


class HaproxyGeneralTuning(GeneralModule):
    CMDS = {
        'set': 'set',
        'search': 'get',
    }
    API_KEY_PATH = 'haproxy.general.tuning'
    API_KEY_PATH_REQ = API_KEY_PATH
    API_MOD = 'haproxy'
    API_CONT = 'settings'
    API_CONT_REL = 'service'
    API_CMD_REL = 'reconfigure'

    FIELDS_TRANSLATE = {
        'max_connections': 'maxConnections',
        'resolvers_prefer': 'resolversPrefer',
        'ssl_server_verify': 'sslServerVerify',
        'max_dh_size': 'maxDHSize',
        'buffer_size': 'bufferSize',
        'spread_checks': 'spreadChecks',
        'bogus_proxy_enabled': 'bogusProxyEnabled',
        'lua_max_mem': 'luaMaxMem',
        'custom_options': 'customOptions',
        'ocsp_update_enabled': 'ocspUpdateEnabled',
        'ocsp_update_min_delay': 'ocspUpdateMinDelay',
        'ocsp_update_max_delay': 'ocspUpdateMaxDelay',
        'ssl_defaults_enabled': 'ssl_defaultsEnabled',
        'ssl_bind_options': 'ssl_bindOptions',
        'ssl_min_version': 'ssl_minVersion',
        'ssl_max_version': 'ssl_maxVersion',
        'ssl_cipher_list': 'ssl_cipherList',
        'ssl_cipher_suites': 'ssl_cipherSuites',
        'h2_initial_window_size': 'h2_initialWindowSize',
        'h2_initial_window_size_outgoing': 'h2_initialWindowSizeOutgoing',
        'h2_initial_window_size_incoming': 'h2_initialWindowSizeIncoming',
        'h2_max_concurrent_streams': 'h2_maxConcurrentStreams',
        'h2_max_concurrent_streams_outgoing': 'h2_maxConcurrentStreamsOutgoing',
        'h2_max_concurrent_streams_incoming': 'h2_maxConcurrentStreamsIncoming',
    }

    FIELDS_CHANGE = list(FIELDS_TRANSLATE.keys()) + ['root', 'nbthread']
    FIELDS_ALL = FIELDS_CHANGE

    FIELDS_TYPING = {
        'bool': ['root', 'bogus_proxy_enabled', 'ocsp_update_enabled', 'ssl_defaults_enabled'],
        'int': ['max_connections', 'nbthread', 'max_dh_size', 'buffer_size', 'spread_checks',
                'lua_max_mem', 'ocsp_update_min_delay', 'ocsp_update_max_delay',
                'h2_initial_window_size', 'h2_initial_window_size_outgoing',
                'h2_initial_window_size_incoming', 'h2_max_concurrent_streams',
                'h2_max_concurrent_streams_outgoing', 'h2_max_concurrent_streams_incoming'],
        'select': ['resolvers_prefer', 'ssl_server_verify', 'ssl_min_version', 'ssl_max_version'],
        'list': ['ssl_bind_options'],
    }

    INT_VALIDATIONS = {
        'max_connections': {'min': 0, 'max': 10000000},
        'nbthread': {'min': 1, 'max': 1024},
        'max_dh_size': {'min': 1024, 'max': 16384},
        'buffer_size': {'min': 1024, 'max': 1048576},
        'spread_checks': {'min': 0, 'max': 50},
        'lua_max_mem': {'min': 0, 'max': 1024},
        'ocsp_update_min_delay': {'min': 1, 'max': 86400},
        'ocsp_update_max_delay': {'min': 1, 'max': 86400},
        'h2_initial_window_size': {'min': 0, 'max': 10000000},
        'h2_initial_window_size_outgoing': {'min': 0, 'max': 10000000},
        'h2_initial_window_size_incoming': {'min': 0, 'max': 10000000},
        'h2_max_concurrent_streams': {'min': 0, 'max': 10000000},
        'h2_max_concurrent_streams_outgoing': {'min': 0, 'max': 10000000},
        'h2_max_concurrent_streams_incoming': {'min': 0, 'max': 10000000},
    }

    TIMEOUT = 60.0

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None):
        GeneralModule.__init__(self=self, m=module, r=result, s=session)
