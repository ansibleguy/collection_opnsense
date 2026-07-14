#!/usr/bin/python
# -*- coding: utf-8 -*-

# GNU General Public License v3.0+ (see https://www.gnu.org/licenses/gpl-3.0.txt)

# see: https://docs.opnsense.org/development/api/core/firewall.html

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.handler import \
    module_dependency_error, MODULE_EXCEPTIONS

try:
    from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.wrapper import module_wrapper
    from ansible_collections.oxlorg.opnsense.plugins.module_utils.defaults.rule import \
        RULE_MOD_ARGS
    from ansible_collections.oxlorg.opnsense.plugins.module_utils.defaults.main import \
        OPN_MOD_ARGS, STATE_MOD_ARG, RELOAD_MOD_ARG
    from ansible_collections.oxlorg.opnsense.plugins.module_utils.main.nat_destination import DNat

except MODULE_EXCEPTIONS:
    module_dependency_error()


# DOCUMENTATION = 'https://ansible-opnsense.oxl.app/modules/nat_destination.html'
# EXAMPLES = 'https://ansible-opnsense.oxl.app/modules/nat_destination.html'


def run_module():
    shared_rule_args = {
        'sequence': RULE_MOD_ARGS['sequence'],
        'interface': RULE_MOD_ARGS['interface'],
        'ip_protocol': RULE_MOD_ARGS['ip_protocol'],
        'protocol': RULE_MOD_ARGS['protocol'],
        'source_invert': RULE_MOD_ARGS['source_invert'],
        'source_net': RULE_MOD_ARGS['source_net'],
        'source_port': RULE_MOD_ARGS['source_port'],
        'destination_invert': RULE_MOD_ARGS['destination_invert'],
        'destination_net': RULE_MOD_ARGS['destination_net'],
        'destination_port': RULE_MOD_ARGS['destination_port'],
        'log': RULE_MOD_ARGS['log'],
        'uuid': RULE_MOD_ARGS['uuid'],
        'description': RULE_MOD_ARGS['description'],
        'tag': RULE_MOD_ARGS['tag'],
        'tagged': RULE_MOD_ARGS['tagged'],
    }

    module_args = dict(
        no_port_forward=dict(
            type='bool', required=False, default=False, aliases=['nordr'],
            description='Packets matching this rule will be passed without a port-forward '
                        'being applied - useful to define exceptions on top of a more general rule.'
        ),
        target=dict(
            type='str', required=False, aliases=['tgt', 't'],
            description='NAT translation target - IP-Address or alias the matching traffic will be '
                        'redirected to. Grouped aliases (with multiple entries) can be used for load-balancing.'
        ),
        local_port=dict(
            type='str', required=False, aliases=['nat_port', 'np'],
            description='Port the packet will be redirected to - port-number, well-known name or alias'
        ),
        pool_opts=dict(
            type='str', required=False, default='', aliases=['pool_options'],
            choices=[
                '', 'round-robin', 'round-robin sticky-address', 'random',
                'random sticky-address', 'source-hash', 'bitmask',
            ],
            description="Only used if 'target' resolves to multiple entries (load-balancing pool). "
                        "Empty value uses the system default."
        ),
        nat_reflection=dict(
            type='str', required=False, default='', choices=['', 'purenat', 'disable'],
            description="Empty value uses the system default."
        ),
        associated_rule=dict(
            type='str', required=False, default='', choices=['', 'pass', 'rule'], aliases=['pass'],
            description="Whether and how a matching firewall-rule should be created for this port-forward. "
                        "Empty = manual (you have to create the matching filter-rule yourself), "
                        "'pass' = automatically allow the redirected traffic, "
                        "'rule' = register an associated but separately editable filter-rule."
        ),
        match_fields=dict(
            type='list', required=True, elements='str',
            description='Fields that are used to match configured rules with the running config - '
                        "if any of those fields are changed, the module will think it's a new rule",
            choices=[
                'sequence', 'interface', 'ip_protocol', 'protocol', 'source_invert', 'source_net',
                'source_port', 'destination_invert', 'destination_net', 'destination_port',
                'target', 'local_port', 'description', 'uuid', 'no_port_forward',
            ]
        ),
        **shared_rule_args,
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

    module_wrapper(DNat(module=module, result=result))
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
