#!/usr/bin/env python3

# Copyright: (C) 2023, AnsibleGuy <guy@ansibleguy.net>
# GNU General Public License v3.0+ (see https://www.gnu.org/licenses/gpl-3.0.txt)

# see: https://docs.opnsense.org/development/api/plugins/firewall.html

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.handler import \
    module_dependency_error, MODULE_EXCEPTIONS

try:
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.utils import profiler
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.main import diff_remove_empty
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.defaults.rule import \
        RULE_MOD_ARGS
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.defaults.main import \
        OPN_MOD_ARGS, STATE_MOD_ARG, RELOAD_MOD_ARG
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.main.source_nat import SNat

except MODULE_EXCEPTIONS:
    module_dependency_error()

PROFILE = False  # create log to profile time consumption

# DOCUMENTATION = 'https://opnsense.ansibleguy.net/en/latest/modules/source_nat.html'
# EXAMPLES = 'https://opnsense.ansibleguy.net/en/latest/modules/source_nat.html'


def run_module():
    shared_rule_args = {
        'sequence': RULE_MOD_ARGS['sequence'],
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
    }

    module_args = dict(
        no_nat=dict(
            type='bool', required=False, default=False,
            description='Enabling this option will disable NAT for traffic matching '
                        'this rule and stop processing Outbound NAT rules.'
        ),
        interface=dict(type='str', required=False, aliases=['int', 'i']),
        target=dict(
            type='str', required=False, aliases=['tgt', 't'],
            description='NAT translation target - Packets matching this rule will be '
                        'mapped to the IP address given here.',
        ),
        target_port=dict(type='str', required=False, aliases=['nat_port', 'np'], default=''),
        match_fields=dict(
            type='list', required=True, elements='str',
            description='Fields that are used to match configured rules with the running config - '
                        "if any of those fields are changed, the module will think it's a new rule",
            choices=[
                'sequence', 'interface', 'target', 'target_port', 'ip_protocol', 'protocol',
                'source_invert', 'source_net', 'source_port', 'destination_invert', 'destination_net',
                'destination_port', 'description', 'uuid',
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

    snat = SNat(module=module, result=result)

    def process():
        snat.check()
        snat.process()
        if result['changed'] and module.params['reload']:
            snat.reload()

    if PROFILE or module.params['debug']:
        profiler(check=process, log_file='source_nat.log')
        # log in /tmp/ansibleguy.opnsense/

    else:
        process()

    snat.s.close()
    result['diff'] = diff_remove_empty(result['diff'])
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
