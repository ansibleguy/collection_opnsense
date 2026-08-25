#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (C) 2026, Pascal Rath <contact+opnsense@OXL.at>
# GNU General Public License v3.0+ (see https://www.gnu.org/licenses/gpl-3.0.txt)

# see: https://docs.opnsense.org/development/api/core/kea.html

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.handler import \
    module_dependency_error, MODULE_EXCEPTIONS

try:
    from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.wrapper import module_wrapper
    from ansible_collections.oxlorg.opnsense.plugins.module_utils.defaults.main import \
        OPN_MOD_ARGS, STATE_MOD_ARG, RELOAD_MOD_ARG
    from ansible_collections.oxlorg.opnsense.plugins.module_utils.main.kea_dhcp4_option import Dhcpv4Option

except MODULE_EXCEPTIONS:
    module_dependency_error()


# DOCUMENTATION = 'https://ansible-opnsense.oxl.app/modules/dhcp.html'
# EXAMPLES = 'https://ansible-opnsense.oxl.app/modules/dhcp.html'

ENCODING_CHOICES = [
    'hex', 'ipv4-address', 'ipv6-address', 'uint8', 'uint16',
    'uint32', 'int32', 'boolean', 'string', 'fqdn',
]


def run_module():
    module_args = dict(
        code=dict(
            type='str', required=False, default='',
            description='DHCP option code.',
        ),
        encoding=dict(
            type='str', required=False, default='hex', choices=ENCODING_CHOICES,
            description='Encoding used for option data.',
        ),
        data=dict(
            type='str', required=False, default='',
            description='Option data encoded according to the selected encoding.',
        ),
        force=dict(
            type='bool', required=False, default=False, aliases=['always_send'],
            description='Always send this option to clients.',
        ),
        match_code=dict(
            type='str', required=False, default='',
            description='Optional DHCP option code that must match before sending this option.',
        ),
        match_encoding=dict(
            type='str', required=False, default='', choices=['', *ENCODING_CHOICES],
            description='Encoding used for match data.',
        ),
        match_data=dict(
            type='str', required=False, default='',
            description='Optional option data that must match before sending this option.',
        ),
        description=dict(
            type='str', required=True, aliases=['name', 'desc'],
            description='Unique description for this DHCPv4 option definition.',
        ),
        match_fields=dict(
            type='list', required=False, elements='str',
            description='Fields that are used to match configured option with the running config - '
                        "if any of those fields are changed, the module will think it's a new entry",
            choices=['code', 'description'],
            default=['description'],
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

    module_wrapper(Dhcpv4Option(module=module, result=result))
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
