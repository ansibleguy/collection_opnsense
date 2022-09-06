#!/usr/bin/python3

# Copyright: (C) 2022, AnsibleGuy <guy@ansibleguy.net>
# GNU General Public License v3.0+ (see https://www.gnu.org/licenses/gpl-3.0.txt)

# see: https://docs.opnsense.org/development/api/plugins/firewall.html

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper import diff_remove_empty
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.defaults import \
    OPN_MOD_ARGS, PURGE_MOD_ARGS, INFO_MOD_ARG
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.rule_defaults import \
    RULE_MATCH_FIELDS_ARG, RULE_MOD_ARG_KEY_FIELD
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.rule_helper import \
    simplify_existing_rule, check_purge_configured
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.api import Session
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.rule_obj import Rule
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.purge_helper import \
    purge, check_purge_filter

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

    session = Session(module=module)
    existing_rules = Rule(module=module, session=session, result={}).search_call()
    rules_to_purge = []

    def obj_func(rule_to_purge: dict) -> Rule:
        if module.params['debug'] or module.params['output_info']:
            module.warn(f"Purging rule '{rule_to_purge[module.params['key_field']]}'!")

        _rule = Rule(
            module=module,
            result={'changed': False, 'diff': {'before': {}, 'after': {}}},
            cnf=rule_to_purge,
            session=session,
            fail=module.params['fail_all']
        )
        _rule.rule = rule_to_purge
        _rule.call_cnf['params'] = [rule_to_purge['uuid']]
        return _rule

    # checking if all rules should be purged
    if not module.params['force_all'] and len(module.params['rules']) == 0 and \
            len(module.params['filters']) == 0:
        module.fail_json("You need to either provide 'rules' or 'filters'!")

    if module.params['force_all'] and len(module.params['rules']) == 0 and \
            len(module.params['filters']) == 0:
        module.warn('Forced to purge ALL RULES!')

        for uuid, raw_existing_rule in existing_rules.items():
            purge(
                module=module, result=result, obj_func=obj_func,
                diff_param=module.params['key_field'],
                item_to_purge=simplify_existing_rule(rule={uuid: raw_existing_rule}),
            )

    else:
        # checking if existing rule should be purged
        for uuid, raw_existing_rule in existing_rules.items():
            existing_rule = simplify_existing_rule(rule={uuid: raw_existing_rule})
            to_purge = check_purge_configured(module=module, existing_rule=existing_rule)

            if to_purge:
                to_purge = check_purge_filter(module=module, item=existing_rule)

            if to_purge:
                if module.params['debug']:
                    module.warn(
                        f"Existing rule '{existing_rule[module.params['key_field']]}' "
                        f"will be purged!"
                    )

                rules_to_purge.append(existing_rule)

        for rule in rules_to_purge:
            result['changed'] = True
            purge(
                module=module, result=result, diff_param=module.params['key_field'],
                obj_func=obj_func, item_to_purge=rule
            )

    session.close()
    result['diff'] = diff_remove_empty(result['diff'])
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
