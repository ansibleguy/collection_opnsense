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

.. include:: ../_include/param_basic.rst

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
    "carp_depend_on","string","false","\-","vip, vip_depend, carp, carp_depend","The CARP VHID to depend on. When this virtual address is not in master state, then the instance will be shutdown."
    "certificate","string","true if no ca","\-","cert","Certificate to use for this service."
    "ca","string","false","true if no certificate","certificate_authority, authority","Select a certificate authority when it differs from the attached certificate."
    "key","string","false","\-","tls_key, tls_static_key","Add an additional layer of HMAC authentication on top of the TLS control channel to mitigate DoS attacks and attacks on the TLS stack. The prefixed mode determines if this measurement is only used for authentication (--tls-auth) or includes encryption (--tls-crypt)."
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

ansibleguy.opnsense.openvpn_static_key
======================================

..  csv-table:: Definition
    :header: "Parameter", "Type", "Required", "Default", "Aliases", "Comment"
    :widths: 15 10 10 10 10 45

    "name","string","true","\-","description, desc","The name used to match this config to existing entries"
    "mode","string","false","tun","type","Define the use of this key, authentication (--tls-auth) or authentication and encryption (--tls-crypt)"
    "key","string","false","\-","\-","OpenVPN Static key. If empty - it will be auto-generated."



Usage
*****

The instance description/name is used to match your config to the existing entries.

----

Examples
********

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
            # protocol: 'udp'
            # port: ''
            # address: ''
            # mode: 'tun'
            # log_level: 3
            # keepalive_interval: ''
            # keepalive_timeout: ''
            # carp_depend_on: ''
            # certificate: ''
            # ca: ''
            # tls_key: ''
            # authentication: ''
            # username: ''
            # password: ''
            # renegotiate_time: ''
            # network_local: []
            # network_remote: []
            # options: []
            # mtu: ''
            # fragment_size: ''
            # mss_fix: ''
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
            key: '#\n# 2048 bit OpenVPN static key\n#\n-----BEGIN OpenVPN Static key V1-----\n
              c07e43dc02829f88184b4fb74243e4ac\nb1d24d1d1a74cd21df8ac64a527915ae\n9c736c0c219eb33774e40e61f6f660c8\n
              daf44730850fae665f5f609a71e99f3c\n8a636b16dff7434ce3b7f9aca896287b\nd6c62d2f6d7db4e9cfcfe0f101cc6474\n
              0c98246fbcd203891a0343777c7551c7\naa2ba1e6a6ab4fcf593a894d4da8f180\nd44645b5a658e17f5d48408a020430c3\n
              5b768f413a2ec69ead015750cacb53d7\n64a19bce04b29f11d3ca7560a99958b6\n9203f493fd7e740b5a5a3d1afe1b4185\n
              50043805c5bac513baf2306e42c1c1f8\n0fd16661536a3ee72ffbd1d2d1b1f6c0\n9683064c9bc044ee0357f4b94f5687ed\n
              67cb013625cfb9b113ecff16674d63e6\n-----END OpenVPN Static key V1-----'

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
