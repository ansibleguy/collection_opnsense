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
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.main.frr_ospf_general import General

except MODULE_EXCEPTIONS:
    module_dependency_error()


# DOCUMENTATION = 'https://opnsense.ansibleguy.net/en/latest/modules/frr_ospf.html'
# EXAMPLES = 'https://opnsense.ansibleguy.net/en/latest/modules/frr_ospf.html'


def run_module():
    module_args = dict(
        carp=dict(
            type='bool', required=False, default=False, aliases=['carp_demote'],
            description='Register CARP status monitor, when no neighbors are found, '
                        'consider this node less attractive. This feature needs syslog '
                        'enabled using "Debugging" logging to catch all relevant status '
                        'events. This option is not compatible with "Enable CARP Failover"'
        ),
        id=dict(
            type='str', required=False, default='', aliases=['router_id'],
            description='If you have a CARP setup, you may want to configure a router id '
                        'in case of a conflict'
        ),
        cost=dict(
            type='str', required=False, default='',
            aliases=['reference_cost', 'ref_cost'],
            description='Here you can adjust the reference cost in Mbps for path calculation. '
                        'Mostly needed when you bundle interfaces to higher bandwidth'
        ),
        passive_ints=dict(
            type='list', elements='str', required=False, default=[],
            aliases=['passive_interfaces'],
            description='Select the interfaces, where no OSPF packets should be sent to'
        ),
        redistribute=dict(
            type='list', elements='str', required=False, default=[],
            options=['bgp', 'connected', 'kernel', 'rip', 'static'],
            description='Select other routing sources, which should be '
                        'redistributed to the other nodes'
        ),
        redistribute_map=dict(
            type='str', required=False, default='',
            description='Route Map to set for Redistribution'
        ),
        originate=dict(
            type='bool', required=False, default=False, aliases=['orig', 'advertise_default_gw'],
            description='This will send the information that we have a default gateway'
        ),
        originate_always=dict(
            type='bool', required=False, default=False,
            aliases=['orig_always', 'always_advertise_default_gw'],
            description='This will send the information that we have a default gateway, '
                        'regardless of if it is available'
        ),
        originate_metric=dict(
            type='str', default='', required=False, aliases=['orig_metric'],
            description='This let you manipulate the metric when advertising default gateway'
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
