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
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.main.ipsec_child import \
        Child

except MODULE_EXCEPTIONS:
    module_dependency_error()


# DOCUMENTATION = 'https://opnsense.ansibleguy.net/en/latest/modules/ipsec.html'
# EXAMPLES = 'https://opnsense.ansibleguy.net/en/latest/modules/ipsec.html'


def run_module():
    module_args = dict(
        name=dict(
            type='str', required=True, aliases=['description', 'desc'],
            description='Unique name to identify the entry'
        ),
        connection=dict(
            type='str', required=False, aliases=['tunnel', 'conn', 'tun'],
            description='Connection to link this child to'
        ),
        mode=dict(
            type='str', required=False, default='tunnel',
            choices=['tunnel', 'transport', 'pass', 'drop'],
            description='IPsec Mode to establish CHILD_SA with. tunnel negotiates the CHILD_SA in IPsec Tunnel '
                        'Mode whereas transport uses IPsec Transport Mode. pass and drop are used to install '
                        'shunt policies which explicitly bypass the defined traffic from IPsec processing or '
                        'drop it, respectively',
        ),
        request_id=dict(
            type='str', required=False, aliases=['req_id', 'reqid'],
            description='This might be helpful in some scenarios, like route based tunnels (VTI), but works only if '
                        'each CHILD_SA configuration is instantiated not more than once. The default uses dynamic '
                        'reqids, allocated incrementally',
        ),
        esp_proposals=dict(
            type='list', elements='str', required=False, default=['default'],
            aliases=['esp_props', 'esp'],
        ),
        sha256_96=dict(
            type='bool', required=False, default=False, aliases=['sha256'],
            description='HMAC-SHA-256 is used with 128-bit truncation with IPsec. For compatibility with '
                        'implementations that incorrectly use 96-bit truncation this option may be enabled to '
                        'configure the shorter truncation length in the kernel. This is not negotiated, so this '
                        'only works with peers that use the incorrect truncation length (or have this option enabled)',
        ),
        start_action=dict(
            type='str', required=False, aliases=['start'], default='start',
            choices=['none', 'trap|start', 'route', 'start', 'trap'],
            description='Action to perform after loading the configuration. The default of none loads the connection '
                        'only, which then can be manually initiated or used as a responder configuration. The value '
                        'trap installs a trap policy which triggers the tunnel as soon as matching traffic has been '
                        'detected. The value start initiates the connection actively. To immediately initiate a '
                        'connection for which trap policies have been installed, user Trap|start',
        ),
        close_action=dict(
            type='str', required=False, aliases=['close'], default='none',
            choices=['none', 'trap', 'start'],
        ),
        dpd_action=dict(
            type='str', required=False, aliases=['dpd'], default='clear',
            choices=['clear', 'trap', 'start'],
        ),
        policies=dict(
            type='bool', required=False, default=True, aliases=['pols'],
            description='Whether to install IPsec policies or not. Disabling this can be useful in some scenarios '
                        'e.g. VTI where policies are not managed by the IKE daemon',
        ),
        local_net=dict(
            type='list', elements='str', required=False, default=[],
            aliases=['local_traffic_selectors', 'local_cidr', 'local_ts', 'local'],
            description='List of local traffic selectors to include in CHILD_SA. Each selector is a CIDR '
                        'subnet definition',
        ),
        remote_net=dict(
            type='list', elements='str', required=False, default=[],
            aliases=['remote_traffic_selectors', 'remote_cidr', 'remote_ts', 'remote'],
            description='List of remote traffic selectors to include in CHILD_SA. Each selector is a CIDR '
                        'subnet definition',
        ),
        rekey_seconds=dict(
            type='int', default=3600, required=False, aliases=['rekey_time', 'rekey'],
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

    module_wrapper(Child(module=module, result=result))

    result['diff'] = diff_remove_empty(result['diff'])
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
