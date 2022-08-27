#!/usr/bin/python3

# Copyright: (C) 2022, AnsibleGuy <guy@ansibleguy.net>
# GNU General Public License v3.0+ (see https://www.gnu.org/licenses/gpl-3.0.txt)

# see: https://docs.opnsense.org/development/api/plugins/firewall.html

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper import diff_remove_empty
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.defaults import OPN_MOD_ARGS
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.rule_obj import Rule
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.rule_main import process_rule


DOCUMENTATION = 'https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_rule.md'
EXAMPLES = 'https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_rule.md'


def run_module():
    module_args = dict(
        sequence=dict(type='int', required=False, default='1'),
        action=dict(type='str', required=False, default='pass', choices=['pass', 'block', 'reject']),
        interface=dict(type='str', required=False, default='lan'),
        direction=dict(type='str', required=False, default='in', choices=['in', 'out']),
        ip_protocol=dict(
            type='str', required=False, choices=['inet', 'inet6'], default='inet',
            description="IPv4 = 'inet', IPv6 = 'inet6'"
        ),
        protocol=dict(
            type='str', required=False, default='any',
            description="Protocol like 'TCP', 'UDP', 'TCP/UDP' and so on."
        ),
        source_invert=dict(type='bool', required=False, default=False),
        source_net=dict(type='str', required=False, description="Host, network or 'any'"),
        source_port=dict(type='str', required=False, default='', description='Leave empty to allow all'),
        destination_invert=dict(type='bool', required=False, default=False),
        destination_net=dict(type='str', required=False, description="Host, network or 'any'"),
        destination_port=dict(type='str', required=False, default='', description='Leave empty to allow all'),
        gateway=dict(type='str', required=False, default='', description='Existing gateway to use'),
        log=dict(type='bool', required=False, default=True),
        description=dict(type='str', required=False, default=''),
        state=dict(type='str', default='present', required=False, choices=['present', 'absent']),
        enabled=dict(type='bool', required=False, default=True),
        match_fields=dict(
            type='list', required=False, default=[
                'ip_protocol', 'source_invert', 'source_net', 'description'
            ],
            description='Fields that are used to match configured rules with the running config - '
                        "if any of those fields are changed, the module will think it's a new rule",
            choises=[
                'sequence', 'action', 'interface', 'direction', 'ip_protocol', 'protocol',
                'source_invert', 'source_net', 'source_port', 'destination_invert', 'destination_net',
                'destination_port', 'gateway', 'description',
            ]
        ),
        **OPN_MOD_ARGS
    )

    result = dict(
        changed=False,
        diff={
            'before': {},
            'after': {},
        },
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True,
    )

    rule = Rule(module=module, result=result)
    rule.check()

    process_rule(rule=rule)

    rule.s.close()
    result['diff'] = diff_remove_empty(result['diff'])
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
