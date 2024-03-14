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
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.defaults.openvpn import \
        OPENVPN_INSTANCE_MOD_ARGS
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.main.openvpn_client import Client

except MODULE_EXCEPTIONS:
    module_dependency_error()


# DOCUMENTATION = 'https://opnsense.ansibleguy.net/en/latest/modules/openvpn.html'
# EXAMPLES = 'https://opnsense.ansibleguy.net/en/latest/modules/openvpn.html'

def run_module():
    module_args = dict(
        # general
        remote=dict(
            type='list', elements='str', required=False, aliases=['peer', 'server'],
            description='Remote host name or IP address with optional port'
        ),
        port=dict(
            type='str', required=False, default='', aliases=['local_port', 'bind_port'],
            description='Port number to use.'
                        'Specifies a bind address, or nobind when client does not have a specific bind address.'
        ),
        carp_depend_on=dict(
            aliases=['vip', 'vip_depend', 'carp', 'carp_depend'],
            type='str', required=False, default='',
            description='The carp VHID to depend on, when this virtual address is not in '
                        'master state, the interface cost will be set to the demoted cost'
        ),
        # auth
        username=dict(
            type='str', required=False, default='', aliases=['user'],
            description='(optional) Username to send to the server for authentication when required.'
        ),
        password=dict(
            type='str', required=False, default='', aliases=['pwd'], no_log=True,
            description='Password belonging to the user specified above'
        ),
        **OPENVPN_INSTANCE_MOD_ARGS,
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

    module_wrapper(Client(module=module, result=result))

    result['diff'] = diff_remove_empty(result['diff'])
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
