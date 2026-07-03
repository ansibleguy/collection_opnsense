#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (C) 2025, Pascal Rath <contact+opnsense@OXL.at>
# GNU General Public License v3.0+ (see https://www.gnu.org/licenses/gpl-3.0.txt)

# see: https://docs.opnsense.org/development/api/core/interfaces.html

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.handler import \
    module_dependency_error, MODULE_EXCEPTIONS

try:
    from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.wrapper import module_wrapper
    from ansible_collections.oxlorg.opnsense.plugins.module_utils.defaults.main import \
        OPN_MOD_ARGS, STATE_ONLY_MOD_ARG, RELOAD_MOD_ARG
    from ansible_collections.oxlorg.opnsense.plugins.module_utils.main.interface_vip import Vip

except MODULE_EXCEPTIONS:
    module_dependency_error()


# DOCUMENTATION = 'https://ansible-opnsense.oxl.app/modules/interface.html'
# EXAMPLES = 'https://ansible-opnsense.oxl.app/modules/interface.html'


def run_module():
    module_args = dict(
        address=dict(
            type='str', required=True, aliases=['addr', 'ip', 'net', 'network'],
            description='Provide an IP-address to use.',
        ),
        # network=dict(
        #     type='str', required=False, aliases=['net'],
        #     description='Provide the network-subnet to use.',
        # ),
        # network_cidr=dict(
        #     type='int', required=False, aliases=['cidr'],
        #     description='Provide the network-subnet-cidr to use.',
        # ),
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
        peer=dict(
            type='str', required=False,
            description='Destination address to use when announcing, defaults to multicast, '
                        'but can be configured as unicast address when multicast can not be '
                        'used (for example with cloud providers)'
        ),
        peer6=dict(
            type='str', required=False,
            description='Destination address to use when announcing, defaults to multicast, '
                        'but can be configured as unicast address when multicast can not be '
                        'used (for example with cloud providers)'
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
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
