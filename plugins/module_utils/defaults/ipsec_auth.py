IPSEC_AUTH_MOD_ARGS = dict(
    description=dict(
        type='str', required=True, aliases=['name'],
        description='Unique name to identify the entry'
    ),
    connection=dict(
        type='str', required=False, aliases=['tunnel', 'conn', 'tun'],
        description='Connection to use this local authentication with'
    ),
    round=dict(
        type='int', required=False, default=0,
        description=''
    ),
    authentication=dict(
        type='str', required=False, aliases=['auth'], default='psk',
        choices=['psk', 'pubkey', 'eap_tls', 'eap_mschapv2', 'xauth_pam', 'eap_radius'],
        description='',
    ),
    id=dict(
        type='str', required=False,
        description=''
    ),
    eap_id=dict(
        type='str', required=False,
        description=''
    ),
    certificates=dict(
        type='list', elements='str', required=False, aliases=['certs'], default=[],
        description='Peer certificates that are allowed to connect'
    ),
    public_keys=dict(
        type='list', elements='str', required=False, aliases=['pubkeys'], default=[],
        description='Peer public-keys that are allowed to connect'
    ),
)
