#!/usr/bin/env python3

# Copyright: (C) 2023, AnsibleGuy <guy@ansibleguy.net>
# GNU General Public License v3.0+ (see https://www.gnu.org/licenses/gpl-3.0.txt)

# see: https://docs.opnsense.org/development/api/core/interfaces.html

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.handler import \
    module_dependency_error, MODULE_EXCEPTIONS

try:
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.wrapper import module_wrapper
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.main import diff_remove_empty
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.defaults.main import \
        OPN_MOD_ARGS, STATE_ONLY_MOD_ARG, RELOAD_MOD_ARG
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.main.interface_vlan import Vlan

except MODULE_EXCEPTIONS:
    module_dependency_error()


# DOCUMENTATION = 'https://opnsense.ansibleguy.net/en/latest/modules/interface.html'
# EXAMPLES = 'https://opnsense.ansibleguy.net/en/latest/modules/interface.html'


def run_module():
    module_args = dict(
        # name=dict(type='str', required=True, aliases=['vlanif']),  # can't be configured
        interface=dict(
            type='str', required=False, aliases=['parent', 'port', 'int', 'if'],
            description='Existing VLAN capable interface - you must provide the network '
                        "port as shown in 'Interfaces - Assignments - Network port'"
        ),
        vlan=dict(
            type='int', required=False, aliases=['tag', 'id'],
            description='802.1Q VLAN tag (between 1 and 4094)'
        ),
        priority=dict(
            type='int', required=False, default=0, aliases=['prio', 'pcp'],
            description='802.1Q VLAN PCP (priority code point)'
        ),
        description=dict(type='str', required=True, aliases=['desc', 'name']),
        **RELOAD_MOD_ARG,
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

    module_wrapper(Vlan(module=module, result=result))

    result['diff'] = diff_remove_empty(result['diff'])
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
