#!/usr/bin/env python3

# Copyright: (C) 2023, AnsibleGuy <guy@ansibleguy.net>
# GNU General Public License v3.0+ (see https://www.gnu.org/licenses/gpl-3.0.txt)

# see: https://docs.opnsense.org/development/api/plugins/quagga.html

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.handler import \
    module_dependency_error, MODULE_EXCEPTIONS

try:
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.wrapper import module_wrapper
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.main import \
        diff_remove_empty
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.defaults.main import \
        OPN_MOD_ARGS, EN_ONLY_MOD_ARG, RELOAD_MOD_ARG
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.main.frr_bgp_general import General

except MODULE_EXCEPTIONS:
    module_dependency_error()


# DOCUMENTATION = 'https://opnsense.ansibleguy.net/en/latest/modules/frr_bgp.html#ansibleguy-opnsense-frr-bgp-general'
# EXAMPLES = 'https://opnsense.ansibleguy.net/en/latest/modules/frr_bgp.html#id1'


def run_module():
    module_args = dict(
        as_number=dict(type='int', required=True, aliases=['as', 'as_nr']),
        id=dict(type='str', required=False, aliases=['router_id']),
        graceful=dict(
            type='bool', required=False, default=False,
            description='BGP graceful restart functionality as defined in '
                        'RFC-4724 defines the mechanisms that allows BGP speaker '
                        'to continue to forward data packets along known routes '
                        'while the routing protocol information is being restored'
        ),
        networks=dict(
            type='list', elements='str', required=False, default=[],
            aliases=['nets'],
            description='Select the network to advertise, you have to set a '
                        'Null route via System -> Routes'
        ),
        redistribute=dict(
            type='list', elements='str', required=False, default=[],
            options=['ospf', 'connected', 'kernel', 'rip', 'static'],
            description='Select other routing sources, which should be '
                        'redistributed to the other nodes'
        ),
        **RELOAD_MOD_ARG,
        **EN_ONLY_MOD_ARG,
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

    module_wrapper(General(module=module, result=result))

    result['diff'] = diff_remove_empty(result['diff'])
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
