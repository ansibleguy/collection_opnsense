#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (C) 2025, Pascal Rath <contact+opnsense@OXL.at>
# GNU General Public License v3.0+ (see https://www.gnu.org/licenses/gpl-3.0.txt)

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.handler import \
    module_dependency_error, MODULE_EXCEPTIONS

try:
    from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.wrapper import module_wrapper
    from ansible_collections.oxlorg.opnsense.plugins.module_utils.defaults.rule import \
        RULE_MOD_ARGS, RULE_MOD_ARG_ALIASES
    from ansible_collections.oxlorg.opnsense.plugins.module_utils.defaults.main import \
        OPN_MOD_ARGS, STATE_MOD_ARG, RELOAD_MOD_ARG
    from ansible_collections.oxlorg.opnsense.plugins.module_utils.main.nat_one_to_one import OneToOne

except MODULE_EXCEPTIONS:
    module_dependency_error()


# DOCUMENTATION = 'https://ansible-opnsense.oxl.app/modules/nat_one_to_one.html'
# EXAMPLES = 'https://ansible-opnsense.oxl.app/modules/nat_one_to_one.html'


def run_module():
    shared_rule_args = {
        'log': RULE_MOD_ARGS['log'],
        'sequence': RULE_MOD_ARGS['sequence'],
        'source_net': RULE_MOD_ARGS['source_net'],
        'source_invert': RULE_MOD_ARGS['source_invert'],
        'destination_net': RULE_MOD_ARGS['destination_net'],
        'destination_invert': RULE_MOD_ARGS['destination_invert'],
        'categories': RULE_MOD_ARGS['categories'],
        'description': RULE_MOD_ARGS['description'],
        'uuid': RULE_MOD_ARGS['uuid'],
    }

    module_args = dict(
        interface=dict(
            type='str', required=False, aliases=RULE_MOD_ARG_ALIASES['interface'],
            description='Interfaces use this rule on',
        ),
        type=dict(
            type='str', required=False, choices=['binat', 'nat'], default='binat',
            description='Select `binat` (default) or `nat`. When nets are equally sized binat is usually the '
                        'best option. Using NAT we can also map unequal sized networks. A BINAT rule specifies a '
                        'bidirectional mapping between an external and internal network and can be used from both '
                        'ends, nat only applies in one direction.',
        ),
        external=dict(
            type='str', required=False, aliases=['external_net', 'ext', 'e'],
            description='The external subnet\'s starting address for the 1:1 mapping or network. This is the address '
                        'or network the traffic will translate to/from.'
        ),
        nat_reflection=dict(type='str', required=False, choices=['enable', 'disable'], aliases=['natreflection']),
        match_fields=dict(
            type='list', required=False, elements='str',
            description='Fields that are used to match configured rules with the running config - '
                        "if any of those fields are changed, the module will think it's a new rule",
            choices=[
                'sequence', 'interface', 'source_net', 'source_invert', 'destination_net', 'destination_invert',
                'description', 'uuid', 'type', 'external', 'nat_reflection',
            ],
            default=['interface', 'external']
        ),
        **shared_rule_args,
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
        required_if=[
            ('ensure', 'present', ('interface', 'external', )),
        ],
    )

    module_wrapper(OneToOne(module=module, result=result))
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
