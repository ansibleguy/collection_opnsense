#!/usr/bin/env python3

# Copyright: (C) 2023, AnsibleGuy <guy@ansibleguy.net>
# GNU General Public License v3.0+ (see https://www.gnu.org/licenses/gpl-3.0.txt)

# see: https://docs.opnsense.org/development/api/plugins/quagga.html

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.handler import \
    module_dependency_error, MODULE_EXCEPTIONS

try:
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.utils import profiler
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.main import \
        diff_remove_empty
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.defaults.main import \
        OPN_MOD_ARGS, EN_ONLY_MOD_ARG, RELOAD_MOD_ARG
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.main.frr_general import General

except MODULE_EXCEPTIONS:
    module_dependency_error()

PROFILE = False  # create log to profile time consumption

# DOCUMENTATION = 'https://opnsense.ansibleguy.net/en/latest/modules/frr_general.html'
# EXAMPLES = 'https://opnsense.ansibleguy.net/en/latest/modules/frr_general.html'


def run_module():
    module_args = dict(
        carp=dict(
            type='bool', required=False, default=False, aliases=['carp_failover'],
            description='Will activate the routing service only on the primary device'
        ),
        profile=dict(
            type='str', required=False, default='traditional',
            options=['traditional', 'datacenter'],
            description="The 'datacenter' profile is more aggressive. "
                        "Please refer to the FRR documentation for more information"
        ),
        snmp_agentx=dict(
            type='bool', required=False, default=False,
            description='En- or disable support for Net-SNMP AgentX'
        ),
        log=dict(
            type='bool', required=False, default=True, aliases=['logging'],
        ),
        log_level=dict(
            type='str', required=False, default='notifications',
            options=[
                'critical', 'emergencies', 'errors', 'alerts', 'warnings', 'notifications',
                'informational', 'debugging',
            ],
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

    g = General(module=module, result=result)

    def process():
        g.check()
        g.process()
        if result['changed'] and module.params['reload']:
            g.reload()

    if PROFILE or module.params['debug']:
        profiler(check=process, log_file='frr_general.log')
        # log in /tmp/ansibleguy.opnsense/

    else:
        process()

    g.s.close()
    result['diff'] = diff_remove_empty(result['diff'])
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
