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
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.main.ipsec_vti import \
        Vti

except MODULE_EXCEPTIONS:
    module_dependency_error()


# DOCUMENTATION = 'https://opnsense.ansibleguy.net/en/latest/modules/ipsec.html'
# EXAMPLES = 'https://opnsense.ansibleguy.net/en/latest/modules/ipsec.html'


def run_module():
    # todo: add description to parameters => VTI not found in WebUI (?!)
    module_args = dict(
        name=dict(
            type='str', required=True, aliases=['description', 'desc'],
            description='Unique name to identify the entry'
        ),
        request_id=dict(
            type='int', default=0, required=False, aliases=['req_id', 'reqid'],
            description='This might be helpful in some scenarios, like route based tunnels (VTI), but works only if '
                        'each CHILD_SA configuration is instantiated not more than once. The default uses dynamic '
                        'reqids, allocated incrementally',
        ),
        local_address=dict(
            type='str', required=False, aliases=['local_addr', 'local'],
        ),
        remote_address=dict(
            type='str', required=False, aliases=['remote_addr', 'remote'],
        ),
        local_tunnel_address=dict(
            type='str', required=False, aliases=['local_tun_addr', 'tunnel_local', 'local_tun'],
        ),
        remote_tunnel_address=dict(
            type='str', required=False, aliases=['remote_tun_addr', 'tunnel_remote', 'remote_tun'],
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

    module_wrapper(Vti(module=module, result=result))

    result['diff'] = diff_remove_empty(result['diff'])
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
