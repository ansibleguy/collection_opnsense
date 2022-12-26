#!/usr/bin/env python3

# Copyright: (C) 2022, AnsibleGuy <guy@ansibleguy.net>
# GNU General Public License v3.0+ (see https://www.gnu.org/licenses/gpl-3.0.txt)

# template to be copied to implement new modules

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.handler import \
    module_dependency_error, MODULE_EXCEPTIONS

try:
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.utils import profiler
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.main import \
        diff_remove_empty, sort_param_lists
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.defaults.main import \
        OPN_MOD_ARGS, RELOAD_MOD_ARG, STATE_MOD_ARG
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.main.webproxy_pac_rule import Rule

except MODULE_EXCEPTIONS:
    module_dependency_error()

PROFILE = False  # create log to profile time consumption

DOCUMENTATION = 'https://opnsense.ansibleguy.net/modules/webproxy.html'
EXAMPLES = 'https://opnsense.ansibleguy.net/modules/webproxy.html'


def run_module():
    module_args = dict(
        description=dict(
            type='str', required=True, aliases=['desc', 'name'],
            description='Unique description used to identify existing rules'
        ),
        matches=dict(
            type='list', elements='str', required=False, default=[],
            description='Matches you want to use in this rule. This matches '
                        'are joined using the selected separator',
        ),
        proxies=dict(
            type='list', elements='str', required=False, default=[],
            description='Proxies you want to use address using this rule',
        ),
        join_type=dict(
            type='str', required=False, default='and',
            aliases=['join'], choises=['and', 'or'],
            description="A separator to join the matches. 'or' means any match "
                        'can be true which can be used to configure the same '
                        "proxy for multiple networks while 'and' means all matches "
                        'must be true which can be used to assign the proxy in a '
                        'more detailed way',
        ),
        match_type=dict(
            type='str', required=False, default='if',
            aliases=['operator'], choises=['if', 'unless'],
            description="Choose 'if' in case any case you want to ensure a match to "
                        "evaluate as is, else choose 'unless' if you want the negated "
                        'version. Unless is used if you want to use the proxy for every '
                        'host but not for some special ones',
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

    r = Rule(module=module, result=result)

    def process():
        r.check()
        r.process()
        if result['changed'] and module.params['reload']:
            r.reload()

    if PROFILE or module.params['debug']:
        profiler(check=process, log_file='webproxy_pac_rule.log')
        # log in /tmp/ansibleguy.opnsense/

    else:
        process()

    r.s.close()
    result['diff'] = diff_remove_empty(result['diff'])
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
