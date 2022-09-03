OPN_MOD_ARGS = dict(
    firewall=dict(type='str', required=True),
    api_port=dict(type=int, required=False, default=443),
    api_key=dict(type='str', required=False, no_log=True),
    api_secret=dict(type='str', required=False, no_log=True),
    api_credential_file=dict(type='path', required=False, no_log=True),
    ssl_verify=dict(type='bool', required=False, default=True),
    ssl_ca_file=dict(type='path', required=False),
    debug=dict(type='bool', required=False, default=False),
)
BUILTIN_ALIASES = [
    'bogons', 'bogonsv6', 'sshlockout', 'virusprot',
]
BUILTIN_INTERFACE_ALIASES_REG = '^__.*?_network$'  # auto-added interface aliases

PURGE_MOD_ARGS = dict(
    action=dict(
        type='str', required=False, default='delete', choises=['disable', 'delete'],
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

STATE_MOD_ARG = dict(
    state=dict(type='str', required=False, choices=['present', 'absent']),
    enabled=dict(type='bool', required=False, default=True),
)

STATE_MOD_ARG_MULTI = dict(
    state=dict(type='str', required=False, choices=['present', 'absent']),
    enabled=dict(type='bool', required=False, default=None),  # override only if set
)
