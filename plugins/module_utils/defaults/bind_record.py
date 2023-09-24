from ansible_collections.ansibleguy.opnsense.plugins.module_utils.defaults.main import \
    OPN_MOD_ARGS, STATE_MOD_ARG, RELOAD_MOD_ARG

RECORD_DEFAULTS = {
    'type': 'A',
    'value': None,
    'round_robin': False,
}

RECORD_MOD_ARG_ALIASES = {
    'domain': ['domain_name'],
    'name': ['record'],
}

RECORD_MATCH_FIELDS_ARG = dict(
    match_fields=dict(
        type='list', required=False, elements='str',
        description='Fields that are used to match configured records with the running config - '
                    "if any of those fields are changed, the module will think it's a new entry",
        choices=['domain', 'name', 'type', 'value'],
        default=['domain', 'name', 'type'],
    ),
)

RECORD_MOD_ARGS = dict(
    domain=dict(type='str', required=True, aliases=RECORD_MOD_ARG_ALIASES['domain']),
    name=dict(type='str', required=True, aliases=RECORD_MOD_ARG_ALIASES['name']),
    type=dict(
        type='str', required=False, default=RECORD_DEFAULTS['type'],
        choices=[
            'A', 'AAAA', 'CAA', 'CNAME', 'DNSKEY', 'DS', 'MX', 'NS', 'PTR',
            'RRSIG', 'SRV', 'TLSA', 'TXT',
        ]
    ),
    value=dict(type='str', required=False),
    round_robin=dict(
        type='bool', required=False, default=RECORD_DEFAULTS['round_robin'],
        description='If multiple records with the same domain/name/type combination exist - '
                    "the module will only execute 'state=absent' if set to 'false'. "
                    "To create multiple ones set this to 'true'. "
                    "Records will only be created, NOT UPDATED! (no matching is done)"
    ),
    **STATE_MOD_ARG,
    **RECORD_MATCH_FIELDS_ARG,
    **RELOAD_MOD_ARG,
    **OPN_MOD_ARGS,
)
