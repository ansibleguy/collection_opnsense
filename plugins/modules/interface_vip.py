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
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.main.interface_vip import Vip

except MODULE_EXCEPTIONS:
    module_dependency_error()


# DOCUMENTATION = 'https://opnsense.ansibleguy.net/en/latest/modules/interface.html'
# EXAMPLES = 'https://opnsense.ansibleguy.net/en/latest/modules/interface.html'


def run_module():
    module_args = dict(
        address=dict(
            type='str', required=True, aliases=['addr', 'ip', 'network', 'net'],
            description='Provide an address and subnet to use. (e.g 192.168.0.1/24)',
        ),
        interface=dict(
            type='str', required=True, aliases=['port', 'int', 'if'],
            description='Existing interface - you must provide the network '
                        "port as shown in 'Interfaces - Assignments - Network port'"
        ),
        mode=dict(
            type='str', required=False, aliases=['m'], default='ipalias',
            choices=['ipalias', 'carp', 'proxyarp', 'other'],
        ),
        expand=dict(type='bool', required=False, default=True),
        bind=dict(
            type='bool', required=False, default=True,
            description="Assigning services to the virtual IP's interface will automatically "
                        "include this address. Uncheck to prevent binding to this address instead"
        ),
        gateway=dict(
            type='str', required=False, aliases=['gw'],
            description='For some interface types a gateway is required to configure an '
                        'IP Alias (ppp/pppoe/tun), leave this field empty for all other interface types'
        ),
        password=dict(
            type='str', required=False, aliases=['pwd'],
            description='VHID group password', no_log=True,
        ),
        vhid=dict(
            type='str', required=False, aliases=['group', 'grp', 'id'],
            description='VHID group that the machines will share'
        ),
        advertising_base=dict(
            type='int', required=False, aliases=['adv_base', 'base'], default=1,
            description='The frequency that this machine will advertise. 0 usually means master. '
                        'Otherwise the lowest combination of both values in the cluster determines the master'
        ),
        advertising_skew=dict(
            type='int', required=False, aliases=['adv_skew', 'skew'], default=0,
        ),
        description=dict(type='str', required=False, aliases=['desc']),
        match_fields=dict(
            type='list', required=False, elements='str',
            description='Fields that are used to match configured VIP with the running config - '
                        "if any of those fields are changed, the module will think it's a new entry",
            choices=['address', 'interface', 'cidr', 'description'],
            default=['address', 'interface'],
        ),
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

    module_wrapper(Vip(module=module, result=result))

    result['diff'] = diff_remove_empty(result['diff'])
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
