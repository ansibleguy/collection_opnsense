#!/usr/bin/env python3

# Copyright: (C) 2022, AnsibleGuy <guy@ansibleguy.net>
# GNU General Public License v3.0+ (see https://www.gnu.org/licenses/gpl-3.0.txt)

# see: https://docs.opnsense.org/development/api/core/trafficshaper.html

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.handler import \
    module_dependency_error, MODULE_EXCEPTIONS

try:
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.utils import profiler
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.main import \
        diff_remove_empty, sort_param_lists
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.defaults.rule import \
        RULE_MOD_ARG_ALIASES
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.defaults.main import \
        OPN_MOD_ARGS, STATE_MOD_ARG, RELOAD_MOD_ARG
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.main.shaper_rule import Rule

except MODULE_EXCEPTIONS:
    module_dependency_error()

PROFILE = False  # create log to profile time consumption

DOCUMENTATION = 'https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/_tmpl.md'
EXAMPLES = 'https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/_tmpl.md'


def run_module():
    module_args = dict(
        target_pipe=dict(type='str', required=False, default='', aliases=['pipe']),
        target_queue=dict(type='str', required=False, default='', aliases=['queue']),
        sequence=dict(
            type='int', required=False, default=1, aliases=RULE_MOD_ARG_ALIASES['sequence']
        ),
        interface=dict(
            type='str', required=False, default='lan', aliases=RULE_MOD_ARG_ALIASES['interface'],
            description='Matching packets traveling to/from interface',
        ),
        interface2=dict(
            type='str', required=False, default='', aliases=['int2', 'i2'],
            description='Secondary interface, matches packets traveling to/from interface '
                        '(1) to/from interface (2). can be combined with direction.',
        ),
        protocol=dict(
            type='str', required=False, default='ip', aliases=RULE_MOD_ARG_ALIASES['protocol'],
            description="Protocol like 'ip', 'ipv4', 'tcp', 'udp' and so on."
        ),
        max_packet_length=dict(
            type='str', required=False, default='', aliases=['max_packet_len', 'packet_len', 'iplen'],
        ),
        source_invert=dict(
            type='bool', required=False, default=False,
            aliases=RULE_MOD_ARG_ALIASES['source_invert'],
        ),
        source_net=dict(
            type='str', required=False, default='any', aliases=RULE_MOD_ARG_ALIASES['source_net'],
            description="Source ip or network, examples 10.0.0.0/24, 10.0.0.1"
        ),
        source_port=dict(
            type='str', required=False, default='any', aliases=RULE_MOD_ARG_ALIASES['source_port'],
        ),
        destination_invert=dict(
            type='bool', required=False, default=False,
            aliases=RULE_MOD_ARG_ALIASES['destination_invert'],
        ),
        destination_net=dict(
            type='str', required=False, default='any', aliases=RULE_MOD_ARG_ALIASES['destination_net'],
            description='Destination ip or network, examples 10.0.0.0/24, 10.0.0.1'
        ),
        destination_port=dict(
            type='str', required=False, default='any',
            aliases=RULE_MOD_ARG_ALIASES['destination_port'],
        ),
        dscp=dict(
            type='list', required=False, elements='str', default=[],
            description='One or multiple DSCP values',
            choises=[
                'be', 'ef', 'af11', 'af12', 'af13', 'af21', 'af22', 'af23', 'af31', 'af32', 'af33',
                'af41', 'af42', 'af43', 'cs1', 'cs2', 'cs3', 'cs4', 'cs5', 'cs6', 'cs7',
            ]
        ),
        direction=dict(
            type='str', required=False, default='', aliases=RULE_MOD_ARG_ALIASES['direction'],
            choices=['', 'in', 'out'], description='Leave empty for both'
        ),
        description=dict(type='str', required=True, aliases=['desc']),
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

    sort_param_lists(module.params)
    rule = Rule(module=module, result=result)

    def process():
        rule.check()
        rule.process()
        if result['changed'] and module.params['reload']:
            rule.reload()

    if PROFILE or module.params['debug']:
        profiler(check=process, log_file='shaper_rule.log')
        # log in /tmp/ansibleguy.opnsense/

    else:
        process()

    rule.s.close()
    result['diff'] = diff_remove_empty(result['diff'])
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
