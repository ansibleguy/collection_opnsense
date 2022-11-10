#!/usr/bin/env python3

# Copyright: (C) 2022, AnsibleGuy <guy@ansibleguy.net>
# GNU General Public License v3.0+ (see https://www.gnu.org/licenses/gpl-3.0.txt)

# see: https://docs.opnsense.org/development/api/plugins/firewall.html

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.handler import \
    module_dependency_error, MODULE_EXCEPTIONS

try:
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.utils import profiler
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.main.rule_purge import process
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.main import diff_remove_empty
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.defaults.main import \
        OPN_MOD_ARGS, PURGE_MOD_ARGS, INFO_MOD_ARG
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.defaults.rule import \
        RULE_MATCH_FIELDS_ARG, RULE_MOD_ARG_KEY_FIELD

except MODULE_EXCEPTIONS:
    module_dependency_error()

PROFILE = False  # create log to profile time consumption

DOCUMENTATION = 'https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_rule_multi.md'
EXAMPLES = 'https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_rule_multi.md'


def run_module():
    module_args = dict(
        rules=dict(
            type='dict', required=False, default={},
            description='Configured rules - compared against existing ones'
        ),
        fail_all=dict(
            type='bool', required=False, default=False, aliases=['fail'],
            description='Fail module if single rule fails the be purged.'
        ),
        **PURGE_MOD_ARGS,
        **INFO_MOD_ARG,
        **RULE_MOD_ARG_KEY_FIELD,
        **RULE_MATCH_FIELDS_ARG,
        **OPN_MOD_ARGS,
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

    if PROFILE or module.params['debug']:
        profiler(
            check=process, kwargs=dict(
                m=module, p=module.params, r=result,
            ),
            log_file='rule_purge.log'  # /tmp/ansibleguy.opnsense/
        )

    else:
        process(m=module, p=module.params, r=result)

    result['diff'] = diff_remove_empty(result['diff'])
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
