from ansible_collections.ansibleguy.opnsense.plugins.module_utils.defaults import \
    OPN_MOD_ARGS, STATE_MOD_ARG

RULE_DEFAULTS = {
    'sequence': 1,
    'action': 'pass',
    'quick': True,
    'interface': ['lan'],
    'direction': 'in',
    'ip_protocol': 'inet',
    'protocol': 'any',
    'source_invert': False,
    'source_net': 'any',
    'source_port': '',
    'destination_invert': False,
    'destination_net': 'any',
    'destination_port': '',
    'gateway': '',
    'log': True,
    'state': 'present',
    'enabled': True,
    'description': '',
    'debug': False,
}

RULE_MOD_ARG_ALIASES = {
    'sequence': ['seq'],
    'action': ['a'],
    'quick': ['q'],
    'interface': ['int', 'i'],
    'direction': ['dir'],
    'ip_protocol': ['ip', 'ip_proto'],
    'protocol': ['proto', 'p'],
    'source_invert': ['src_inv', 'si', 'src_not'],
    'source_net': ['src', 's'],
    'source_port': ['src_port', 'sp'],
    'destination_invert': ['dest_inv', 'di', 'dest_not'],
    'destination_net': ['dest', 'd'],
    'destination_port': ['dest_port', 'dp'],
    'gateway': ['gw', 'g'],
    'log': ['l'],
    'description': ['desc'],
    'state': ['st'],
    'enabled': ['en'],
}

RULE_MATCH_FIELDS_ARG = dict(
    match_fields=dict(
        type='list', required=True, elements='str',
        description='Fields that are used to match configured rules with the running config - '
                    "if any of those fields are changed, the module will think it's a new rule",
        choises=[
            'sequence', 'action', 'interface', 'direction', 'ip_protocol', 'protocol',
            'source_invert', 'source_net', 'source_port', 'destination_invert', 'destination_net',
            'destination_port', 'gateway', 'description', 'uuid',
        ]
    ),
)

RULE_MOD_ARGS = dict(
    sequence=dict(
        type='int', required=False, default=RULE_DEFAULTS['sequence'],
        aliases=RULE_MOD_ARG_ALIASES['sequence']
    ),
    action=dict(
        type='str', required=False, default=RULE_DEFAULTS['action'], choices=['pass', 'block', 'reject'],
        aliases=RULE_MOD_ARG_ALIASES['action']
    ),
    quick=dict(type='bool', required=False, default=RULE_DEFAULTS['quick'], aliases=RULE_MOD_ARG_ALIASES['quick']),
    interface=dict(
        type='list', required=False, default=RULE_DEFAULTS['interface'], aliases=RULE_MOD_ARG_ALIASES['interface'],
        description='One or multiple interfaces use this rule on', elements='str',
    ),
    direction=dict(
        type='str', required=False, default=RULE_DEFAULTS['direction'], aliases=RULE_MOD_ARG_ALIASES['direction'],
        choices=['in', 'out']
    ),
    ip_protocol=dict(
        type='str', required=False, choices=['inet', 'inet6'],
        default=RULE_DEFAULTS['ip_protocol'], description="IPv4 = 'inet', IPv6 = 'inet6'",
        aliases=RULE_MOD_ARG_ALIASES['ip_protocol'],
    ),
    protocol=dict(
        type='str', required=False, default=RULE_DEFAULTS['protocol'], aliases=RULE_MOD_ARG_ALIASES['protocol'],
        description="Protocol like 'TCP', 'UDP', 'TCP/UDP' and so on."
    ),
    source_invert=dict(
        type='bool', required=False, default=RULE_DEFAULTS['source_invert'],
        aliases=RULE_MOD_ARG_ALIASES['source_invert'],
    ),
    source_net=dict(
        type='str', required=False, default=RULE_DEFAULTS['source_net'], aliases=RULE_MOD_ARG_ALIASES['source_net'],
        description="Host, network, alias or 'any'"),
    source_port=dict(
        type='str', required=False, default=RULE_DEFAULTS['source_port'], aliases=RULE_MOD_ARG_ALIASES['source_port'],
        description='Leave empty to allow all, alias not supported'
    ),
    destination_invert=dict(
        type='bool', required=False, default=RULE_DEFAULTS['destination_invert'],
        aliases=RULE_MOD_ARG_ALIASES['destination_invert'],
    ),
    destination_net=dict(
        type='str', required=False, default=RULE_DEFAULTS['destination_net'],
        aliases=RULE_MOD_ARG_ALIASES['destination_net'], description="Host, network, alias or 'any'"
    ),
    destination_port=dict(
        type='str', required=False, default=RULE_DEFAULTS['destination_port'],
        aliases=RULE_MOD_ARG_ALIASES['destination_port'],
        description='Leave empty to allow all, alias not supported'
    ),
    gateway=dict(
        type='str', required=False, default=RULE_DEFAULTS['gateway'],
        aliases=RULE_MOD_ARG_ALIASES['gateway'], description='Existing gateway to use'
    ),
    log=dict(type='bool', required=False, default=RULE_DEFAULTS['log'], aliases=RULE_MOD_ARG_ALIASES['log'],),
    description=dict(
        type='str', required=False, default=RULE_DEFAULTS['description'],
        aliases=RULE_MOD_ARG_ALIASES['description']
    ),
    uuid=dict(type='str', required=False, description='Optionally you can supply the uuid of an existing rule'),
    **STATE_MOD_ARG,
    **RULE_MATCH_FIELDS_ARG,
    **OPN_MOD_ARGS,
)

RULE_MOD_ARG_KEY_FIELD = dict(
    key_field=dict(
        type='str', required=True, choises=['sequence', 'description', 'uuid'], aliases=['key'],
        description='What field is used as key of the provided dictionary'
    )
)
