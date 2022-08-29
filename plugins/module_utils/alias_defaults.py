from ansible_collections.ansibleguy.opnsense.plugins.module_utils.defaults import OPN_MOD_ARGS

ALIAS_DEFAULTS = {
    'state': 'present',
    'enabled': True,
    'description': '',
    'type': 'host',
    'content': [],
    'debug': False,
}

ALIAS_MOD_ARGS = dict(
    name=dict(type='str', required=True),
    description=dict(type='str', required=False, default=ALIAS_DEFAULTS['description']),
    content=dict(type='list', required=False, default=ALIAS_DEFAULTS['content']),
    type=dict(type='str', required=False, choices=[
        'host', 'network', 'port', 'url', 'urltable', 'geoip', 'networkgroup',
        'mac', 'dynipv6host', 'internal', 'external',
    ], default=ALIAS_DEFAULTS['type']),
    state=dict(type='str', default=ALIAS_DEFAULTS['state'], required=False, choices=['present', 'absent']),
    enabled=dict(type='bool', required=False, default=ALIAS_DEFAULTS['enabled']),
    # todo: updatefreq not yet working (used by 'urltable')
    # updatefreq_days=dict(type='int', required=False),
    **OPN_MOD_ARGS
)
