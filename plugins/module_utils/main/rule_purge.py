from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.main import is_unset
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.purge import \
    purge, check_purge_filter
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.rule import \
    check_purge_configured
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.api import Session
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.main.rule import Rule


def process(m: AnsibleModule, p: dict, r: dict):
    s = Session(module=m)
    existing_rules = Rule(module=m, session=s, result={}).get_existing()
    rules_to_purge = []

    def obj_func(rule_to_purge: dict) -> Rule:
        if 'debug' not in rule_to_purge:
            rule_to_purge['debug'] = p['debug']

        if rule_to_purge['debug'] or p['output_info']:
            m.warn(f"Purging rule '{rule_to_purge[p['key_field']]}'!")

        _rule = Rule(
            module=m,
            result={'changed': False, 'diff': {'before': {}, 'after': {}}},
            cnf=rule_to_purge,
            session=s,
            fail_verify=p['fail_all'],
            fail_proc=p['fail_all'],
        )
        _rule.rule = rule_to_purge
        _rule.call_cnf['params'] = [rule_to_purge['uuid']]
        return _rule

    # checking if all rules should be purged
    if not p['force_all'] and is_unset(p['rules']) and \
            is_unset(p['filters']):
        m.fail_json("You need to either provide 'rules' or 'filters'!")

    if len(existing_rules) > 0:
        if p['force_all'] and is_unset(p['rules']) and \
                is_unset(p['filters']):
            m.warn('Forced to purge ALL RULES!')

            for existing_rule in existing_rules:
                purge(
                    module=m, result=r, obj_func=obj_func,
                    diff_param=p['key_field'],
                    item_to_purge=existing_rule,
                )

        else:
            # checking if existing rule should be purged
            for existing_rule in existing_rules:
                to_purge = check_purge_configured(module=m, existing_rule=existing_rule)

                if to_purge:
                    to_purge = check_purge_filter(module=m, item=existing_rule)

                if to_purge:
                    if p['debug']:
                        m.warn(
                            f"Existing rule '{existing_rule[p['key_field']]}' "
                            f"will be purged!"
                        )

                    rules_to_purge.append(existing_rule)

            for rule in rules_to_purge:
                r['changed'] = True
                purge(
                    module=m, result=r, diff_param=p['key_field'],
                    obj_func=obj_func, item_to_purge=rule
                )

    s.close()
