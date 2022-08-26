ALIAS_DEFAULTS = {
    'state': 'present',
    'enabled': True,
    'description': '',
    'type': 'host',
    'content': [],
}

ALIAS_MOD_ARGS = dict(
    firewall=dict(type='str', required=True),
    name=dict(type='str', required=True),
    description=dict(type='str', required=False, default=ALIAS_DEFAULTS['description']),
    content=dict(type='list', required=False, default=ALIAS_DEFAULTS['content']),
    type=dict(type='str', required=False, choices=[
        'host', 'network', 'port', 'url', 'urltable', 'geoip', 'networkgroup',
        'mac', 'dynipv6host', 'internal', 'external',
    ], default=ALIAS_DEFAULTS['type']),
    state=dict(type='str', default=ALIAS_DEFAULTS['state'], required=False, choices=['present', 'absent']),
    enabled=dict(type='bool', required=False, default=ALIAS_DEFAULTS['enabled']),
    api_key=dict(type='str', required=False),
    api_secret=dict(type='str', required=False, no_log=True),
    api_credential_file=dict(type='str', required=False),
    ssl_verify=dict(type='bool', required=False, default=True),
    ssl_ca_file=dict(type='str', required=False),
    debug=dict(type='bool', required=False, default=False),
    # todo: updatefreq not yet working (used by 'urltable')
    # updatefreq_days=dict(type='int', required=False),
)
