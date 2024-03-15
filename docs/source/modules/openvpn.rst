.. _modules_openvpn:

.. include:: ../_include/head.rst

=======
OpenVPN
=======

**STATE**: testing

**TESTS**: `ansibleguy.opnsense.openvpn_client <https://github.com/ansibleguy/collection_opnsense/blob/latest/tests/openvpn_client.yml>`_ |
`ansibleguy.opnsense.openvpn_server <https://github.com/ansibleguy/collection_opnsense/blob/latest/tests/openvpn_server.yml>`_ |
`ansibleguy.opnsense.openvpn_static_key <https://github.com/ansibleguy/collection_opnsense/blob/latest/tests/openvpn_static_key.yml>`_ |
`ansibleguy.opnsense.openvpn_status <https://github.com/ansibleguy/collection_opnsense/blob/latest/tests/openvpn_status.yml>`_

**API Docs**: `OpenVPN <https://docs.opnsense.org/development/api/core/openvpn.html>`_

**Service Docs**: `OpenVPN <https://docs.opnsense.org/troubleshooting/openvpn.html>`_

Info
****

You can use the :ref:`ansibleguy.opnsense.service <modules_service>` module to interact with the OpenVPN service.

----

Definition
**********

.. include:: ../_include/param_basic.rst

ansibleguy.opnsense.openvpn_server
==================================

..  csv-table:: Definition
    :header: "Parameter", "Type", "Required", "Default", "Aliases", "Comment"
    :widths: 15 10 10 10 10 45

    "name","string","true","\-","description, desc","The name used to match this config to existing entries"
    "server_ip4","string","true if no server_ip6","\-","server, client_net_ip4","This directive will set up an OpenVPN server which will allocate addresses to clients out of the given network/netmask. The server itself will take the .1 address of the given network for use as the server-side endpoint of the local TUN/TAP interface"
    "server_ip6","string","true if no server_ip4","\-","server6, client_net_ip6","This directive will set up an OpenVPN server which will allocate addresses to clients out of the given network/netmask. The server itself will take the next base address (+1) of the given network for use as the server-side endpoint of the local TUN/TAP interface"
    "protocol","string","false","udp","proto","One of: 'udp', 'udp4', 'udp6', 'tcp', 'tcp4', 'tcp6'. Use protocol for communicating with remote host."
    "port","integer","false","1194","local_port, bind_port","Port number to use"
    "address","string","false","\-","bind_address, bind, ip","Optional IP address for bind. If specified, OpenVPN will bind to this address only. If unspecified, OpenVPN will bind to all interfaces."
    "mode","string","false","tun","type","One of: 'tun', 'tap'. Choose the type of tunnel, OSI Layer 3 [tun] is the most common option to route IPv4 or IPv6 traffic, [tap] offers Ethernet 802.3 (OSI Layer 2) connectivity between hosts and is usually combined with a bridge."
    "topology","string","false","subnet","topo","One of: 'net30', 'p2p', 'subnet'. Configure virtual addressing topology when running in --dev tun mode. This directive has no meaning in --dev tap mode, which always uses a subnet topology."
    "max_connections","integer","false","\-","max_conn, max_clients","Specify the maximum number of clients allowed to concurrently connect to this server."
    "log_level","integer","false","\-","verbosity, verb","From 0 to 11. Output verbosity level. 0 = no output, 1-4 = normal, 5 = log packets, 6-11 debug"
    "keepalive_interval","integer","false","\-","kai","Ping interval in seconds. 0 to disable keep alive"
    "keepalive_timeout","integer","false","\-","kat","Causes OpenVPN to restart after n seconds pass without reception of a ping or other packet from remote."
    "renegotiate_time","integer","false","\-","reneg_time, reneg","Renegotiate data channel key after n seconds (default=3600). When using a one time password, be advised that your connection will automatically drop because your password is not valid anymore. Set to 0 to disable, remember to change your client as well."
    "auth_token_time","integer","false","\-","auth_time, token_time","After successful user/password authentication, the OpenVPN server will with this option generate a temporary authentication token and push that to the client. On the following renegotiations, the OpenVPN client will pass this token instead of the users password. On the server side the server will do the token authentication internally and it will NOT do any additional authentications against configured external user/password authentication mechanisms. When set to 0, the token will never expire, any other value specifies the lifetime in seconds."
    "certificate","string","true if no ca","\-","cert","Certificate to use for this service."
    "ca","string","false","true if no certificate","certificate_authority, authority","Select a certificate authority when it differs from the attached certificate."
    "crl","string","false","false","certificate_revocation_list, revocation_list","Select a certificate revocation list to use for this service."
    "key","string","false","\-","tls_key, tls_static_key","Add an additional layer of HMAC authentication on top of the TLS control channel to mitigate DoS attacks and attacks on the TLS stack. The prefixed mode determines if this measurement is only used for authentication (--tls-auth) or includes encryption (--tls-crypt)."
    "authentication","string","false","\-","auth, auth_algo","One of: 'BLAKE2b512', 'BLAKE2s256', 'whirlpool', 'none', 'MD4', 'MD5', 'MD5-SHA1', 'RIPEMD160', 'SHA1', 'SHA224', 'SHA256', 'SHA3-224', 'SHA3-256', 'SHA3-384', 'SHA3-512', 'SHA384', 'SHA512', 'SHA512-224', 'SHA512-256', 'SHAKE128', 'SHAKE256'. Authenticate data channel packets and (if enabled) tls-auth control channel packets with HMAC using message digest algorithm alg."
    "network_local","list","false","\-","local, net_local, push_route","These are the networks accessible on this host, these are pushed via route{-ipv6} clauses in OpenVPN to the client"
    "network_remote","list","false","\-","remote, net_remote, route","Remote networks for the server, add route to routing table after connection is established"
    "data_ciphers","list","false","\-","ciphers","One or multiple of: 'AES-256-GCM', 'AES-128-GCM', 'CHACHA20-POLY1305'. Restrict the allowed ciphers to be negotiated to the ciphers in this list."
    "data_cipher_fallback","string","false","\-","cipher_fallback","One of: 'AES-256-GCM', 'AES-128-GCM', 'CHACHA20-POLY1305'. Configure a cipher that is used to fall back to if we could not determine which cipher the peer is willing to use. This option should only be needed to connect to peers that are running OpenVPN 2.3 or older versions, and have been configured with --enable-small (typically used on routers or other embedded devices)."
    "auth_mode","list","false","\-","authentication_mode, auth_source","Select authentication methods to use, leave empty if no challenge response authentication is needed."
    "auth_group","string","false","\-","group","Restrict access to users in the selected local group. Please be aware that other authentication backends will refuse to authenticate when using this option."
    "options","list","false","\-","opts","One or multiple of: 'client-to-client', 'duplicate-cn', 'passtos', 'persist-remote-ip', 'route-nopull', 'route-noexec', 'remote-random'. Various less frequently used yes/no options which can be set for this instance."
    "push_options","list","false","\-","push_opts","One or multiple of: 'block-outside-dns', 'register-dns'. Various less frequently used yes/no options which can be pushed to the client for this instance."
    "redirect_gateway","list","false","\-","push_opts","One or multiple of: 'local', 'autolocal', 'def1', 'bypass_dhcp', 'bypass_dns', 'block_local', 'ipv6', 'notipv4'. Automatically execute routing commands to cause all outgoing IP traffic to be redirected over the VPN."
    "domain","string","false","\-","dns_domain","Set Connection-specific DNS Suffix."
    "domain_list","list","false","\-","dns_domain_search","Add name to the domain search list. Repeat this option to add more entries. Up to 10 domains are supported"
    "dns_servers","list","false","\-","dns","Set primary domain name server IPv4 or IPv6 address. Repeat this option to set secondary DNS server addresses."
    "ntp_servers","list","false","\-","ntp","Set primary NTP server address (Network Time Protocol). Repeat this option to set secondary NTP server addresses."
    "mtu","integer","false","\-","tun_mtu","Take the TUN device MTU to be tun-mtu and derive the link MTU from it."
    "route_metric","integer","false","\-","metric, push_metric","Specify a default metric m for use with --route on the connecting client (push option)."
    "fragment_size","string","false","\-","frag_size","Enable internal datagram fragmentation so that no UDP datagrams are sent which are larger than the specified byte size."
    "verify_client_cert","string","false","require","verify_client, verify_cert","One of: 'require', 'none'. Specify if the client is required to offer a certificate."
    "cert_depth","integer","false","\-","certificate_depth","From 1 to 5. When a certificate-based client logs in, do not accept certificates below this depth. Useful for denying certificates made with intermediate CAs generated from the same CA as the server."
    "register_dns","boolean","false","false","\-","Run ipconfig /flushdns and ipconfig /registerdns on connection initiation. This is known to kick Windows into recognizing pushed DNS servers."
    "ocsp","boolean","false","false","use_ocsp, verify_ocsp","When the CA used supplies an authorityInfoAccess OCSP URI extension, it will be used to validate the client certificate."
    "user_as_cn","boolean","false","false","username_as_cn","Use the authenticated username as the common-name, rather than the common-name from the client certificate."
    "user_cn_strict","boolean","false","false","username_cn_strict","When authenticating users, enforce a match between the Common Name of the client certificate and the username given at login."
    "mss_fix","boolean","false","false","mss","Announce to TCP sessions running over the tunnel that they should limit their send packet sizes such that after OpenVPN has encapsulated them, the resulting UDP packet size that OpenVPN sends to its peer will not exceed the recommended size."
    "reload","boolean","false","true","\-", .. include:: ../_include/param_reload.rst

ansibleguy.opnsense.openvpn_client
==================================

..  csv-table:: Definition
    :header: "Parameter", "Type", "Required", "Default", "Aliases", "Comment"
    :widths: 15 10 10 10 10 45

    "name","string","true","\-","description, desc","The name used to match this config to existing entries"
    "remote","list","true","\-","peer, server","Remote host name or IP address with optional port"
    "protocol","string","false","udp","proto","One of: 'udp', 'udp4', 'udp6', 'tcp', 'tcp4', 'tcp6'. Use protocol for communicating with remote host."
    "port","integer","false","\-","local_port, bind_port","Port number to use. Specifies a bind address, or nobind when client does not have a specific bind address."
    "address","string","false","\-","bind_address, bind, ip","Optional IP address for bind. If specified, OpenVPN will bind to this address only. If unspecified, OpenVPN will bind to all interfaces."
    "mode","string","false","tun","type","One of: 'tun', 'tap'. Choose the type of tunnel, OSI Layer 3 [tun] is the most common option to route IPv4 or IPv6 traffic, [tap] offers Ethernet 802.3 (OSI Layer 2) connectivity between hosts and is usually combined with a bridge."
    "log_level","integer","false","\-","verbosity, verb","From 0 to 11. Output verbosity level. 0 = no output, 1-4 = normal, 5 = log packets, 6-11 debug"
    "keepalive_interval","integer","false","\-","kai","Ping interval in seconds. 0 to disable keep alive"
    "keepalive_timeout","integer","false","\-","kat","Causes OpenVPN to restart after n seconds pass without reception of a ping or other packet from remote."
    "renegotiate_time","integer","false","\-","reneg_time, reneg","Renegotiate data channel key after n seconds (default=3600). When using a one time password, be advised that your connection will automatically drop because your password is not valid anymore. Set to 0 to disable, remember to change your client as well."
    "carp_depend_on","string","false","\-","vip, vip_depend, carp, carp_depend","The CARP VHID to depend on. When this virtual address is not in master state, then the instance will be shutdown."
    "certificate","string","true if no ca","\-","cert","Certificate to use for this service."
    "ca","string","false","true if no certificate","certificate_authority, authority","Select a certificate authority when it differs from the attached certificate."
    "key","string","false","\-","tls_key, tls_static_key","Add an additional layer of HMAC authentication on top of the TLS control channel to mitigate DoS attacks and attacks on the TLS stack. The prefixed mode determines if this measurement is only used for authentication (--tls-auth) or includes encryption (--tls-crypt)."
    "authentication","string","false","\-","auth, auth_algo","One of: 'BLAKE2b512', 'BLAKE2s256', 'whirlpool', 'none', 'MD4', 'MD5', 'MD5-SHA1', 'RIPEMD160', 'SHA1', 'SHA224', 'SHA256', 'SHA3-224', 'SHA3-256', 'SHA3-384', 'SHA3-512', 'SHA384', 'SHA512', 'SHA512-224', 'SHA512-256', 'SHAKE128', 'SHAKE256'. Authenticate data channel packets and (if enabled) tls-auth control channel packets with HMAC using message digest algorithm alg."
    "username","string","false","\-","user","(optional) Username to send to the server for authentication when required."
    "password","string","false","\-","pwd","Password belonging to the user specified above"
    "network_local","list","false","\-","local, net_local, push_route","These are the networks accessible on this host, these are pushed via route{-ipv6} clauses in OpenVPN to the client"
    "network_remote","list","false","\-","remote, net_remote, route","Remote networks for the server, add route to routing table after connection is established"
    "options","list","false","\-","opts","One or multiple of: 'client-to-client', 'duplicate-cn', 'passtos', 'persist-remote-ip', 'route-nopull', 'route-noexec', 'remote-random'. Various less frequently used yes/no options which can be set for this instance."
    "mtu","integer","false","\-","tun_mtu","Take the TUN device MTU to be tun-mtu and derive the link MTU from it."
    "fragment_size","string","false","\-","frag_size","Enable internal datagram fragmentation so that no UDP datagrams are sent which are larger than the specified byte size."
    "mss_fix","boolean","false","false","mss","Announce to TCP sessions running over the tunnel that they should limit their send packet sizes such that after OpenVPN has encapsulated them, the resulting UDP packet size that OpenVPN sends to its peer will not exceed the recommended size."
    "reload","boolean","false","true","\-", .. include:: ../_include/param_reload.rst

ansibleguy.opnsense.openvpn_static_key
======================================

..  csv-table:: Definition
    :header: "Parameter", "Type", "Required", "Default", "Aliases", "Comment"
    :widths: 15 10 10 10 10 45

    "name","string","true","\-","description, desc","The name used to match this config to existing entries"
    "mode","string","false","crypt","type","One of: 'auth', 'crypt'. Define the use of this key, authentication (--tls-auth) or authentication and encryption (--tls-crypt)"
    "key","string","false","\-","\-","OpenVPN Static key. If empty - it will be auto-generated."

ansibleguy.opnsense.openvpn_status
==================================

..  csv-table:: Definition
    :header: "Parameter", "Type", "Required", "Default", "Aliases", "Comment"
    :widths: 15 10 10 10 10 45

    "target","string","false","sessions","kind","One of: 'sessions', 'routes'. What information to query"


----

Usage
*****

The instance description/name is used to match your config to the existing entries.

**WARNING**: The openvpn_server and openvpn_client module share the same namespace! Be aware that you p.e. CANNOT create an openvpn_server with the same name as an existing openvpn_client (*on the same box*)!

Use can create an manage certificates `using the OPNSense WebUI <https://docs.opnsense.org/manual/how-tos/self-signed-chain.html>`_!

----

Examples
********

ansibleguy.opnsense.openvpn_server
==================================

.. code-block:: yaml

    - hosts: localhost
      gather_facts: no
      module_defaults:
        group/ansibleguy.opnsense.all:
          firewall: 'opnsense.template.ansibleguy.net'
          api_credential_file: '/home/guy/.secret/opn.key'

        ansibleguy.opnsense.list:
          target: 'openvpn_instance'

      tasks:
        - name: Example
          ansibleguy.opnsense.openvpn_server:
            name: 'example'
            server_ip4: ''
            server_ip6: ''
            certificate: ''
            # topology: 'subnet'
            # protocol: 'udp'
            # port: ''
            # address: ''
            # mode: 'tun'
            # max_connections: ''
            # ca: ''
            # crl: ''
            # verify_client_cert: 'require'
            # cert_depth: ''
            # data_ciphers: []
            # data_cipher_fallback: ''
            # ocsp: false
            # log_level: 3
            # keepalive_interval: ''
            # keepalive_timeout: ''
            # key: ''
            # authentication: ''
            # auth_mode: []
            # auth_group: ''
            # renegotiate_time: ''
            # auth_token_time: ''
            # network_local: []
            # network_remote: []
            # options: []
            # push_options: []
            # redirect_gateway: []
            # route_metric: ''
            # mtu: ''
            # fragment_size: ''
            # domain: ''
            # domain_list: []
            # dns_servers: []
            # ntp_servers: []
            # register_dns: false
            # user_as_cn: false
            # user_cn_strict: false
            # mss_fix: false
            # reload: true
            # enabled: true

        - name: Adding
          ansibleguy.opnsense.openvpn_server:
            name: 'ANSIBLE_TEST_1_1'
            port: 20000
            protocol: 'udp'
            mode: 'tun'
            server: '192.168.77.0/29'
            network_local: ['192.168.78.128/27']
            ca: 'OpenVPN'
            certificate: 'OpenVPN Server'

        - name: Changing
          ansibleguy.opnsense.openvpn_server:
            name: 'ANSIBLE_TEST_1_1'
            port: 20000
            protocol: 'udp'
            mode: 'tun'
            server: '192.168.77.0/29'
            network_local: ['192.168.78.128/27']
            ca: 'OpenVPN'
            certificate: 'OpenVPN Server'
            cert_depth: 1
            data_ciphers: ['AES-256-GCM', 'CHACHA20-POLY1305']
            max_connections: 100
            user_as_cn: true
            user_cn_strict: true
            push_options: ['block-outside-dns', 'register-dns']
            mtu: 1420

        - name: Disabling
          ansibleguy.opnsense.openvpn_server:
            name: 'ANSIBLE_TEST_1_1'
            port: 20000
            protocol: 'udp'
            mode: 'tun'
            server: '192.168.77.0/29'
            network_local: ['192.168.78.128/27']
            ca: 'OpenVPN'
            certificate: 'OpenVPN Server'
            cert_depth: 1
            data_ciphers: ['AES-256-GCM', 'CHACHA20-POLY1305']
            max_connections: 100
            user_as_cn: true
            user_cn_strict: true
            push_options: ['block-outside-dns', 'register-dns']
            mtu: 1420
            enabled: false

        - name: Listing
          ansibleguy.opnsense.list:
            # target: 'openvpn_instance'
          register: existing_entries

        - name: Printing tests
          ansible.builtin.debug:
            var: existing_entries.data

        - name: Removing
          ansibleguy.opnsense.openvpn_server:
            name: 'test1'
            state: 'absent'

----

ansibleguy.opnsense.openvpn_client
==================================

.. code-block:: yaml

    - hosts: localhost
      gather_facts: no
      module_defaults:
        group/ansibleguy.opnsense.all:
          firewall: 'opnsense.template.ansibleguy.net'
          api_credential_file: '/home/guy/.secret/opn.key'

        ansibleguy.opnsense.list:
          target: 'openvpn_instance'

      tasks:
        - name: Example
          ansibleguy.opnsense.openvpn_client:
            name: 'example'
            remote: 'example.ovpn.ansibleguy.net:10000'
            certificate: ''
            # ca: ''
            # protocol: 'udp'
            # port: ''
            # address: ''
            # mode: 'tun'
            # log_level: 3
            # keepalive_interval: ''
            # keepalive_timeout: ''
            # carp_depend_on: ''
            # key: ''
            # authentication: ''
            # username: ''
            # password: ''
            # renegotiate_time: ''
            # network_local: []
            # network_remote: []
            # options: []
            # mtu: ''
            # fragment_size: ''
            # mss_fix: false
            # reload: true
            # enabled: true

        - name: Adding
          ansibleguy.opnsense.openvpn_client:
            name: 'test1'
            remote: 'openvpn.test.ansibleguy.net:20000'
            protocol: 'udp'
            mode: 'tun'
            network_remote: ['192.168.77.128/27', '192.168.89.64/27']
            log_level: 2
            ca: 'OpenVPN'
            certificate: 'OpenVPN Client'
            mtu: 1400

        - name: Changing
          ansibleguy.opnsense.openvpn_client:
            name: 'test1'
            remote: 'openvpn.test.ansibleguy.net:10000'
            protocol: 'tcp'
            mode: 'tun'
            network_remote: ['192.168.77.0/24']
            log_level: 5
            ca: 'OpenVPN'
            certificate: 'OpenVPN Client'
            mtu: 1400

        - name: Disabling
          ansibleguy.opnsense.openvpn_client:
            name: 'test1'
            remote: 'openvpn.test.ansibleguy.net:10000'
            protocol: 'tcp'
            mode: 'tun'
            network_remote: ['192.168.77.0/24']
            log_level: 5
            ca: 'OpenVPN'
            certificate: 'OpenVPN Client'
            mtu: 1400
            enabled: false

        - name: Listing
          ansibleguy.opnsense.list:
            # target: 'openvpn_instance'
          register: existing_entries

        - name: Printing tests
          ansible.builtin.debug:
            var: existing_entries.data

        - name: Removing
          ansibleguy.opnsense.openvpn_client:
            name: 'test1'
            state: 'absent'

----

ansibleguy.opnsense.openvpn_static_key
======================================

.. code-block:: yaml

    - hosts: localhost
      gather_facts: no
      module_defaults:
        group/ansibleguy.opnsense.all:
          firewall: 'opnsense.template.ansibleguy.net'
          api_credential_file: '/home/guy/.secret/opn.key'

        ansibleguy.opnsense.list:
          target: 'openvpn_static_key'

      tasks:
        - name: Example
          ansibleguy.opnsense.openvpn_static_key:
            name: 'example'
            # mode: 'crypt'
            # key: ''

        - name: Adding
          ansibleguy.opnsense.openvpn_static_key:
            name: 'test1'
            # key: => will be auto-generated

        - name: Changing
          ansibleguy.opnsense.openvpn_static_key:
            name: 'test1'
            key: '#\n# 2048 bit OpenVPN static key\n#\n
              -----BEGIN OpenVPN Static key V1-----\n
              c07e43dc02829f88184b4fb74243e4ac\
              nb1d24d1d1a74cd21df8ac64a527915ae\n
              9c736c0c219eb33774e40e61f6f660c8\n
              daf44730850fae665f5f609a71e99f3c\n
              8a636b16dff7434ce3b7f9aca896287b\n
              d6c62d2f6d7db4e9cfcfe0f101cc6474\n
              0c98246fbcd203891a0343777c7551c7\n
              aa2ba1e6a6ab4fcf593a894d4da8f180\n
              d44645b5a658e17f5d48408a020430c3\n
              5b768f413a2ec69ead015750cacb53d7\n
              64a19bce04b29f11d3ca7560a99958b6\n
              9203f493fd7e740b5a5a3d1afe1b4185\n
              50043805c5bac513baf2306e42c1c1f8\n
              0fd16661536a3ee72ffbd1d2d1b1f6c0\n
              9683064c9bc044ee0357f4b94f5687ed\n
              67cb013625cfb9b113ecff16674d63e6\n
              -----END OpenVPN Static key V1-----'

        - name: Listing
          ansibleguy.opnsense.list:
            # target: 'openvpn_static_key'
          register: existing_entries

        - name: Printing tests
          ansible.builtin.debug:
            var: existing_entries.data

        - name: Removing
          ansibleguy.opnsense.openvpn_static_key:
            name: 'test1'
            state: 'absent'

----

ansibleguy.opnsense.openvpn_status
==================================

.. code-block:: yaml

    - hosts: localhost
      gather_facts: no
      module_defaults:
        group/ansibleguy.opnsense.all:
          firewall: 'opnsense.template.ansibleguy.net'
          api_credential_file: '/home/guy/.secret/opn.key'

      tasks:
        - name: Querying OpenVPN Sessions
          ansibleguy.opnsense.openvpn_status:
            target: 'sessions'
          register: ovpn_sessions

        - name: Printing Sessions
          ansible.builtin.debug:
            var: ovpn_sessions.data

        - name: Querying OpenVPN Routes
          ansibleguy.opnsense.openvpn_status:
            target: 'routes'
          register: ovpn_routes

        - name: Printing Routes
          ansible.builtin.debug:
            var: ovpn_routes.data
