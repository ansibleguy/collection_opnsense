#!/usr/bin/env python3

# Copyright: (C) 2023, AnsibleGuy <guy@ansibleguy.net>
# GNU General Public License v3.0+ (see https://www.gnu.org/licenses/gpl-3.0.txt)

# see: https://docs.opnsense.org/development/api/plugins/unbound.html

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.handler import \
    module_dependency_error, MODULE_EXCEPTIONS

try:
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.utils import profiler
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.main import \
        diff_remove_empty
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.defaults.main import \
        OPN_MOD_ARGS, EN_ONLY_MOD_ARG, RELOAD_MOD_ARG
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.main.unbound_general import General

except MODULE_EXCEPTIONS:
    module_dependency_error()

PROFILE = False  # create log to profile time consumption

DOCUMENTATION = 'https://opnsense.ansibleguy.net/en/latest/modules/unbound.html'
EXAMPLES = 'https://opnsense.ansibleguy.net/en/latest/modules/unbound.html'


def run_module():
    module_args = dict(
        port=dict(
            type='int', required=False, default=53,
            description='The TCP/UDP port used for responding to DNS queries'
        ),
        interfaces=dict(
            type='list', elements='str', required=False, default=[],
            description='The interface(s) used for responding to queries from clients'
        ),
        dnssec=dict(
            type='bool', required=False, default=False,
            description='Whether DNSSEC is enabled'
        ),
        dns64=dict(
            type='bool', required=False, default=False,
            description='Whether Unbound will synthesize AAAA records from A records if no '
                        'actual AAAA records are present'
        ),
        # IPv6 netmask
        dns64_prefix=dict(
            type='str', required=False, default='64:ff9b::/96',
            description='The DNS64 prefix'
        ),
        aaaa_only_mode=dict(
            type='bool', required=False, default=False,
            description='Whether Unbound will remove all A records from the answer section '
                        'of all responses'
        ),
        register_dhcp_leases=dict(
            type='bool', required=False, default=False,
            description='Whether machines that specify their hostname when requesting a '
                        'DHCP lease will be registered in Unbound'
        ),
        dhcp_domain=dict(
            type='str', required=False, default='',
            description='The default domain name to use for DHCP lease registration'
        ),
        register_dhcp_static_mappings=dict(
            type='bool', required=False, default=False,
            description='Whether DHCP static mappings will be registered in Unbound'
        ),
        register_ipv6_link_local=dict(
            type='bool', required=False, default=True,
            description='Whether IPv6 link-local addresses will be registered in Unbound'
        ),
        register_system_records=dict(
            type='bool', required=False, default=True,
            description='Whether A/AAAA records for the configured listen interfaces '
                        'will be generated'
        ),
        txt_records=dict(
            type='bool', required=False, default=False, aliases=['txt'],
            description='Whether descriptions associated with Host entries and DHCP Static '
                        'mappings will create a corresponding TXT record'
        ),
        flush_dns_cache=dict(
            type='bool', required=False, default=False,
            description='Whether the DNS cache will be flushed during each daemon reload'
        ),
        local_zone_type=dict(
            type='str', required=False, default='transparent', choices=['transparent',
            'always_nxdomain', 'always_refuse', 'always_transparent', 'deny', 'inform',
            'inform_deny', 'nodefault', 'refuse', 'static', 'typetransparent'],
            description='The local zone type used for the system domain'
        ),
        outgoing_interfaces=dict(
            type='list', elements='str', required=False, default=[],
            description='The interface(s) that Unbound will use to send queries to '
                        'authoritative servers and receive their replies'
        ),
        wpad=dict(
            type='bool', required=False, default=False,
            description='Whether CNAME records for the WPAD host of all configured domains '
                        'will be automatically added as well as overrides for TXT records for domains'
        ),
        **EN_ONLY_MOD_ARG,
        **OPN_MOD_ARGS,
        **RELOAD_MOD_ARG,
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

    g = General(module=module, result=result)

    def process():
        g.check()
        g.process()
        if result['changed'] and module.params['reload']:
            g.reload()

    if PROFILE or module.params['debug']:
        profiler(check=process, log_file='unbound_general.log')
        # log in /tmp/ansibleguy.opnsense/

    else:
        process()

    g.s.close()
    result['diff'] = diff_remove_empty(result['diff'])
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
