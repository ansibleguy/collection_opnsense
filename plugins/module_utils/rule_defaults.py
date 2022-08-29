from ansible_collections.ansibleguy.opnsense.plugins.module_utils.defaults import OPN_MOD_ARGS

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

RULE_MATCH_FIELDS_ARG = dict(
    match_fields=dict(
        type='list', required=True,
        description='Fields that are used to match configured rules with the running config - '
                    "if any of those fields are changed, the module will think it's a new rule",
        choises=[
            'sequence', 'action', 'interface', 'direction', 'ip_protocol', 'protocol',
            'source_invert', 'source_net', 'source_port', 'destination_invert', 'destination_net',
            'destination_port', 'gateway', 'description',
        ]
    ),
)

RULE_MOD_ARGS = dict(
    sequence=dict(type='int', required=False, default=RULE_DEFAULTS['sequence']),
    action=dict(type='str', required=False, default=RULE_DEFAULTS['action'], choices=['pass', 'block', 'reject']),
    quick=dict(type='bool', required=False, default=RULE_DEFAULTS['quick']),
    interface=dict(
        type='list', required=False, default=RULE_DEFAULTS['interface'],
        description='One or multiple interfaces use this rule on'
    ),
    direction=dict(
        type='str', required=False, default=RULE_DEFAULTS['direction'],
        choices=['in', 'out']
    ),
    ip_protocol=dict(
        type='str', required=False, choices=['inet', 'inet6'], default=RULE_DEFAULTS['ip_protocol'],
        description="IPv4 = 'inet', IPv6 = 'inet6'"
    ),
    protocol=dict(
        type='str', required=False, default=RULE_DEFAULTS['protocol'],
        description="Protocol like 'TCP', 'UDP', 'TCP/UDP' and so on."
    ),
    source_invert=dict(type='bool', required=False, default=RULE_DEFAULTS['source_invert']),
    source_net=dict(
        type='str', required=False, default=RULE_DEFAULTS['source_net'],
        description="Host, network, alias or 'any'"),
    source_port=dict(
        type='str', required=False, default=RULE_DEFAULTS['source_port'],
        description='Leave empty to allow all, alias not supported'
    ),
    destination_invert=dict(type='bool', required=False, default=RULE_DEFAULTS['destination_invert']),
    destination_net=dict(
        type='str', required=False, default=RULE_DEFAULTS['destination_net'],
        description="Host, network, alias or 'any'"
    ),
    destination_port=dict(
        type='str', required=False, default=RULE_DEFAULTS['destination_port'],
        description='Leave empty to allow all, alias not supported'
    ),
    gateway=dict(
        type='str', required=False, default=RULE_DEFAULTS['gateway'],
        description='Existing gateway to use'
    ),
    log=dict(type='bool', required=False, default=RULE_DEFAULTS['log']),
    description=dict(type='str', required=False, default=RULE_DEFAULTS['description']),
    state=dict(type='str', default=RULE_DEFAULTS['state'], required=False, choices=['present', 'absent']),
    enabled=dict(type='bool', required=False, default=RULE_DEFAULTS['enabled']),
    **RULE_MATCH_FIELDS_ARG,
    **OPN_MOD_ARGS,
)
