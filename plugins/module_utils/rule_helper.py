import validators

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper import ensure_list


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
        simple['uuid'] = uuid
        simple['enabled'] = values['enabled'] in [1, '1', True]
        simple['log'] = values['log'] in [1, '1', True]
        simple['quick'] = values['quick'] in [1, '1', True]
        simple['source_invert'] = values['source_not'] in [1, '1', True]
        simple['destination_invert'] = values['destination_not'] in [1, '1', True]

        if values['action']['block']['selected'] in [1, '1', True]:
            simple['action'] = 'block'

        elif values['action']['reject']['selected'] in [1, '1', True]:
            simple['action'] = 'reject'

        else:
            simple['action'] = 'pass'

        for field in copy_fields:
            simple[field] = values[field]

        simple['interface'] = []

        for interface, interface_values in values['interface'].items():
            if interface_values['selected'] in [1, '1', True]:
                simple['interface'].append(interface)

        for direction, direction_values in values['direction'].items():
            if direction_values['selected'] in [1, '1', True]:
                simple['direction'] = direction
                break

        for proto_name, proto_values in values['ipprotocol'].items():
            if proto_values['selected'] in [1, '1', True]:
                simple['ip_protocol'] = proto_name
                break

        for proto_name, proto_values in values['protocol'].items():
            if proto_values['selected'] in [1, '1', True]:
                simple['protocol'] = proto_name
                break

        for gw, gw_values in values['gateway'].items():
            if gw_values['selected'] in [1, '1', True]:
                simple['gateway'] = gw
                break

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
    if cnf['action'] == 'pass':
        if cnf['source_net'] == 'any' and cnf['destination_net'] == 'any' and cnf['protocol'] in ['TCP', 'UDP']:
            module.warn(
                "Configuring allow-rules with 'any' source and "
                "'any' destination is bad practise!"
            )

        elif cnf['destination_net'] == 'any' and cnf['destination_port'] == 'any' and cnf['protocol'] in ['TCP', 'UDP']:
            module.warn(
                "Configuring allow-rules to 'any' destination "
                "using 'all' ports is bad practise!"
            )


def diff_filter(cnf: dict) -> dict:
    diff = {}
    relevant_fields = [
        'action', 'quick', 'direction', 'ip_protocol', 'protocol',
        'source_invert', 'source_net', 'destination_invert', 'destination_net',
        'gateway', 'log', 'description'
    ]

    # special case..
    diff['sequence'] = str(cnf['sequence'])
    diff['destination_port'] = str(cnf['destination_port'])
    diff['source_port'] = str(cnf['source_port'])
    diff['interface'] = ','.join(map(str, ensure_list(cnf['interface'])))

    for field in relevant_fields:
        diff[field] = cnf[field]

    return diff


def get_any_change(before: dict, after: dict) -> bool:
    matching = []

    for b_k, b_v in before.items():
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
