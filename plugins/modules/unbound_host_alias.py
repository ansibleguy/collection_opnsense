#!/usr/bin/python3

# Copyright: (C) 2022, AnsibleGuy <guy@ansibleguy.net>
# GNU General Public License v3.0+ (see https://www.gnu.org/licenses/gpl-3.0.txt)

# see: https://docs.opnsense.org/development/api/core/unbound.html

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.handler import \
    module_dependency_error, MODULE_EXCEPTIONS

try:
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.utils import profiler
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper import diff_remove_empty
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.defaults import \
        OPN_MOD_ARGS, STATE_MOD_ARG, RELOAD_MOD_ARG
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.unbound_host_alias_obj import Alias

except MODULE_EXCEPTIONS:
    module_dependency_error()

PROFILE = False  # create log to profile time consumption

DOCUMENTATION = 'https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_unbound_host_alias.md'
EXAMPLES = 'https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_unbound_host_alias.md'


def run_module():
    module_args = dict(
        alias=dict(type='str', required=True, aliases=['hostname']),
        domain=dict(type='str', required=True, aliases=['dom', 'd']),
        target=dict(type='str', required=True, aliases=['tgt', 'host']),
        description=dict(type='str', required=False, default='', aliases=['desc']),
        match_fields=dict(
            type='list', required=False, elements='str',
            description='Fields that are used to match configured override-alias with the running config - '
                        "if any of those fields are changed, the module will think it's a new entry",
            choises=['hostname', 'domain', 'alias',  'description'],
            default=['alias', 'domain'],
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

    alias = Alias(module=module, result=result)

    def process():
        alias.check()
        alias.process()
        if result['changed'] and module.params['reload']:
            alias.reload()

    if PROFILE or module.params['debug']:
        profiler(check=process, log_file='unbound_host_alias.log')
        # log in /tmp/ansibleguy.opnsense/

    else:
        process()

    alias.s.close()
    result['diff'] = diff_remove_empty(result['diff'])
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
