.. _modules_openvpn:

.. include:: ../_include/head.rst

=======
OpenVPN
=======

**STATE**: testing

**TESTS**: `ansibleguy.opnsense.openvpn_client <https://github.com/ansibleguy/collection_opnsense/blob/latest/tests/openvpn_client.yml>`_

**API Docs**: `OpenVPN <https://docs.opnsense.org/development/api/core/openvpn.html>`_

**Service Docs**: `OpenVPN <https://docs.opnsense.org/troubleshooting/openvpn.html>`_


Definition
**********

ansibleguy.opnsense.openvpn_client
==================================

..  csv-table:: Definition
    :header: "Parameter", "Type", "Required", "Default", "Aliases", "Comment"
    :widths: 15 10 10 10 10 45

    "description","string","true","\-","name, desc","The name used to match this config to existing entries"
    "remote","string","true","\-","peer, server","Remote host name or IP address with optional port"
    "protocol","string","false","udp","proto","One of: 'udp', 'udp4', 'udp6', 'tcp', 'tcp4', 'tcp6'. Use protocol for communicating with remote host."
    "port","integer","false","\-","\-","Port number to use. Specifies a bind address, or nobind when client does not have a specific bind address."
    "address","string","false","\-","bind_address, bind, ip","Optional IP address for bind. If specified, OpenVPN will bind to this address only. If unspecified, OpenVPN will bind to all interfaces."
    "mode","string","false","tun","type","One of: 'tun', 'tap'. Choose the type of tunnel, OSI Layer 3 [tun] is the most common option to route IPv4 or IPv6 traffic, [tap] offers Ethernet 802.3 (OSI Layer 2) connectivity between hosts and is usually combined with a bridge."
    "log_level","integer","false","\-","verbosity, verb","From 0 to 11. Output verbosity level. 0 = no output, 1-4 = normal, 5 = log packets, 6-11 debug"
    "keepalive_interval","integer","false","\-","kai","Ping interval in seconds. 0 to disable keep alive"
    "keepalive_timeout","integer","false","\-","kat","Causes OpenVPN to restart after n seconds pass without reception of a ping or other packet from remote."
    "carp_depend_on","string","false","\-","vip, vip_depend, carp, carp_depend","The CARP VHID to depend on. When this virtual address is not in master state, then the instance will be shutdown."
    "certificate","string","true","\-","cert","Certificate to use for this service."
    "ca","string","false","\-","certificate_authority, authority","Select a certificate authority when it differs from the attached certificate."
    "tls_key","string","false","\-","tls_static_key","Add an additional layer of HMAC authentication on top of the TLS control channel to mitigate DoS attacks and attacks on the TLS stack. The prefixed mode determines if this measurement is only used for authentication (--tls-auth) or includes encryption (--tls-crypt)."
    "authentication","string","false","\-","auth, auth_algo","One of: 'BLAKE2b512', 'BLAKE2s256', 'whirlpool', 'none', 'MD4', 'MD5', 'MD5-SHA1', 'RIPEMD160', 'SHA1', 'SHA224', 'SHA256', 'SHA3-224', 'SHA3-256', 'SHA3-384', 'SHA3-512', 'SHA384', 'SHA512', 'SHA512-224', 'SHA512-256', 'SHAKE128', 'SHAKE256'. Authenticate data channel packets and (if enabled) tls-auth control channel packets with HMAC using message digest algorithm alg."
    "username","string","false","\-","user","(optional) Username to send to the server for authentication when required."
    "password","string","false","\-","pwd","Password belonging to the user specified above"
    "renegotiate_time","integer","false","\-","reneg_time, reneg","Renegotiate data channel key after n seconds (default=3600). When using a one time password, be advised that your connection will automatically drop because your password is not valid anymore. Set to 0 to disable, remember to change your client as well."
    "network_local","list","false","\-","local, net_local, push_route","These are the networks accessible on this host, these are pushed via route{-ipv6} clauses in OpenVPN to the client"
    "network_remote","list","false","\-","remote, net_remote, route","Remote networks for the server, add route to routing table after connection is established"
    "options","list","false","\-","opts","One or multiple of: 'client-to-client', 'duplicate-cn', 'passtos', 'persist-remote-ip', 'route-nopull', 'route-noexec', 'remote-random'. Various less frequently used yes/no options which can be set for this instance."
    "mtu","integer","false","\-","tun_mtu","Take the TUN device MTU to be tun-mtu and derive the link MTU from it."
    "fragment_size","string","false","\-","frag_size","Enable internal datagram fragmentation so that no UDP datagrams are sent which are larger than the specified byte size."
    "mss_fix","string","false","\-","mss","Announce to TCP sessions running over the tunnel that they should limit their send packet sizes such that after OpenVPN has encapsulated them, the resulting UDP packet size that OpenVPN sends to its peer will not exceed the recommended size."
    "reload","boolean","false","true","\-", .. include:: ../_include/param_reload.rst

.. include:: ../_include/param_basic.rst

Usage
*****

The instance description/name is used to match your config to the existing entries.

Examples
********

tbd
