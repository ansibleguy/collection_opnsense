#!/usr/bin/env python3

# Copyright: (C) 2022, AnsibleGuy <guy@ansibleguy.net>
# GNU General Public License v3.0+ (see https://www.gnu.org/licenses/gpl-3.0.txt)

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.handler import \
    module_dependency_error, MODULE_EXCEPTIONS

try:
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.utils import profiler
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.main import \
        diff_remove_empty
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.defaults.main import \
        OPN_MOD_ARGS, RELOAD_MOD_ARG
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.main.webproxy_forward import General

except MODULE_EXCEPTIONS:
    module_dependency_error()

PROFILE = False  # create log to profile time consumption

DOCUMENTATION = 'https://opnsense.ansibleguy.net/en/latest/modules/webproxy.html'
EXAMPLES = 'https://opnsense.ansibleguy.net/en/latest/modules/webproxy.html'


def run_module():
    module_args = dict(
        interfaces=dict(
            type='list', elements='str', required=False, default=['lan'], aliases=['ints'],
            description='Interface(s) the proxy will bind to'
        ),
        port=dict(type='int', required=False, default=3128, aliases=['p']),
        port_ssl=dict(type='int', required=False, default=3129, aliases=['p_ssl']),
        transparent=dict(
            type='bool', required=False, default=False, aliases=['transparent_mode'],
            description='Enable transparent proxy mode. You will need a firewall rule to '
                        'forward traffic from the firewall to the proxy server. You may '
                        'leave the proxy interfaces empty, but remember to set a valid ACL '
                        'in that case'
        ),
        ssl_inspection=dict(
            type='bool', required=False, default=False, aliases=['ssl_inspect', 'ssl'],
            description='Enable SSL inspection mode, which allows to log HTTPS connections '
                        'information, such as requested URL and/or make the proxy act as a '
                        'man in the middle between the internet and your clients. Be aware '
                        'of the security implications before enabling this option. If you '
                        'plan to use transparent HTTPS mode, you need nat rules to reflect '
                        'your traffic'
        ),
        ssl_inspection_sni_only=dict(
            type='bool', required=False, default=False, aliases=['ssl_sni_only'],
            description='Do not decode and/or filter SSL content, only log requested domains '
                        'and IP addresses. Some old servers may not provide SNI, so their '
                        'addresses will not be indicated'
        ),
        ssl_ca=dict(
            type='str', required=False, default='', aliases=['ca'],
            description='Select a Certificate Authority to use'
        ),
        ssl_exclude=dict(
            type='list', elements='str', required=False, default=[],
            description='A list of sites which may not be inspected, for example bank sites. '
                        'Prefix the domain with a . to accept all subdomains (e.g. .google.com)'
        ),
        ssl_cache_mb=dict(
            type='int', required=False, default=4, aliases=['ssl_cache', 'cache'],
            description='The maximum size (in MB) to use for SSL certificates'
        ),
        ssl_workers=dict(
            type='int', required=False, default=5, aliases=['workers'],
            description='The number of ssl certificate workers to use (sslcrtd_children)'
        ),
        allow_interface_subnets=dict(
            type='bool', required=False, default=True, aliases=['allow_subnets'],
            description='When enabled the subnets of the selected interfaces will be '
                        'added to the allow access list'
        ),
        # snmp tab
        snmp=dict(
            type='bool', required=False, default=False,
            description='Enable or disable the squid SNMP Agent'
        ),
        port_snmp=dict(type='int', required=False, default=3401, aliases=['p_snmp']),
        snmp_password=dict(
            type='str', required=False, default='public', no_log=True,
            aliases=['snmp_community', 'snmp_pwd'],
            description='The password for access to SNMP agent'
        ),
        # ftp tab
        interfaces_ftp=dict(
            type='list', elements='str', required=False, default=[], aliases=['ints_ftp'],
            description='Interface(s) the ftp proxy will bind to'
        ),
        port_ftp=dict(type='int', required=False, default=2121, aliases=['p_ftp']),
        transparent_ftp=dict(
            type='bool', required=False, default=False,
            description='Enable transparent ftp proxy mode to forward all requests '
                        'for destination port 21 to the proxy server without any '
                        'additional configuration'
        ),
        **RELOAD_MOD_ARG,
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

    g = General(module=module, result=result)

    def process():
        g.check()
        g.process()
        if result['changed'] and module.params['reload']:
            g.reload()

    if PROFILE or module.params['debug']:
        profiler(check=process, log_file='webproxy_forward.log')
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
