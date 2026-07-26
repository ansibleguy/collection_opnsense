from ansible_collections.oxlorg.opnsense.plugins.module_utils.defaults.main import \
    STATE_MOD_ARG


ALIAS_MOD_ARGS = dict(
    name=dict(type='str', required=True, aliases=['n']),
    description=dict(
        type='str', required=False, default='', aliases=['desc'],
    ),
    content=dict(
        type='list', required=False, default=[], aliases=['c', 'cont'], elements='str',
    ),
    type=dict(type='str', required=False, default='host', aliases=['t'], choices=[
        'host', 'network', 'port', 'url', 'urltable', 'geoip', 'networkgroup',
        'mac', 'dynipv6host', 'internal', 'external', 'urljson',
    ]),
    updatefreq_days=dict(
        type='str', default='', required=False,
        description="Update frequency used by type 'urltable' or 'urljson' in days - per example '0.5' for 12 hours"
    ),
    interface=dict(
        type='str', default=None, aliases=['int', 'if'], required=False,
        description=' Select the interface for the V6 dynamic IP.',
    ),
    path_expression=dict(
        type='str', default='', aliases=['pe', 'jq'], required=False,
        description='Simplified expression to select a field inside a container, a dot is used as field separator. '
                    'Expressions using the jq language are also supported.',
    ),
    statistics=dict(
        type='bool', default=False, required=False,
    ),
    url_auth_type=dict(type='str', required=False, default='', aliases=['auth_type'], choices=[
        '', 'Basic', 'Bearer', 'Header',
    ]),
    url_username=dict(type='str', required=False, default='', aliases=['username']),
    url_password=dict(type='str', required=False, default='', aliases=['password'], no_log=True),
    **STATE_MOD_ARG,
)
