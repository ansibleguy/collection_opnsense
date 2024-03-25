#!/usr/bin/env python3

# Copyright: (C) 2023, AnsibleGuy <guy@ansibleguy.net>
# GNU General Public License v3.0+ (see https://www.gnu.org/licenses/gpl-3.0.txt)

# see: https://docs.opnsense.org/development/api/plugins/quagga.html

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.handler import \
    module_dependency_error, MODULE_EXCEPTIONS

try:
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.wrapper import module_wrapper
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.main import diff_remove_empty
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.defaults.main import \
        OPN_MOD_ARGS, STATE_MOD_ARG, RELOAD_MOD_ARG
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.main.frr_bgp_as_path import AsPath

except MODULE_EXCEPTIONS:
    module_dependency_error()


# DOCUMENTATION = 'https://opnsense.ansibleguy.net/en/latest/modules/frr_bgp.html#ansibleguy-opnsense-frr-bgp-as-path'
# EXAMPLES = 'https://opnsense.ansibleguy.net/en/latest/modules/frr_bgp.html#id6'


def run_module():
    module_args = dict(
        description=dict(type='str', required=True, aliases=['desc']),
        number=dict(
            type='str', required=False, aliases=['nr'],
            description='The ACL rule number (10-99); keep in mind that there are no '
                        'sequence numbers with AS-Path lists. When you want to add a '
                        'new line between you have to completely remove the ACL!'
        ),
        action=dict(type='str', required=False, options=['permit', 'deny']),
        as_pattern=dict(
            type='str', required=False, aliases=['as'],
            description="The AS pattern you want to match, regexp allowed (e.g. .$ or _1$). "
                        "It's not validated so please be careful!"
        ),
        **STATE_MOD_ARG,
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

    module_wrapper(AsPath(module=module, result=result))

    result['diff'] = diff_remove_empty(result['diff'])
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
