from ansible_collections.oxlorg.opnsense.plugins.module_utils.defaults.main import STATE_MOD_ARG

RULE_DEFAULTS = {
    'sequence': 1,
    'action': 'pass',
    'quick': True,
    'interface': ['lan'],
    'interface_invert': False,
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
    'replyto': '',
    'disable_replyto': False,
    'log': True,
    'allow_opts': False,
    'state_type': 'keep',
    'state_policy': '',
    'state_timeout': None,
    'max_states': None,
    'max_src_nodes': None,
    'max_src_states': None,
    'max_src_conn': None,
    'max_src_conn_rate': None,
    'max_src_conn_rates': None,
    'overload': None,
    'adaptive_start': None,
    'adaptive_end': None,
    'prio': '',
    'set_prio': '',
    'set_prio_low': '',
    'tag': '',
    'tagged': '',
    'tcp_flags': [],
    'tcp_flags_clear': [],
    'schedule': '',
    'tos': '',
    'state': 'present',
    'enabled': True,
    'description': '',
    'debug': False,
    'icmp_type': [],
    'icmpv6_type': [],
    'divert_to': '',
    'shaper1': '',
    'shaper2': '',
}

RULE_MOD_ARG_ALIASES = {
    'sequence': ['seq'],
    'action': ['a'],
    'quick': ['q'],
    'interface': ['int', 'i'],
    'interface_invert': ['int_inv', 'ii', 'int_not'],
    'direction': ['dir'],
    'ip_protocol': ['ip', 'ip_proto'],
    'protocol': ['proto', 'p'],
    'source_invert': ['src_inv', 'si', 'src_not'],
    'source_net': ['source', 'src', 's'],
    'source_port': ['src_port', 'sp'],
    'destination_invert': ['dest_inv', 'di', 'dest_not'],
    'destination_net': ['destination', 'dest', 'd'],
    'destination_port': ['dest_port', 'dp'],
    'gateway': ['gw', 'g'],
    'replyto': ['rt'],
    'log': ['l'],
    'allow_opts': ['opts'],
    'overload': ['ol'],
    'schedule': ['sched'],
    'description': ['name', 'desc'],
    'state': ['st'],
    'enabled': ['en'],
    'icmp_type': ['icmp_types'],
    'icmpv6_type': ['icmpv6_types', 'ip6_icmp_types'],
}

RULE_MATCH_FIELDS_ARG = dict(
    match_fields=dict(
        type='list', required=True, elements='str',
        description='Fields that are used to match configured rules with the running config - '
                    "if any of those fields are changed, the module will think it's a new rule",
        choices=[
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
    interface_invert=dict(
        type='bool', required=False, default=RULE_DEFAULTS['interface_invert'],
        aliases=RULE_MOD_ARG_ALIASES['interface_invert'],
    ),
    direction=dict(
        type='str', required=False, default=RULE_DEFAULTS['direction'], aliases=RULE_MOD_ARG_ALIASES['direction'],
        choices=['in', 'out', 'any']
    ),
    ip_protocol=dict(
        type='str', required=False, choices=['inet', 'inet6', 'inet46'],
        default=RULE_DEFAULTS['ip_protocol'], description="IPv4 = 'inet', IPv6 = 'inet6', 'IPv4+6 = 'inet46'",
        aliases=RULE_MOD_ARG_ALIASES['ip_protocol'],
    ),
    protocol=dict(
        type='str', required=False, default=RULE_DEFAULTS['protocol'], aliases=RULE_MOD_ARG_ALIASES['protocol'],
        description="Protocol like 'TCP', 'UDP', 'ICMP', 'TCP/UDP' and so on."
    ),
    source_invert=dict(
        type='bool', required=False, default=RULE_DEFAULTS['source_invert'],
        aliases=RULE_MOD_ARG_ALIASES['source_invert'],
    ),
    source_net=dict(
        type='str', required=False, default=RULE_DEFAULTS['source_net'], aliases=RULE_MOD_ARG_ALIASES['source_net'],
        description="Host, network, alias or 'any'",
    ),
    source_port=dict(
        type='str', required=False, default=RULE_DEFAULTS['source_port'], aliases=RULE_MOD_ARG_ALIASES['source_port'],
        description='Leave empty to allow all, valid port-number, name, alias or range'
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
        description='Leave empty to allow all, valid port-number, name, alias or range'
    ),
    gateway=dict(
        type='str', required=False, default=RULE_DEFAULTS['gateway'],
        aliases=RULE_MOD_ARG_ALIASES['gateway'], description='Existing gateway to use'
    ),
    replyto=dict(
        type='str', required=False, default=RULE_DEFAULTS['replyto'],
        aliases=RULE_MOD_ARG_ALIASES['replyto'],
        description='Determines how packets route back in the opposite direction'
    ),
    disable_replyto=dict(
        type='bool', required=False, default=RULE_DEFAULTS['disable_replyto'],
        description='Explicit disable reply-to for this rule'
    ),
    log=dict(type='bool', required=False, default=RULE_DEFAULTS['log'], aliases=RULE_MOD_ARG_ALIASES['log'],),
    allow_opts=dict(
        type='bool', required=False, default=RULE_DEFAULTS['allow_opts'], aliases=RULE_MOD_ARG_ALIASES['allow_opts'],
        description='Allows packets with IP options to pass'
    ),
    state_type=dict(
        type='str', required=False, default=RULE_DEFAULTS['state_type'],
        choices=['keep', 'sloppy', 'modulate', 'synproxy', 'none'],
        description='State tracking mechanism to use'
    ),
    state_policy=dict(
        type='str', required=False, default=RULE_DEFAULTS['state_policy'],
        choices=['', 'if-bound', 'floating'], description='State tracking mechanism to use'
    ),
    state_timeout=dict(
        type='int', required=False,
        description='State Timeout in seconds (TCP only)'
    ),
    max_states=dict(type='int', required=False, description='Limits the number of concurrent states',),
    max_src_nodes=dict(
        type='int', required=False,
        description='Limits the number of source addresses which can simultaneously have state table entries'
    ),
    max_src_states=dict(
        type='int', required=False,
        description='Limits the number of simultaneous state entries that a single source address can create'
    ),
    max_src_conn=dict(
        type='int', required=False,
        description='Limit the number of simultaneous TCP connections a single host can make'
    ),
    max_src_conn_rate=dict(
        type='int', required=False,
        description='Maximum new connections per host, measured over time'
    ),
    max_src_conn_rates=dict(
        type='int', required=False,
        description='Time interval (seconds) to measure the number of connections'
    ),
    overload=dict(
        type='str', required=False,
        aliases=RULE_MOD_ARG_ALIASES['overload'],
        description='Overload table used when max new connections per time interval has been reached'
    ),
    adaptive_start=dict(type='int', required=False,),
    adaptive_end=dict(type='int', required=False,),
    prio=dict(
        type='str', required=False, default=RULE_DEFAULTS['prio'],
        choices=['', '0', '1', '2', '3', '4', '5', '6', '7'],
        description='Match packets which have the given queueing priority assigned'
    ),
    set_prio=dict(
        type='str', required=False, default=RULE_DEFAULTS['set_prio'],
        choices=['', '0', '1', '2', '3', '4', '5', '6', '7'],
        description='Assigne a specific queueing priority'
    ),
    set_prio_low=dict(
        type='str', required=False, default=RULE_DEFAULTS['set_prio_low'],
        choices=['', '0', '1', '2', '3', '4', '5', '6', '7'],
        description='Assigne a specific queueing priority to packets which have a TOS of lowdelay '
                    'and TCP ACKs with no data payload'
    ),
    tag=dict(type='str', required=False, default=RULE_DEFAULTS['tag'],),
    tagged=dict(type='str', required=False, default=RULE_DEFAULTS['tagged'],),
    tcp_flags=dict(
        type='list', elements='str', required=False, default=RULE_DEFAULTS['tcp_flags'],
        choices=['syn', 'ack', 'fin', 'rst', 'psh', 'urg', 'ece', 'cwr'],
        description='TCP flags that must be set for this rule to match'
    ),
    tcp_flags_clear=dict(
        type='list', elements='str', required=False, default=RULE_DEFAULTS['tcp_flags_clear'],
        choices=['syn', 'ack', 'fin', 'rst', 'psh', 'urg', 'ece', 'cwr'],
        description='TCP flags that must be cleared for this rule to match'
    ),
    schedule=dict(
        type='str', required=False, default=RULE_DEFAULTS['schedule'],
        aliases=RULE_MOD_ARG_ALIASES['schedule'],
    ),
    tos=dict(
        type='str', required=False, default=RULE_DEFAULTS['tos'],
        description='Match packets which have the given TOS/DCSP assigned'
    ),
    description=dict(
        type='str', required=False, default=RULE_DEFAULTS['description'],
        aliases=RULE_MOD_ARG_ALIASES['description']
    ),
    uuid=dict(type='str', required=False, description='Optionally you can supply the uuid of an existing rule'),
    icmp_type=dict(
        type='list', elements='str', required=False, default=RULE_DEFAULTS['icmp_type'],
        aliases=RULE_MOD_ARG_ALIASES['icmp_type'], choices=[
            'echoreq', 'echorep', 'unreach', 'redir', 'routeradv', 'routersol', 'timex',
            'paramprob', 'timereq', 'timerep', 'photuris',
        ],
        description='If protocol is ICMP you can specify the types'
    ),
    icmpv6_type=dict(
        type='list', elements='str', required=False, default=RULE_DEFAULTS['icmpv6_type'],
        aliases=RULE_MOD_ARG_ALIASES['icmpv6_type'], choices=[
            'unreach', 'toobig', 'timex', 'paramprob', 'echoreq', 'echorep', 'listqry', 'listenrep',
            'listendone', 'routersol', 'reouteradv', 'neighbrsol', 'neighbradv', 'redir', 'routrrenum',
            'niqry', 'nirep', 'mtraceresp', 'mtrace',
        ],
        description='If protocol is ICMPv6 you can specify the types'
    ),
    divert_to=dict(type='str', required=False, description='Target to divert the traffic to'),
    shaper1=dict(type='str', required=False, description='Traffic Shaper to apply'),
    shaper2=dict(type='str', required=False, description='Traffic Shaper to apply'),
    **STATE_MOD_ARG,
    **RULE_MATCH_FIELDS_ARG,
)
