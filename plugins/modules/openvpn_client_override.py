#!/usr/bin/env python3

# Copyright: (C) 2024, AnsibleGuy <guy@ansibleguy.net>
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
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.main.openvpn_client_override import Override

except MODULE_EXCEPTIONS:
    module_dependency_error()


# DOCUMENTATION = 'https://opnsense.ansibleguy.net/en/latest/modules/openvpn.html'
# EXAMPLES = 'https://opnsense.ansibleguy.net/en/latest/modules/openvpn.html'

def run_module():
    module_args = dict(
        name=dict(
            type='str', required=True, aliases=['x509', 'common_name'],
            description="The client's X.509 common-name used to match these override to"
        ),
        servers=dict(
            type='list', elements='str', required=False, aliases=['instances'],
            description='Select the OpenVPN servers where this override applies to, leave empty for all'
        ),
        description=dict(
            type='str', required=False, aliases=['desc'],
            description='You may enter a description here for your reference (not parsed).'
        ),
        block=dict(
            type='bool', required=False, default=False, aliases=['block_connection', 'block_client'],
            description="Block this client connection based on its common name. Don't use this option to permanently "
                        "disable a client due to a compromised key or password. "
                        "Use a CRL (certificate revocation list) instead."
        ),
        push_reset=dict(
            type='bool', required=False, default=False, aliases=['reset'],
            description="Don't inherit the global push list for a specific client instance. NOTE: --push-reset is "
                        "very thorough: it will remove almost all options from the list of to-be-pushed options. "
                        "In many cases, some of these options will need to be re-configured afterwards - "
                        "specifically, --topology subnet and --route-gateway will get lost and this will break "
                        "client configs in many cases."
        ),
        network_tunnel_ip4=dict(
            type='str', required=False, aliases=['tun_ip4', 'tunnel_ip4'],
            description='Push virtual IP endpoints for client tunnel, overriding dynamic allocation.'
        ),
        network_tunnel_ip6=dict(
            type='str', required=False, aliases=['tun_ip6', 'tunnel_ip6'],
            description='Push virtual IP endpoints for client tunnel, overriding dynamic allocation.'
        ),
        network_local=dict(
            type='list', elements='str', required=False, default=[], aliases=['net_local', 'push_route'],
            description='These are the networks accessible by the client, these are pushed via route{-ipv6} '
                        'clauses in OpenVPN to the client.'
        ),
        network_remote=dict(
            type='list', elements='str', required=False, default=[], aliases=['net_remote', 'route'],
            description='Remote networks for the server, these are configured via iroute{-ipv6} clauses in OpenVPN '
                        'and inform the server to send these networks to this specific client.'
        ),
        route_gateway=dict(
            type='str', required=False, aliases=['route_gw', 'rt_gw'],
            description='Specify a default gateway to use for the connected client. Without one set the first '
                        'address in the netblock is being offered. When segmenting the tunnel (server) network, '
                        'this one might not be accessible from the client.'
        ),
        redirect_gateway=dict(
            type='list', elements='str', required=False, default=[], aliases=['redirect_gw', 'redir_gw'],
            choices=['local', 'autolocal', 'def1', 'bypass_dhcp', 'bypass_dns', 'block_local', 'ipv6', 'notipv4'],
            description='Automatically execute routing commands to cause all outgoing IP traffic to be '
                        'redirected over the VPN.'
        ),
        register_dns=dict(
            type='bool', required=False, default=False,
            description='Run ipconfig /flushdns and ipconfig /registerdns on connection initiation. '
                        'This is known to kick Windows into recognizing pushed DNS servers.'
        ),
        domain=dict(
            type='str', required=False, aliases=['dns_domain'],
            description='Set Connection-specific DNS Suffix.'
        ),
        domain_list=dict(
            type='list', elements='str', required=False, default=[], aliases=['dns_domain_search'],
            description='Add name to the domain search list. Repeat this option to add more entries. '
                        'Up to 10 domains are supported.'
        ),
        dns_servers=dict(
            type='list', elements='str', required=False, default=[], aliases=['dns'],
            description='Set primary domain name server IPv4 or IPv6 address. '
                        'Repeat this option to set secondary DNS server addresses.'
        ),
        ntp_servers=dict(
            type='list', elements='str', required=False, default=[], aliases=['ntp'],
            description='Set primary NTP server address (Network Time Protocol). '
                        'Repeat this option to set secondary NTP server addresses.'
        ),
        wins_servers=dict(
            type='list', elements='str', required=False, default=[], aliases=['wins'],
            description='Set primary WINS server address (NetBIOS over TCP/IP Name Server). '
                        'Repeat this option to set secondary WINS server addresses.'
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

    module_wrapper(Override(module=module, result=result))

    result['diff'] = diff_remove_empty(result['diff'])
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
