OPENVPN_INSTANCE_MOD_ARGS = dict(
    name=dict(
        type='str', required=True, aliases=['desc', 'description'],
        description='The name used to match this config to existing entries'
    ),
    protocol=dict(
        type='str', required=False, default='udp', aliases=['proto'],
        choices=['udp', 'udp4', 'udp6', 'tcp', 'tcp4', 'tcp6'],
        description='Use protocol for communicating with remote host.'
    ),
    address=dict(
        type='str', required=False, default='', aliases=['bind_address', 'ip', 'bind'],
        description='Optional IP address for bind.'
                    'If specified, OpenVPN will bind to this address only.'
                    'If unspecified, OpenVPN will bind to all interfaces.'
    ),
    mode=dict(
        type='str', required=False, default='tun', aliases=['type'], choices=['tun', 'tap'],
        description='Choose the type of tunnel, OSI Layer 3 [tun] is the most common option '
                    'to route IPv4 or IPv6 traffic, [tap] offers Ethernet 802.3 (OSI Layer 2) connectivity '
                    'between hosts and is usually combined with a bridge.'
    ),
    log_level=dict(
        type='int', required=False, default=3, aliases=['verbosity', 'verb'],
        choices=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
        description='Output verbosity level. 0 = no output, 1-4 = normal, 5 = log packets, 6-11 debug'
    ),
    keepalive_interval=dict(
        type='str', required=False, default='', aliases=['kai'],
        description='Ping interval in seconds. 0 to disable keep alive'
    ),
    keepalive_timeout=dict(
        type='str', required=False, default='', aliases=['kat'],
        description='Causes OpenVPN to restart after n seconds pass without reception of a '
                    'ping or other packet from remote.'
    ),
    # trust
    certificate=dict(
        type='str', required=False, aliases=['cert'],
        description='Certificate to use for this service.'
    ),
    ca=dict(
        type='str', required=False, default='', aliases=['certificate_authority', 'authority'],
        description='Select a certificate authority when it differs from the attached certificate.'
    ),
    key=dict(
        type='str', required=False, default='', aliases=['tls_key', 'tls_static_key'],
        description='Add an additional layer of HMAC authentication on top of the TLS control channel to '
                    'mitigate DoS attacks and attacks on the TLS stack. The prefixed mode determines if '
                    'this measurement is only used for authentication (--tls-auth) or includes encryption '
                    '(--tls-crypt).'
    ),
    authentication=dict(
        type='str', required=False, default='', aliases=['auth', 'auth_algo'],
        choices=[
            '', 'BLAKE2b512', 'BLAKE2s256', 'whirlpool', 'none',
            'MD4', 'MD5', 'MD5-SHA1', 'RIPEMD160', 'SHA1', 'SHA224', 'SHA256', 'SHA3-224', 'SHA3-256',
            'SHA3-384', 'SHA3-512', 'SHA384', 'SHA512', 'SHA512-224', 'SHA512-256', 'SHAKE128', 'SHAKE256',
        ],
        description='Authenticate data channel packets and (if enabled) tls-auth control channel packets with '
                    'HMAC using message digest algorithm alg.'
    ),
    # auth
    renegotiate_time=dict(
        type='str', required=False, default='', aliases=['reneg_time', 'reneg'],
        description='Renegotiate data channel key after n seconds (default=3600). When using a one time '
                    'password, be advised that your connection will automatically drop because your '
                    'password is not valid anymore. Set to 0 to disable, remember to change your '
                    'client as well.'
    ),
    # routing
    network_local=dict(
        type='list', elements='str', required=False, default=[], aliases=['net_local', 'push_route'],
        description='These are the networks accessible on this host, these are pushed via route{-ipv6} '
                    'clauses in OpenVPN to the client.'
    ),
    network_remote=dict(
        type='list', elements='str', required=False, default=[], aliases=['net_remote', 'route'],
        description='Remote networks for the server, add route to routing table after connection is established'
    ),
    # misc
    options=dict(
        type='list', elements='str', required=False, default=[], aliases=['opts'],
        description='Various less frequently used yes/no options which can be set for this instance.',
        choices=[
            'client-to-client', 'duplicate-cn', 'passtos', 'persist-remote-ip', 'route-nopull', 'route-noexec',
            'remote-random',
        ],
    ),
    mtu=dict(
        type='str', required=False, default='', aliases=['tun_mtu'],
        description='Take the TUN device MTU to be tun-mtu and derive the link MTU from it.'
    ),
    fragment_size=dict(
        type='str', required=False, default='', aliases=['frag_size'],
        description='Enable internal datagram fragmentation so that no UDP datagrams are sent which are larger '
                    'than the specified byte size.'
    ),
    mss_fix=dict(
        type='bool', required=False, default=False, aliases=['mss'],
        description='Announce to TCP sessions running over the tunnel that they should limit their send packet '
                    'sizes such that after OpenVPN has encapsulated them, the resulting UDP packet size that '
                    'OpenVPN sends to its peer will not exceed the recommended size.'
    ),
)
