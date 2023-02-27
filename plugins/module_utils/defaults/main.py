OPN_MOD_ARGS = dict(
    firewall=dict(type='str', required=True),
    api_port=dict(type=int, required=False, default=443),
    api_key=dict(type='str', required=False, no_log=True),
    api_secret=dict(type='str', required=False, no_log=True),
    api_credential_file=dict(type='path', required=False),
    ssl_verify=dict(type='bool', required=False, default=True),
    ssl_ca_file=dict(type='path', required=False),
    debug=dict(type='bool', required=False, default=False),
    timeout=dict(type='float', required=False),
)
BUILTIN_ALIASES = [
    'bogons', 'bogonsv6', 'sshlockout', 'virusprot',
]
BUILTIN_INTERFACE_ALIASES_REG = '^__.*?_network$'  # auto-added interface aliases

PURGE_MOD_ARGS = dict(
    action=dict(
        type='str', required=False, default='delete', choices=['disable', 'delete'],
        description='What to do with the matched items'
    ),
    filters=dict(
        type='dict', required=False, default={},
        description='Field-value pairs to filter on - per example: {param1: test} '
                    "- to only purge items that have 'param1' set to 'test'"
    ),
    filter_invert=dict(
        type='bool', required=False, default=False,
        description='If true - it will purge all but the filtered ones'
    ),
    filter_partial=dict(
        type='bool', required=False, default=False,
        description="If true - the filter will also match if it is just a partial value-match"
    ),
    force_all=dict(
        type='bool', required=False, default=False,
        description='If set to true and neither items, nor filters are provided - all items will be purged'
    ),
)

INFO_MOD_ARG = dict(
    output_info=dict(type='bool', required=False, default=False, aliases=['info']),
)

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

STATE_MOD_ARG_MULTI = dict(
    **STATE_ONLY_MOD_ARG,
    enabled=dict(type='bool', required=False, default=None),  # override only if set
)

RELOAD_MOD_ARG = dict(
    reload=dict(
        type='bool', required=False, default=True,
        description='If the running config should be reloaded on change - '
                    'will take some time'
    )
)

RELOAD_MOD_ARG_DEF_FALSE = dict(
    reload=dict(
        type='bool', required=False, default=False,
        description='If the running config should be reloaded on change - '
                    'will take some time'
    )
)

FAIL_MOD_ARG_MULTI = dict(
    fail_verification=dict(
        type='bool', required=False, default=False, aliases=['fail_verify'],
        description='Fail module if a single entry fails the verification.'
    ),
    fail_processing=dict(
        type='bool', required=False, default=True, aliases=['fail_proc'],
        description='Fail module if a single entry fails to be processed.'
    ),
)

DEBUG_CONFIG = dict(
    path_log='/tmp/ansibleguy.opnsense',
    log_api_calls='api_calls.log',
)

CONNECTION_TEST_TIMEOUT = 1.5
