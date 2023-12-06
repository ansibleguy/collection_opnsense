#!/usr/bin/env python3

# Copyright: (C) 2023, AnsibleGuy <guy@ansibleguy.net>
# GNU General Public License v3.0+ (see https://www.gnu.org/licenses/gpl-3.0.txt)

# see: https://docs.opnsense.org/development/api/core/ids.html

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.handler import \
    module_dependency_error, MODULE_EXCEPTIONS

try:
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.defaults.main import \
        OPN_MOD_ARGS
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.api import \
        single_get, single_post

except MODULE_EXCEPTIONS:
    module_dependency_error()

PROFILE = False  # create log to profile time consumption

# DOCUMENTATION = 'https://opnsense.ansibleguy.net/en/latest/modules/ids.html'
# EXAMPLES = 'https://opnsense.ansibleguy.net/en/latest/modules/ids.html'

ACTION_MAPPING = {
    'get_alert_info': {'a': 'getAlertInfo', 'post': False},
    'get_alert_logs': {'a': 'getAlertLogs', 'post': False},
    'query_alerts': {'a': 'queryAlerts', 'post': False},
    'status': {'post': False},
    'reconfigure': {'post': True},
    'restart': {'post': True},
    'start': {'post': True},
    'stop': {'post': True},
    'drop_alert_log': {'a': 'dropAlertLog', 'post': True},
    'reload_rules': {'a': 'reloadRules', 'post': True},
    'update_rules': {'a': 'updateRules', 'post': True},
}

def run_module():
    module_args = dict(
        action=dict(
            type='str', required=True, aliases=['do', 'a'],
            choices=[
                'get_alert_logs', 'query_alerts', 'get_alert_info', 'status',
                'reconfigure', 'restart', 'start', 'stop',
                'drop_alert_log', 'reload_rules', 'update_rules',
            ],
        ),
        parameter=dict(
            type='str', required=False, aliases=['param'],
            description="Parameter Alert-ID needed for 'get_alert_info'",
        ),
        **OPN_MOD_ARGS,
    )

    result = dict(
        changed=False,
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True,
    )

    action = module.params['action']
    if action == 'get_alert_info' and module.params['parameter'] is None:
        module.fail_json("You need to provide an Alert-ID as 'parameter' to execute 'get_alert_info'!")

    # translate actions to api-commands
    cmd = action
    if 'a' in ACTION_MAPPING[action]:
        cmd = ACTION_MAPPING[action]['a']

    result['executed'] = cmd

    # execute action or pull status
    if ACTION_MAPPING[action]['post']:
        result['changed'] = True

        if not module.check_mode:
            single_post(
                module=module,
                cnf={
                    'module': 'ids',
                    'controller': 'service',
                    'command': cmd,
                }
            )

    else:
        params = []
        if module.params['parameter'] is not None:
            params = [module.params['parameter']]

        info = single_get(
            module=module,
            cnf={
                'module': 'ids',
                'controller': 'service',
                'command': cmd,
                'params': params,
            }
        )

        if 'response' in info:
            info = info['response']

            if isinstance(info, str):
                info = info.strip()

        result['data'] = info

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
