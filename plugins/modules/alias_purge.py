#!/usr/bin/python3

# Copyright: (C) 2022, AnsibleGuy <guy@ansibleguy.net>
# GNU General Public License v3.0+ (see https://www.gnu.org/licenses/gpl-3.0.txt)

# see: https://docs.opnsense.org/development/api/core/firewall.html

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.defaults import \
    OPN_MOD_ARGS, PURGE_MOD_ARGS, INFO_MOD_ARG
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper import diff_remove_empty
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.alias_helper import \
    check_purge_configured, simplify_existing_alias, builtin_alias
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.api import Session
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.alias_obj import Alias
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.rule_obj import Rule
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.purge_helper import \
    purge, check_purge_filter

DOCUMENTATION = 'https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_alias_multi.md'
EXAMPLES = 'https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/tests/alias_multi.yml'


def run_module():
    module_args = dict(
        aliases=dict(
            type='dict', required=False, default={},
            description='Configured aliases - compared against existing ones'
        ),
        **INFO_MOD_ARG,
        **PURGE_MOD_ARGS,
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

    session = Session(module=module)
    existing_aliases = Alias(module=module, session=session, result={}).search_call()
    existing_rules = Rule(module=module, session=session, result={}).search_call()
    aliases_to_purge = []

    def obj_func(alias_to_purge: dict) -> Alias:
        if module.params['debug'] or module.params['output_info']:
            module.warn(f"Purging alias '{alias['name']}'!")

        _alias = Alias(
            module=module,
            result={'changed': False, 'diff': {'before': {}, 'after': {}}},
            cnf=alias_to_purge,
            session=session,
        )
        _alias.alias = alias_to_purge
        _alias.existing_rules = existing_rules
        _alias.call_cnf['params'] = [alias_to_purge['uuid']]
        return _alias

    # checking if all aliases should be purged
    if not module.params['force_all'] and len(module.params['aliases']) == 0 and \
            len(module.params['filters']) == 0:
        module.fail_json("You need to either provide 'aliases' or 'filters'!")

    if module.params['force_all'] and len(module.params['aliases']) == 0 and \
            len(module.params['filters']) == 0:
        module.warn('Forced to purge ALL ALIASES!')

        for alias in existing_aliases:
            if not builtin_alias(name=alias['name']):
                purge(
                    module=module, result=result, diff_param='name',
                    obj_func=obj_func, item_to_purge=alias,
                )

    else:
        # checking if existing alias should be purged
        for alias in existing_aliases:
            if not builtin_alias(name=alias['name']):
                alias = simplify_existing_alias(existing=alias)
                to_purge = check_purge_configured(module=module, existing_alias=alias)

                if to_purge:
                    to_purge = check_purge_filter(module=module, item=alias)

                if to_purge:
                    if module.params['debug']:
                        module.warn(
                            f"Existing alias '{alias[module.params['key_field']]}' "
                            f"will be purged!"
                        )

                    aliases_to_purge.append(alias)

        for alias in aliases_to_purge:
            result['changed'] = True
            purge(
                module=module, result=result, diff_param='name',
                obj_func=obj_func, item_to_purge=alias,
            )

    session.close()
    result['diff'] = diff_remove_empty(result['diff'])
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
