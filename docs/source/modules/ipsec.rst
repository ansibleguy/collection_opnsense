.. _modules_ipsec:

.. include:: ../_include/head.rst

=====
IPSec
=====

**STATE**: stable

**TESTS**: `ipsec_cert <https://github.com/ansibleguy/collection_opnsense/blob/stable/tests/ipsec_cert.yml>`_ |
`ipsec_psk <https://github.com/ansibleguy/collection_opnsense/blob/stable/tests/ipsec_psk.yml>`_ |
`ipsec_connection <https://github.com/ansibleguy/collection_opnsense/blob/stable/tests/ipsec_connection.yml>`_ |
`ipsec_pool <https://github.com/ansibleguy/collection_opnsense/blob/stable/tests/ipsec_pool.yml>`_ |
`ipsec_vti <https://github.com/ansibleguy/collection_opnsense/blob/stable/tests/ipsec_vti.yml>`_

**API Docs**: `Core - IPSec <https://docs.opnsense.org/development/api/core/ipsec.html>`_

**Service Docs**: `IPSec <https://docs.opnsense.org/manual/vpnet.html#ipsec>`_ |
`IPSec Examples <https://docs.opnsense.org/manual/vpnet.html#new-23-1-vpn-ipsec-connections>`_ |
`IPSec VTI <https://docs.opnsense.org/manual/how-tos/ipsec-s2s-conn-route.html>`_

Limitations
***********

.. warning::

    The IPSec modules can only be used on OPNSense version >= 23.1


Definition
**********

.. include:: ../_include/param_basic.rst

ansibleguy.opnsense.ipsec_connection
====================================

Module alias: ansibleguy.opnsense.ipsec_tunnel

..  csv-table:: Definition
    :header: "Parameter", "Type", "Required", "Default", "Aliases", "Comment"
    :widths: 15 10 10 10 10 45

    "name","string","true","\-","description, desc","Unique connection/tunnel name"
    "local_addresses","list","false","\-","local_addr, local","Local address[es] to use for IKE communication. Accepts single IPv4/IPv6 addresses, DNS names, CIDR subnets or IP address ranges. As an initiator, the first non-range/non-subnet is used to initiate the connection from. As a responder the local destination address must match at least to one of the specified addresses, subnets or ranges. If FQDNs are assigned, they are resolved every time a configuration lookup is done. If DNS resolution times out, the lookup is delayed for that time. When left empty %any is choosen as default"
    "remote_addresses","list","false","\-","remote_addr, remote","Remote address[es] to use for IKE communication. Accepts single IPv4/IPv6 addresses, DNS names, CIDR subnets or IP address ranges. As an initiator, the first non-range/non-subnet is used to initiate the connection to. As a responder the local destination address must match at least to one of the specified addresses, subnets or ranges. If FQDNs are assigned, they are resolved every time a configuration lookup is done. If DNS resolution times out, the lookup is delayed for that time. To initiate a connection, at least one specific address or DNS name must be specified"
    "pools","list","false","\-","networks","List of named IP pools to allocate virtual IP addresses and other configuration attributes from. Each name references a pool by name from either the pools section or an external pool. Note that the order in which they are queried primarily depends on the plugin order"
    "proposals","list","false","['default']","props","A proposal is a set of algorithms. For non-AEAD algorithms this includes IKE an encryption algorithm, an integrity algorithm, a pseudo random function (PRF) and a Diffie-Hellman key exchange group. For AEAD algorithms, instead of encryption and integrity algorithms a combined algorithm is used. With IKEv2 multiple algorithms of the same kind can be specified in a single proposal, from which one gets selected. For IKEv1 only one algorithm per kind is allowed per proposal, more algorithms get implicitly stripped. Use multiple proposals to offer different algorithm combinations with IKEv1. Algorithm keywords get separated using dashes. Multiple proposals may be separated by commas. The special value default adds a default proposal of supported algorithms considered safe and is usually a good choice for interoperability."
    "unique","string","false","no","\-","One of: 'no', 'never', 'keep', 'replace'; Connection uniqueness policy to enforce. To avoid multiple connections from the same user, a uniqueness policy can be enforced."
    "aggressive","boolean","false","false","aggr","Enables IKEv1 Aggressive Mode instead of IKEv1 Main Mode with Identity Protection. Aggressive Mode is considered less secure because the ID and HASH payloads are exchanged unprotected. This allows a passive attacker to snoop peer identities and even worse, start dictionary attacks on the Preshared Key"
    "version","string","false","ike","vers, v","One of: 'ike', 'ikev1', 'ikev2'; IKE major version to use for connection. 1 uses IKEv1 aka ISAKMP, 2 uses IKEv2. A connection using IKEv1+IKEv2 accepts both IKEv1 and IKEv2 as a responder and initiates the connection actively with IKEv2"
    "mobike","boolean","false","true","mob","Enables MOBIKE on IKEv2 connections. MOBIKE is enabled by default on IKEv2 connections and allows mobility of clients and multi-homing on servers by migrating active IPsec tunnels. Usually keeping MOBIKE enabled is unproblematic, as it is not used if the peer does not indicate support for it. However, due to the design of MOBIKE, IKEv2 always floats to UDP port 4500 starting from the second exchange. Some implementations don’t like this behavior, hence it can be disabled"
    "encapsulation","boolean","false","false","udp_encapsulation, encap","To enforce UDP encapsulation of ESP packets, the IKE daemon can manipulate the NAT detection payloads. This makes the peer believe that a NAT situation exist on the transmission path, forcing it to encapsulate ESP packets in UDP. Usually this is not required but it can help to work around connectivity issues with too restrictive intermediary firewalls that block ESP packets"
    "reauth_seconds","integer","false","\-","reauth, reauth_sec, reauth_time","	Time to schedule IKE reauthentication. IKE reauthentication recreates the IKE/ISAKMP SA from scratch and re-evaluates the credentials. In asymmetric configurations (with EAP or configuration payloads) it might not be possible to actively reauthenticate as responder. The IKEv2 reauthentication lifetime negotiation can instruct the client to perform reauthentication. Reauthentication is disabled by default (0). Enabling it usually may lead to small connection interruptions as strongSwan uses a break-before-make policy with IKEv2 by default"
    "rekey_seconds","integer","false","\-","rekey, rekey_sec, rekey_time","IKE rekeying refreshes key material using a Diffie-Hellman key exchange, but does not re-check associated credentials. It is supported with IKEv2 only. IKEv1 performs a reauthentication procedure instead. With the default value, IKE rekeying is scheduled every 4 hours minus the configured rand_time. If a reauth_time is configured, rekey_time defaults to zero, disabling rekeying. In that case set rekey_time explicitly to both enforce rekeying and reauthentication"
    "over_seconds","integer","false","\-","over, over_sec, over_time","Hard IKE_SA lifetime if rekey/reauth does not complete, as time. To avoid having an IKE or ISAKMP connection kept alive if IKE reauthentication or rekeying fails perpetually, a maximum hard lifetime may be specified. If the IKE_SA fails to rekey or reauthenticate within the specified time, the IKE_SA gets closed. In contrast to CHILD_SA rekeying, over_time is relative in time to the rekey_time and reauth_time values, as it applies to both. The default is 10% of either rekey_time or reauth_time, whichever value is larger. [0.1 * max(rekey_time, reauth_time)]"
    "dpd_delay_seconds","integer","false","\-","dpd_delay, dpd_delay_sec, dpd_delay_time","Interval to check the liveness of a peer actively using IKEv2 INFORMATIONAL exchanges or IKEv1 R_U_THERE messages. Active DPD checking is only enforced if no IKE or ESP/AH packet has been received for the configured DPD delay. Defaults to 0s"
    "dpd_timeout_seconds","integer","false","\-","dpd_timeout, dpd_timeout_sec","Charon by default uses the normal retransmission mechanism and timeouts to check the liveness of a peer, as all messages are used for liveness checking. For compatibility reasons, with IKEv1 a custom interval may be specified. This option has no effect on IKEv2 connections"
    "send_certificate_request","boolean","false","true","send_cert_req","Send certificate request payloads to offer trusted root CA certificates to the peer. Certificate requests help the peer to choose an appropriate certificate/private key for authentication and are enabled by default. Disabling certificate requests can be useful if too many trusted root CA certificates are installed, as each certificate request increases the size of the initial IKE packets"
    "send_certificate","string","false","\-","send_cert","One of: '' (default), 'ifasked', 'never', 'always'; Send certificate payloads when using certificate authentication. With the default of [ifasked] the daemon sends certificate payloads only if certificate requests have been received. [never] disables sending of certificate payloads altogether whereas [always] causes certificate payloads to be sent unconditionally whenever certificate-based authentication is used"
    "keying_tries","integer","false","\-","keyingtries","Number of retransmission sequences to perform during initial connect. Instead of giving up initiation after the first retransmission sequence with the default value of 1, additional sequences may be started according to the configured value. A value of 0 initiates a new sequence until the connection establishes or fails with a permanent error"
    "reload","boolean","false","true","\-", .. include:: ../_include/param_reload.rst

ansibleguy.opnsense.ipsec_pool
==============================

Module alias: ansibleguy.opnsense.ipsec_network

..  csv-table:: Definition
    :header: "Parameter", "Type", "Required", "Default", "Aliases", "Comment"
    :widths: 15 10 10 10 10 45

    "name","string","true","\-","\-","Unique pool/network name"
    "network","string","false for state changes, else true","\-","net, cidr","Pool network in CIDR format"
    "reload","boolean","false","true","\-", .. include:: ../_include/param_reload.rst

ansibleguy.opnsense.ipsec_child
===============================

..  csv-table:: Definition
    :header: "Parameter", "Type", "Required", "Default", "Aliases", "Comment"
    :widths: 15 10 10 10 10 45

    "name","string","true","\-","description, desc","Unique name to identify the entry"
    "connection","string","false for state changes, else true","\-","tunnel, conn, tun","Connection to link this child to"
    "mode","string","false","tunnel","\-","One of: 'tunnel', 'transport', 'pass', 'drop'; IPsec Mode to establish CHILD_SA with. tunnel negotiates the CHILD_SA in IPsec Tunnel Mode whereas transport uses IPsec Transport Mode. pass and drop are used to install shunt policies which explicitly bypass the defined traffic from IPsec processing or drop it, respectively"
    "local_net","list","true","\-","local_traffic_selectors, local_cidr, local_ts, local","List of local traffic selectors to include in CHILD_SA. Each selector is a CIDR subnet definition"
    "remote_net","list","true","\-","remote_traffic_selectors, remote_cidr, remote_ts, remote","List of remote traffic selectors to include in CHILD_SA. Each selector is a CIDR subnet definition"
    "sha256_96","boolean","false","false","sha256","HMAC-SHA-256 is used with 128-bit truncation with IPsec. For compatibility with implementations that incorrectly use 96-bit truncation this option may be enabled to configure the shorter truncation length in the kernel. This is not negotiated, so this only works with peers that use the incorrect truncation length (or have this option enabled)"
    "start_action","string","false","start","start","One of: 'none', 'trap|start', 'route', 'start', 'trap'; Action to perform after loading the configuration. The default of none loads the connection only, which then can be manually initiated or used as a responder configuration. The value trap installs a trap policy which triggers the tunnel as soon as matching traffic has been detected. The value start initiates the connection actively. To immediately initiate a connection for which trap policies have been installed, user Trap|start"
    "close_action","string","false","none","close","One of: 'none', 'trap', 'start'; Action to perform after a CHILD_SA gets closed by the peer. The default of none does not take any action. trap installs a trap policy for the CHILD_SA (note that this is redundant if start_action includes trap). start tries to immediately re-create the CHILD_SA. close_action does not provide any guarantee that the CHILD_SA is kept alive. It acts on explicit close messages only but not on negotiation failures. Use trap policies to reliably re-create failed CHILD_SAs"
    "dpd_action","string","false","clear","dpd","One of: 'clear', 'trap', 'start'; Action to perform for this CHILD_SA on DPD timeout. The default clear closes the CHILD_SA and does not take further action. trap installs a trap policy, which will catch matching traffic and tries to re-negotiate the tunnel on-demand (note that this is redundant if start_action includes trap. restart immediately tries to re-negotiate the CHILD_SA under a fresh IKE_SA"
    "policies","boolean","false","true","pols","Whether to install IPsec policies or not. Disabling this can be useful in some scenarios e.g. VTI where policies are not managed by the IKE daemon"
    "request_id","integer","false","\-","req_id, reqid","This might be helpful in some scenarios, like route based tunnels (VTI), but works only if each CHILD_SA configuration is instantiated not more than once. The default uses dynamic reqids, allocated incrementally"
    "esp_proposals","list","false","['default']","esp_props, esp","Choose 'default' or at least one of the options shown in the Web-UI"
    "rekey_seconds","integer","false","3600","rekey_time, rekey","Time to schedule CHILD_SA rekeying. CHILD_SA rekeying refreshes key material, optionally using a Diffie-Hellman exchange if a group is specified in the proposal. To avoid rekey collisions initiated by both ends simultaneously, a value in the range of rand_time gets subtracted to form the effective soft lifetime. By default CHILD_SA rekeying is scheduled every hour, minus rand_time"
    "reload","boolean","false","true","\-", .. include:: ../_include/param_reload.rst

ansibleguy.opnsense.ipsec_vti
=============================

..  csv-table:: Definition
    :header: "Parameter", "Type", "Required", "Default", "Aliases", "Comment"
    :widths: 15 10 10 10 10 45

    "name","string","true","\-","description, desc","Unique name to identify the entry"
    "request_id","integer","false for state changes, else true","\-","req_id, reqid","This might be helpful in some scenarios, like route based tunnels (VTI), but works only if each CHILD_SA configuration is instantiated not more than once. The default uses dynamic reqids, allocated incrementally"
    "local_address","string","false","\-","local_addr, local","\-"
    "remote_address","string","false","\-","remote_addr, remote","\-"
    "local_tunnel_address","string","false","\-","local_tun_addr, tunnel_local, local_tun","\-"
    "remote_tunnel_address","string","false","\-","remote_tun_addr, tunnel_remote, remote_tun","\-"
    "reload","boolean","false","true","\-", .. include:: ../_include/param_reload.rst

ansibleguy.opnsense.ipsec_auth_local
====================================

..  csv-table:: Definition
    :header: "Parameter", "Type", "Required", "Default", "Aliases", "Comment"
    :widths: 15 10 10 10 10 45

    "name","string","true","\-","description, desc","Unique name to identify the entry"
    "connection","string","false for state changes, else true","\-","tunnel, conn, tun","Connection to use this local authentication with"
    "round","integer","false","0","\-","Numeric identifier by which authentication rounds are sorted"
    "authentication","string","false","psk","auth","One of: 'psk', 'pubkey', 'eap-tls', 'eap-mschapv2', 'xauth-pam', 'eap-radius'; Authentication to perform for this round, when using Pre-Shared key make sure to define one under "VPN->IPsec->Pre-Shared Keys""
    "id","string","false","\-","ike_id","IKE identity to use for authentication round. When using certificate authentication. The IKE identity must be contained in the certificate, either as the subject DN or as a subjectAltName (the identity will default to the certificate’s subject DN if not specified). Refer to https://docs.strongswan.org/docs/5.9/config/identityParsing.html for details on how identities are parsed and may be configured"
    "eap_id","string","false","\-","\-","Must be defined if authentication is set to one of: ['eap-tls', 'eap-mschapv2', 'eap-radius']; Client EAP-Identity to use in EAP-Identity exchange and the EAP method"
    "certificates","list","false","\-","certs","Certificate or public-key must be defined if authentication is set to 'pubkey'; List of certificate candidates to use for authentication"
    "public_keys","list","false","\-","pubkeys","Certificate or public-key must be defined if authentication is set to 'pubkey'; List of raw public key candidates to use for authentication"
    "reload","boolean","false","true","\-", .. include:: ../_include/param_reload.rst

ansibleguy.opnsense.ipsec_auth_remote
=====================================

See: ansibleguy.opnsense.ipsec_auth_local

ansibleguy.opnsense.ipsec_cert
==============================

..  csv-table:: Definition
    :header: "Parameter", "Type", "Required", "Default", "Aliases", "Comment"
    :widths: 15 10 10 10 10 45

    "name","string","true","\-","\-","Name of the key-pair - used to identify the entry."
    "public_key","string","false for state changes, else true","\-","pub_key, pub","\-"
    "private_key","string","false for state changes, else true","\-","priv_key, priv","\-"
    "type","string","false","rsa","\-","Type of the key. Currently the only option is 'rsa'"
    "reload","boolean","false","true","\-", .. include:: ../_include/param_reload.rst

ansibleguy.opnsense.ipsec_psk
=============================

..  csv-table:: Definition
    :header: "Parameter", "Type", "Required", "Default", "Aliases", "Comment"
    :widths: 15 10 10 10 10 45

    "identity_local","string","true","\-","identity, ident","This can be either an IP address, fully qualified domain name or an email address."
    "identity_remote","string","false","\-","remote_ident","(optional) This can be either an IP address, fully qualified domain name or an email address to identify the remote host."
    "psk","string","true","\-","key, secret","\-"
    "type","string","false","\-","kind","One of: 'PSK', 'EAP'"


Usage
*****

To apply changes to the keys, you need to set 'reload: true' on each call or use the :ref:`ansibleguy.opnsense.reload <modules_reload>` module to apply it once you finished modifying all entries!

As far as I can tell - the IPSec service gets restarted one you do so - be aware of that.

Vault
=====

You may want to use '**ansible-vault**' to **encrypt** your 'private_key' content!

.. code-block:: bash

    ansible-vault encrypt_string '-----BEGIN RSA PRIVATE KEY-----\n...-----END RSA PRIVATE KEY-----\n'

    # or encrypt the private_key file beforehand (might be easier)
    ansible-vault encrypt /path/to/private/key/file.pem


Examples
********

ansibleguy.opnsense.ipsec_cert
==============================

.. code-block:: yaml

    - hosts: localhost
      gather_facts: no
      module_defaults:
        group/ansibleguy.opnsense.all:
          firewall: 'opnsense.template.ansibleguy.net'
          api_credential_file: '/home/guy/.secret/opn.key'

        ansibleguy.opnsense.list:
          target: 'ipsec_cert'

      tasks:
        - name: Example
          ansibleguy.opnsense.ipsec_cert:
            name: 'example'
            public_key: |
              -----BEGIN PUBLIC KEY-----
              ...
              -----END PUBLIC KEY-----
            private_key: |
              -----BEGIN RSA PRIVATE KEY-----
              ...
              -----END RSA PRIVATE KEY-----

            # reload: false

        - name: Adding key-pair and applying it
          ansibleguy.opnsense.ipsec_cert:
            name: 'test1'
            public_key: |
              -----BEGIN PUBLIC KEY-----
              ...
              -----END PUBLIC KEY-----
            private_key: !vault ...
            reload: true

        - name: Listing
          ansibleguy.opnsense.list:
          #  target: 'ipsec_cert'
          no_log: true  # could log private keys
          register: existing_entries

        - name: Printing Certificates
          ansible.builtin.debug:
            var: existing_entries.data

        - name: Manually reloading/applying config
          ansibleguy.opnsense.reload:
            target: 'ipsec'

----

ansibleguy.opnsense.ipsec_psk
=============================

.. code-block:: yaml

    - hosts: localhost
      gather_facts: no
      module_defaults:
        group/ansibleguy.opnsense.all:
          firewall: 'opnsense.template.ansibleguy.net'
          api_credential_file: '/home/guy/.secret/opn.key'

        ansibleguy.opnsense.list:
          target: 'ipsec_psk'

      tasks:
        - name: Example
          ansibleguy.opnsense.ipsec_psk:
            identity: 'example'
            psk: 'secret'
            # type: 'PSK'
            # identity_remote: ''

        - name: Adding
          ansibleguy.opnsense.ipsec_psk:
            identity: 'test1'
            psk: 'my-super-secret'

        - name: Removing
          ansibleguy.opnsense.ipsec_psk:
            identity: 'test1'
            state: 'absent'
