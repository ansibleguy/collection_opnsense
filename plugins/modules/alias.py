#!/usr/bin/python3

# Copyright: (C) 2022, AnsibleGuy <guy@ansibleguy.net>
# GNU General Public License v3.0+ (see https://www.gnu.org/licenses/gpl-3.0.txt)

# see: https://docs.opnsense.org/development/api/core/firewall.html

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.handler import \
    module_dependency_error, MODULE_EXCEPTIONS

try:
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.defaults import RELOAD_MOD_ARG_DEF_FALSE
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper import diff_remove_empty
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.alias_obj import Alias
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.alias_defaults import ALIAS_MOD_ARGS

except MODULE_EXCEPTIONS:
    module_dependency_error()

DOCUMENTATION = 'https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_alias.md'
EXAMPLES = 'https://github.com/ansibleguy/collection_opnsense/blob/stable/tests/alias.yml'


def run_module():
    module_args = dict(
        **RELOAD_MOD_ARG_DEF_FALSE,  # default-true takes pretty long sometimes (urltables and so on)
        **ALIAS_MOD_ARGS
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
    alias.check()
    alias.process()
    if result['changed'] and module.params['reload']:
        alias.reload()

    alias.s.close()
    result['diff'] = diff_remove_empty(result['diff'])
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
