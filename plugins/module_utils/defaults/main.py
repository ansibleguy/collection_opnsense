OPN_MOD_ARGS = dict(
    firewall=dict(
        type='str', required=True,
        description="IP-Address or DNS hostname of the target firewall. "
                    "Must be included as 'common name' or 'subject alternative name' in the firewalls web-certificate "
                    "to use 'ssl_verify=true'"
    ),
    api_port=dict(
        type='int', required=False, default=443,
        description='Port the target firewall uses for its web-interface'
    ),
    api_key=dict(
        type='str', required=False, no_log=True,
        description="API key used to authenticate, alternative to 'api_credential_file'"
    ),
    api_secret=dict(
        type='str', required=False, no_log=True,
        description="API secret used to authenticate, alternative to 'api_credential_file'. "
                    "Is set as 'no_log' parameter"
    ),
    api_credential_file=dict(
        type='path', required=False,
        description="Path to the api-credential file as downloaded through the web-interface. "
                    "Alternative to 'api_key' and 'api_secret'"
    ),
    ssl_verify=dict(
        type='bool', required=False, default=True,
        description='If the certificate of the target firewall should be validated. RECOMMENDED FOR PRODUCTION USAGE!'
    ),
    ssl_ca_file=dict(
        type='path', required=False,
        description='If you use an internal certificate-authority to create the certificate of the target firewall, '
                    'provide the path to its public key for validation'
    ),
    debug=dict(
        type='bool', required=False, default=False,
        description="Used to en-/disable the debug mode. All API requests and responses will be shown "
                    "as Ansible warnings at runtime. Will be hidden if the tasks 'no_log' parameter is set to 'true'"
    ),
    profiling=dict(
        type='bool', required=False, default=False,
        description="Used to en-/disable the profiling mode. "
                    "Time consumption of the module will be logged to '/tmp/oxlorg.opnsense'"
    ),
    api_timeout=dict(
        type='float', required=False, aliases=['timeout'],
        description='Manually override the modules default API-request timeout'
    ),
    api_retries=dict(
        type='int', required=False, default=0, aliases=['connect_retries'],
        description='Number of retries on API requests, in case there is an error when establishing the connection. '
                    'This does not handle errors returned by the OPNsense system'
    ),
)

BUILTIN_ALIASES = [
    'bogons', 'bogonsv6', 'sshlockout', 'virusprot', '__wazuh_agent_drop',
    'crowdsec_blocklists', 'crowdsec6_blocklists',
]
BUILTIN_INTERFACE_ALIASES_REG = '^__.*?_network$'  # auto-added interface aliases

STATE_ONLY_MOD_ARG = dict(
    state=dict(type='str', required=False, choices=['present', 'absent'], default='present'),
)

EN_ONLY_MOD_ARG = dict(
    enabled=dict(type='bool', required=False, default=True),
)

STATE_MOD_ARG = dict(
    **STATE_ONLY_MOD_ARG,
    **EN_ONLY_MOD_ARG,
)

RELOAD_MOD_ARG = dict(
    reload=dict(
        type='bool', required=False, default=False, aliases=['apply'],
        description='If the running config should be reloaded/applied on change - '
                    'will take some time'
    )
)

RELOAD_MOD_ARG_DEF_FALSE = dict(
    reload=dict(
        type='bool', required=False, default=False, aliases=['apply'],
        description='If the running config should be reloaded on change - '
                    'will take some time'
    )
)

DEBUG_CONFIG = dict(
    path_log='/tmp/oxlorg.opnsense',
    log_api_calls='api_calls.log',
)

CONNECTION_TEST_TIMEOUT = 1.5
