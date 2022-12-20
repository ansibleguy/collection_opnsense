#!/usr/bin/env python3

# Copyright: (C) 2022, AnsibleGuy <guy@ansibleguy.net>
# GNU General Public License v3.0+ (see https://www.gnu.org/licenses/gpl-3.0.txt)

# see: https://docs.opnsense.org/development/api/core/unbound.html

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.handler import \
    module_dependency_error, MODULE_EXCEPTIONS

try:
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.utils import profiler
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.main import diff_remove_empty
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.defaults.main import \
        OPN_MOD_ARGS, STATE_MOD_ARG, RELOAD_MOD_ARG
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.main.unbound_domain import Domain

except MODULE_EXCEPTIONS:
    module_dependency_error()

PROFILE = False  # create log to profile time consumption

DOCUMENTATION = 'https://opnsense.ansibleguy.net/modules/unbound_domain.html'
EXAMPLES = 'https://opnsense.ansibleguy.net/modules/unbound_domain.html'


def run_module():
    module_args = dict(
        domain=dict(type='str', required=True, aliases=['dom', 'd']),
        server=dict(type='str', required=True, aliases=['value', 'srv']),
        description=dict(type='str', required=False, default='', aliases=['desc']),
        match_fields=dict(
            type='list', required=False, elements='str',
            description='Fields that are used to match configured domain-overrides with the running config - '
                        "if any of those fields are changed, the module will think it's a new entry",
            choises=['domain', 'server', 'description'],
            default=['domain', 'server'],
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

    dom = Domain(module=module, result=result)

    def process():
        dom.check()
        dom.process()
        if result['changed'] and module.params['reload']:
            dom.reload()

    if PROFILE or module.params['debug']:
        profiler(check=process, log_file='unbound_domain.log')
        # log in /tmp/ansibleguy.opnsense/

    else:
        process()

    dom.s.close()
    result['diff'] = diff_remove_empty(result['diff'])
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
