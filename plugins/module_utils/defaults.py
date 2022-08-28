OPN_MOD_ARGS = dict(
    firewall=dict(type='str', required=True),
    api_port=dict(type=int, required=False, default=443),
    api_key=dict(type='str', required=False),
    api_secret=dict(type='str', required=False, no_log=True),
    api_credential_file=dict(type='str', required=False),
    ssl_verify=dict(type='bool', required=False, default=True),
    ssl_ca_file=dict(type='str', required=False),
    debug=dict(type='bool', required=False, default=False),
)
