from ansible_collections.ansibleguy.opnsense.plugins.module_utils.rule_obj import Rule


def process_rule(rule: Rule):
    if rule.cnf['state'] == 'absent':
        if rule.exists:
            rule.delete()

    else:
        if rule.exists:
            rule.update()

        else:
            rule.create()
