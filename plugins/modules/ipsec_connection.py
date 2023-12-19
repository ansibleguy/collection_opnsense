#!/usr/bin/env python3

# Copyright: (C) 2023, AnsibleGuy <guy@ansibleguy.net>
# GNU General Public License v3.0+ (see https://www.gnu.org/licenses/gpl-3.0.txt)

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.handler import \
    module_dependency_error, MODULE_EXCEPTIONS

try:
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.wrapper import module_wrapper
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.main import \
        diff_remove_empty
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.defaults.main import \
        OPN_MOD_ARGS, STATE_MOD_ARG, RELOAD_MOD_ARG
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.main.ipsec_connection import \
        Connection

except MODULE_EXCEPTIONS:
    module_dependency_error()


# DOCUMENTATION = 'https://opnsense.ansibleguy.net/en/latest/modules/ipsec.html'
# EXAMPLES = 'https://opnsense.ansibleguy.net/en/latest/modules/ipsec.html'


def run_module():
    module_args = dict(
        name=dict(
            type='str', required=True, aliases=['description', 'desc'],
            description='Unique connection/tunnel name',
        ),
        local_addresses=dict(
            type='list', elements='str', required=False, aliases=['local_addr', 'local'], default=[],
            description='Local address[es] to use for IKE communication. Accepts single IPv4/IPv6 addresses, '
                        'DNS names, CIDR subnets or IP address ranges. As an initiator, the first non-range/non-subnet '
                        'is used to initiate the connection from. As a responder the local destination address must '
                        'match at least to one of the specified addresses, subnets or ranges. If FQDNs are assigned, '
                        'they are resolved every time a configuration lookup is done. If DNS resolution times out, '
                        'the lookup is delayed for that time. When left empty %any is choosen as default',
        ),
        remote_addresses=dict(
            type='list', elements='str', required=False, aliases=['remote_addr', 'remote'], default=[],
            description='Remote address[es] to use for IKE communication. Accepts single IPv4/IPv6 addresses, '
                        'DNS names, CIDR subnets or IP address ranges. As an initiator, the first non-range/non-subnet '
                        'is used to initiate the connection to. As a responder, the initiator source address must '
                        'match at least to one of the specified addresses, subnets or ranges. If FQDNs are assigned '
                        'they are resolved every time a configuration lookup is done. If DNS resolution times out, '
                        'the lookup is delayed for that time. To initiate a connection, at least one specific address '
                        'or DNS name must be specified',
        ),
        pools=dict(
            type='list', elements='str', required=False, default=[], aliases=['networks', 'nets'],
            description='List of named IP pools to allocate virtual IP addresses and other configuration attributes '
                        'from. Each name references a pool by name from either the pools section or an external pool. '
                        'Note that the order in which they are queried primarily depends on the plugin order',
        ),
        proposals=dict(
            type='list', elements='str', required=False, default=['default'], aliases=['props'],
            description='A proposal is a set of algorithms. For non-AEAD algorithms this includes IKE an encryption '
                        'algorithm, an integrity algorithm, a pseudo random function (PRF) and a Diffie-Hellman key '
                        'exchange group. For AEAD algorithms, instead of encryption and integrity algorithms a '
                        'combined algorithm is used. With IKEv2 multiple algorithms of the same kind can be specified '
                        'in a single proposal, from which one gets selected. For IKEv1 only one algorithm per kind '
                        'is allowed per proposal, more algorithms get implicitly stripped. Use multiple proposals '
                        'to offer different algorithm combinations with IKEv1. Algorithm keywords get separated '
                        'using dashes. Multiple proposals may be separated by commas. The special value default adds '
                        'a default proposal of supported algorithms considered safe and is usually a good choice '
                        'for interoperability',
        ),
        unique=dict(
            type='str', required=False, default='no',
            choices=['no', 'never', 'keep', 'replace'],
            description='Connection uniqueness policy to enforce. To avoid multiple connections from the same user, '
                        'a uniqueness policy can be enforced',
        ),
        aggressive=dict(
            type='bool', required=False, default=False, aliases=['aggr'],
            description='Enables IKEv1 Aggressive Mode instead of IKEv1 Main Mode with Identity Protection. '
                        'Aggressive Mode is considered less secure because the ID and HASH payloads are exchanged '
                        'unprotected. This allows a passive attacker to snoop peer identities and even worse, '
                        'start dictionary attacks on the Preshared Key',
        ),
        version=dict(
            type='str', required=False, default='ikev1+2', aliases=['vers', 'v'],
            choices=list(Connection.FIELDS_VALUE_MAPPING['version'].keys()),
            description='IKE major version to use for connection. 1 uses IKEv1 aka ISAKMP, 2 uses IKEv2. A connection '
                        'using IKEv1+IKEv2 accepts both IKEv1 and IKEv2 as a responder and initiates the connection '
                        'actively with IKEv2',
        ),
        mobike=dict(
            type='bool', required=False, default=True, aliases=['mob'],
            description='Enables MOBIKE on IKEv2 connections. MOBIKE is enabled by default on IKEv2 connections and '
                        'allows mobility of clients and multi-homing on servers by migrating active IPsec tunnels. '
                        'Usually keeping MOBIKE enabled is unproblematic, as it is not used if the peer does not '
                        'indicate support for it. However, due to the design of MOBIKE, IKEv2 always floats to UDP '
                        'port 4500 starting from the second exchange. Some implementations don’t like this behavior, '
                        'hence it can be disabled',
        ),
        encapsulation=dict(
            type='bool', required=False, default=False, aliases=['udp_encapsulation', 'encap'],
            description='To enforce UDP encapsulation of ESP packets, the IKE daemon can manipulate the NAT detection '
                        'payloads. This makes the peer believe that a NAT situation exist on the transmission path, '
                        'forcing it to encapsulate ESP packets in UDP. Usually this is not required but it can help '
                        'to work around connectivity issues with too restrictive intermediary firewalls that block '
                        'ESP packets',
        ),
        reauth_seconds=dict(
            type='str', required=False, aliases=['reauth', 'reauth_sec', 'reauth_time'], default='',
            description='Time to schedule IKE reauthentication. IKE reauthentication recreates the IKE/ISAKMP SA '
                        'from scratch and re-evaluates the credentials. In asymmetric configurations (with EAP or '
                        'configuration payloads) it might not be possible to actively reauthenticate as responder. '
                        'The IKEv2 reauthentication lifetime negotiation can instruct the client to perform '
                        'reauthentication. Reauthentication is disabled by default (0). Enabling it usually may '
                        'lead to small connection interruptions as strongSwan uses a break-before-make policy '
                        'with IKEv2 by default',
        ),
        rekey_seconds=dict(
            type='str', required=False, aliases=['rekey', 'rekey_sec', 'rekey_time'], default='',
            description='IKE rekeying refreshes key material using a Diffie-Hellman key exchange, but does not '
                        're-check associated credentials. It is supported with IKEv2 only. IKEv1 performs a '
                        'reauthentication procedure instead. With the default value, IKE rekeying is scheduled '
                        'every 4 hours minus the configured rand_time. If a reauth_time is configured, rekey_time '
                        'defaults to zero, disabling rekeying. In that case set rekey_time explicitly to both '
                        'enforce rekeying and reauthentication',
        ),
        over_seconds=dict(
            type='str', required=False, aliases=['over', 'over_sec', 'over_time'], default='',
            description='Hard IKE_SA lifetime if rekey/reauth does not complete, as time. To avoid having an IKE or '
                        'ISAKMP connection kept alive if IKE reauthentication or rekeying fails perpetually, a '
                        'maximum hard lifetime may be specified. If the IKE_SA fails to rekey or reauthenticate '
                        'within the specified time, the IKE_SA gets closed. In contrast to CHILD_SA rekeying, '
                        'over_time is relative in time to the rekey_time and reauth_time values, as it applies '
                        'to both. The default is 10% of either rekey_time or reauth_time, whichever value is larger. '
                        '[0.1 * max(rekey_time, reauth_time)]',
        ),
        dpd_delay_seconds=dict(
            type='str', required=False, aliases=['dpd_delay', 'dpd_delay_sec', 'dpd_delay_time'], default='',
            description='Interval to check the liveness of a peer actively using IKEv2 INFORMATIONAL exchanges or '
                        'IKEv1 R_U_THERE messages. Active DPD checking is only enforced if no IKE or ESP/AH packet '
                        'has been received for the configured DPD delay. Defaults to 0s',
        ),
        dpd_timeout_seconds=dict(
            type='str', required=False, aliases=['dpd_timeout', 'dpd_timeout_sec'], default='',
            description='Charon by default uses the normal retransmission mechanism and timeouts to check the '
                        'liveness of a peer, as all messages are used for liveness checking. For compatibility '
                        'reasons, with IKEv1 a custom interval may be specified. This option has no effect on '
                        'IKEv2 connections',
        ),
        send_certificate_request=dict(
            type='bool', required=False, default=True, aliases=['send_cert_req'],
            description='Send certificate request payloads to offer trusted root CA certificates to the peer. '
                        'Certificate requests help the peer to choose an appropriate certificate/private key for '
                        'authentication and are enabled by default. Disabling certificate requests can be useful '
                        'if too many trusted root CA certificates are installed, as each certificate request '
                        'increases the size of the initial IKE packets',
        ),
        send_certificate=dict(
            type='str', required=False, default='', aliases=['send_cert'],
            choices=['', 'ifasked', 'never', 'always'],
            description='Send certificate payloads when using certificate authentication. With the default of '
                        '[ifasked] the daemon sends certificate payloads only if certificate requests have been '
                        'received. [never] disables sending of certificate payloads altogether whereas [always] '
                        'causes certificate payloads to be sent unconditionally whenever certificate-based '
                        'authentication is used',
        ),
        keying_tries=dict(
            type='str', required=False, aliases=['keyingtries'], default='',
            description='Number of retransmission sequences to perform during initial connect. Instead of giving '
                        'up initiation after the first retransmission sequence with the default value of 1, '
                        'additional sequences may be started according to the configured value. A value of 0 '
                        'initiates a new sequence until the connection establishes or fails with a permanent error',
        ),
        **RELOAD_MOD_ARG,
        **STATE_MOD_ARG,
        **OPN_MOD_ARGS,
    )

    result = dict(
        changed=False,
        diff={
            'before': {},
            'after': {},
        }
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True,
    )

    module_wrapper(Connection(module=module, result=result))

    result['diff'] = diff_remove_empty(result['diff'])
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
