from ansible_collections.ansibleguy.opnsense.plugins.module_utils.defaults import OPN_MOD_ARGS

ALIAS_DEFAULTS = {
    'state': 'present',
    'enabled': True,
    'description': '',
    'type': 'host',
    'content': [],
    'debug': False,
}

ALIAS_MOD_ARG_ALIASES = {
    'name': ['n'],
    'content': ['c', 'cont'],
    'type': ['t'],
    'description': ['desc'],
    'state': ['st'],
    'enabled': ['en'],
}

ALIAS_MOD_ARGS = dict(
    name=dict(type='str', required=True, aliases=ALIAS_MOD_ARG_ALIASES['name']),
    description=dict(
        type='str', required=False, default=ALIAS_DEFAULTS['description'],
        aliases=ALIAS_MOD_ARG_ALIASES['description']
    ),
    content=dict(
        type='list', required=False, default=ALIAS_DEFAULTS['content'],
        aliases=ALIAS_MOD_ARG_ALIASES['content']
    ),
    type=dict(type='str', required=False, choices=[
        'host', 'network', 'port', 'url', 'urltable', 'geoip', 'networkgroup',
        'mac', 'dynipv6host', 'internal', 'external',
    ], default=ALIAS_DEFAULTS['type'], aliases=ALIAS_MOD_ARG_ALIASES['type']),
    state=dict(
        type='str', default=ALIAS_DEFAULTS['state'], required=False,
        choices=['present', 'absent'], aliases=ALIAS_MOD_ARG_ALIASES['state']
    ),
    enabled=dict(
        type='bool', required=False, default=ALIAS_DEFAULTS['enabled'],
        aliases=ALIAS_MOD_ARG_ALIASES['enabled']
    ),
    # todo: updatefreq not yet working (used by 'urltable')
    # updatefreq_days=dict(type='int', required=False),
    **OPN_MOD_ARGS
)
