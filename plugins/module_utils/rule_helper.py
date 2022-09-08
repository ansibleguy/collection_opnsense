import validators

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper import \
    get_selected, get_selected_list, is_true


def get_rule(rules: (list, dict), cnf: dict) -> dict:
    rule = {}

    if len(rules) > 0:
        for uuid, values in rules.items():
            existing = simplify_existing_rule(rule={uuid: values})
            if check_for_matching_rule(existing=existing, cnf=cnf):
                rule = existing
                break

    return rule


def check_for_matching_rule(existing: dict, cnf: dict) -> bool:
    _matching = []

    for field in cnf['match_fields']:
        _matching.append(str(existing[field]) == str(cnf[field]))

    return all(_matching)


def simplify_existing_rule(rule: dict) -> dict:
    # because the return of api/firewall/filter/get is too verbose for easy access
    simple = {}

    copy_fields = [
        'sequence', 'source_net', 'source_not', 'source_port', 'destination_net',
        'destination_not', 'destination_port', 'description'
    ]

    for uuid, values in rule.items():
        simple = {
            'uuid': uuid,
            'enabled': is_true(values['enabled']),
            'log': is_true(values['log']),
            'quick': is_true(values['quick']),
            'source_invert': is_true(values['source_not']),
            'destination_invert': is_true(values['destination_not']),
            'action': get_selected(data=values['action']),
            'interface': get_selected_list(data=values['interface']),
            'direction': get_selected(data=values['direction']),
            'ip_protocol': get_selected(data=values['ipprotocol']),
            'protocol': get_selected(data=values['protocol']),
            'gateway': get_selected(data=values['gateway']),
        }

        for field in copy_fields:
            simple[field] = values[field]

    return simple


def validate_values(error_func, module: AnsibleModule, cnf: dict) -> None:
    error = "Value '%s' is invalid for the field '%s'!"

    # can't validate as aliases are supported
    # for field in ['source_net', 'destination_net']:
    #     if cnf[field] not in [None, '', 'any']:
    #         try:
    #             ip_network(cnf[field])
    #
    #         except ValueError:
    #             try:
    #                 ip_address(cnf[field])
    #
    #             except ValueError:
    #                 error_func(error % (cnf[field], field))

    for field in ['source_port', 'destination_port']:
        if cnf[field] not in [None, '']:
            try:
                if not validators.between(int(cnf[field]), 1, 65535):
                    error_func(error % (cnf[field], field))

            except ValueError:
                error_func(error % (cnf[field], field))

    if cnf['protocol'] in ['TCP/UDP']:
        error_func(error % (cnf['protocol'], 'protocol'))

    # some recommendations - maybe the user overlooked something
    if cnf['action'] == 'pass' and cnf['protocol'] in ['TCP', 'UDP']:
        if cnf['source_net'] == 'any' and cnf['destination_net'] == 'any':
            module.warn(
                "Configuring allow-rules with 'any' source and "
                "'any' destination is bad practise!"
            )

        elif cnf['destination_net'] == 'any' and cnf['destination_port'] == 'any':
            module.warn(
                "Configuring allow-rules to 'any' destination "
                "using 'all' ports is bad practise!"
            )


def get_state_change(before: dict, after: dict) -> bool:
    return before['enabled'] != after['enabled']


def get_config_change(before: dict, after: dict) -> bool:
    matching = []

    for b_k, b_v in before.items():
        if b_k == 'enabled':
            continue

        matching.append(str(b_v) == str(after[b_k]))

    return not all(matching)


def check_purge_configured(module: AnsibleModule, existing_rule: dict) -> bool:
    to_purge = True

    for rule_key, rule_config in module.params['rules'].items():
        if rule_config is None:
            rule_config = {}

        rule_config['match_fields'] = module.params['match_fields']
        rule_config[module.params['key_field']] = rule_key
        if check_for_matching_rule(existing=existing_rule, cnf=rule_config):
            to_purge = False
            break

    return to_purge
