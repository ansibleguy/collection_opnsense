#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (C) 2026, Pascal Rath <contact+opnsense@OXL.at>
# GNU General Public License v3.0+ (see https://www.gnu.org/licenses/gpl-3.0.txt)

# see: https://docs.opnsense.org/development/api/core/radvd.html

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.handler import \
    module_dependency_error, MODULE_EXCEPTIONS

try:
    from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.wrapper import module_wrapper
    from ansible_collections.oxlorg.opnsense.plugins.module_utils.defaults.main import \
        OPN_MOD_ARGS, STATE_MOD_ARG, RELOAD_MOD_ARG
    from ansible_collections.oxlorg.opnsense.plugins.module_utils.main.radvd import Radvd

except MODULE_EXCEPTIONS:
    module_dependency_error()


# DOCUMENTATION = 'https://ansible-opnsense.oxl.app/modules/radvd.html'
# EXAMPLES = 'https://ansible-opnsense.oxl.app/modules/radvd.html'


def run_module():
    module_args = dict(
        interface=dict(
            type='str', required=True,
            description='Interface that should send router advertisements.',
        ),
        base6_interface=dict(
            type='str', required=False, default='',
            description='Optional constructor interface for the advertised prefix.',
        ),
        mode=dict(
            type='str', required=False, default='stateless',
            choices=['router', 'unmanaged', 'managed', 'assist', 'stateless'],
        ),
        deprecate_prefix=dict(
            type='str', required=False, default='',
            choices=['', 'on', 'off'],
        ),
        remove_adv_on_exit=dict(
            type='str', required=False, default='',
            choices=['', 'on', 'off'],
        ),
        remove_route=dict(
            type='str', required=False, default='',
            choices=['', 'on', 'off'],
        ),
        routes=dict(type='list', elements='str', required=False, default=[]),
        rdnss=dict(type='list', elements='str', required=False, default=[]),
        dnssl=dict(type='list', elements='str', required=False, default=[]),
        dns=dict(type='bool', required=False, default=True),
        min_rtr_adv_interval=dict(type='int', required=False, default=200),
        max_rtr_adv_interval=dict(type='int', required=False, default=600),
        adv_dnssl_lifetime=dict(type='int', required=False),
        adv_default_lifetime=dict(type='int', required=False),
        adv_link_mtu=dict(type='int', required=False),
        adv_preferred_lifetime=dict(type='int', required=False),
        adv_ra_src_address=dict(type='str', required=False, default=''),
        adv_rdnss_lifetime=dict(type='int', required=False),
        adv_route_lifetime=dict(type='int', required=False),
        adv_valid_lifetime=dict(type='int', required=False),
        adv_default_preference=dict(
            type='str', required=False, default='medium',
            choices=['low', 'medium', 'high'],
        ),
        nat64prefix=dict(type='str', required=False),
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

    module_wrapper(Radvd(module=module, result=result))
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
