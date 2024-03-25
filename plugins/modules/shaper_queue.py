#!/usr/bin/env python3

# Copyright: (C) 2023, AnsibleGuy <guy@ansibleguy.net>
# GNU General Public License v3.0+ (see https://www.gnu.org/licenses/gpl-3.0.txt)

# see: https://docs.opnsense.org/development/api/core/trafficshaper.html

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.handler import \
    module_dependency_error, MODULE_EXCEPTIONS

try:
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.wrapper import module_wrapper
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.main import diff_remove_empty
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.defaults.main import \
        OPN_MOD_ARGS, STATE_MOD_ARG, RELOAD_MOD_ARG
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.main.shaper_queue import Queue

except MODULE_EXCEPTIONS:
    module_dependency_error()


# DOCUMENTATION = 'https://opnsense.ansibleguy.net/en/latest/modules/shaper.html'
# EXAMPLES = 'https://opnsense.ansibleguy.net/en/latest/modules/shaper.html'


def run_module():
    module_args = dict(
        pipe=dict(type='str', required=False),
        mask=dict(
            type='str', required=False, default='none', choices=['none', 'src-ip', 'dst-ip']
        ),
        weight=dict(type='str', required=False),
        buckets=dict(type='str', required=False),
        pie_enable=dict(type='bool', required=False, default=False, aliases=['pie']),
        codel_enable=dict(type='bool', required=False, default=False, aliases=['codel']),
        codel_ecn_enable=dict(type='bool', required=False, default=False, aliases=['codel_ecn']),
        codel_target=dict(type='str', required=False),
        codel_interval=dict(type='int', required=False),
        description=dict(type='str', required=True, aliases=['desc']),
        reset=dict(
            type='bool', required=False, default=False, aliases=['flush'],
            description='If the running config should be flushed and reloaded on change - '
                        'will take some time. This might have impact on other services using '
                        'the same technology underneath (such as Captive portal)'
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

    module_wrapper(Queue(module=module, result=result))

    result['diff'] = diff_remove_empty(result['diff'])
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
