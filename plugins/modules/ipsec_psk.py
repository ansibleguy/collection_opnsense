#!/usr/bin/env python3

# Copyright: (C) 2023, AnsibleGuy <guy@ansibleguy.net>
# GNU General Public License v3.0+ (see https://www.gnu.org/licenses/gpl-3.0.txt)

# see: https://docs.opnsense.org/development/api/core/ipsec.html

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.handler import \
    module_dependency_error, MODULE_EXCEPTIONS

try:
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.wrapper import module_wrapper
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.main import diff_remove_empty
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.main.ipsec_psk import PreSharedKey
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.defaults.main import \
        OPN_MOD_ARGS, STATE_ONLY_MOD_ARG, RELOAD_MOD_ARG_DEF_FALSE

except MODULE_EXCEPTIONS:
    module_dependency_error()


# DOCUMENTATION = 'https://opnsense.ansibleguy.net/en/latest/modules/ipsec.html'
# EXAMPLES = 'https://opnsense.ansibleguy.net/en/latest/modules/ipsec.html'


def run_module():
    module_args = dict(
        identity_local=dict(
            type='str', required=True, aliases=['identity', 'ident'],
            description='This can be either an IP address, fully qualified domain name or an email address.'
        ),
        identity_remote=dict(
            type='str', required=False, aliases=['remote_ident'],
            description='(optional) This can be either an IP address, fully qualified domain name or '
                        'an email address to identify the remote host.'
        ),
        psk=dict(type='str', required=False, no_log=True, aliases=['key', 'secret']),
        type=dict(
            type='str', required=False, choices=['PSK', 'EAP'], default='PSK', aliases=['kind'],
        ),
        **RELOAD_MOD_ARG_DEF_FALSE,
        **STATE_ONLY_MOD_ARG,
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

    module_wrapper(PreSharedKey(module=module, result=result))

    result['diff'] = diff_remove_empty(result['diff'])
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
