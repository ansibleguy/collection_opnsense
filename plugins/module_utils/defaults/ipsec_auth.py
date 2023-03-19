IPSEC_AUTH_MOD_ARGS = dict(
    name=dict(
        type='str', required=True, aliases=['description', 'desc'],
        description='Unique name to identify the entry'
    ),
    connection=dict(
        type='str', required=False, aliases=['tunnel', 'conn', 'tun'],
        description='Connection to use this local authentication with'
    ),
    round=dict(
        type='int', required=False, default=0,
        description='Numeric identifier by which authentication rounds are sorted'
    ),
    authentication=dict(
        type='str', required=False, aliases=['auth'], default='psk',
        choices=['psk', 'pubkey', 'eap_tls', 'eap_mschapv2', 'xauth_pam', 'eap_radius'],
        description='Authentication to perform for this round, when using Pre-Shared key make sure to define one '
                    'under "VPN->IPsec->Pre-Shared Keys"',
    ),
    id=dict(
        type='str', required=False, aliases=['ike_id'],
        description='IKE identity to use for authentication round. When using certificate authentication. The IKE '
                    'identity must be contained in the certificate, either as the subject DN or as a subjectAltName '
                    '(the identity will default to the certificate’s subject DN if not specified). '
                    'Refer to https://docs.strongswan.org/docs/5.9/config/identityParsing.html for details on '
                    'how identities are parsed and may be configured'
    ),
    eap_id=dict(
        type='str', required=False,
        description='Client EAP-Identity to use in EAP-Identity exchange and the EAP method'
    ),
    certificates=dict(
        type='list', elements='str', required=False, aliases=['certs'], default=[],
        description='List of certificate candidates to use for authentication'
    ),
    public_keys=dict(
        type='list', elements='str', required=False, aliases=['pubkeys'], default=[],
        description='List of raw public key candidates to use for authentication'
    ),
)
