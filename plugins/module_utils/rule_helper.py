import validators

from ansible.module_utils.basic import AnsibleModule


def get_rule(rules: (list, dict), cnf: dict) -> dict:
    rule = {}

    if len(rules) > 0:
        for uuid, values in rules.items():
            existing = _simplify_existing_rule(rule={uuid: values})
            if _check_for_match(existing=existing, cnf=cnf):
                rule = existing
                break

    return rule


def _check_for_match(existing: dict, cnf: dict) -> bool:
    _matching = []

    for field in cnf['match_fields']:
        _matching.append(str(existing[field]) == str(cnf[field]))

    return all(_matching)


def _simplify_existing_rule(rule: dict) -> dict:
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
    if cnf['source_net'] == 'any' and cnf['destination_net'] == 'any':
        module.warn(f"Configuring rules with 'any' source and 'any' destination is bad practise!")

    elif cnf['destination_net'] == 'any' and cnf['destination_port'] == 'any' and cnf['protocol'] in ['TCP', 'UDP']:
        module.warn(f"Configuring rules to 'any' destination using 'all' ports is bad practise!")


def diff_filter(cnf: dict) -> dict:
    diff = {}
    relevant_fields = [
        'action', 'quick', 'interface', 'direction', 'ip_protocol', 'protocol',
        'source_invert', 'source_net', 'source_port',
        'destination_invert', 'destination_net', 'destination_port',
        'gateway', 'log', 'description'
    ]

    # special case..
    diff['sequence'] = str(cnf['sequence'])

    for field in relevant_fields:
        diff[field] = cnf[field]

    return diff


def get_any_change(before: dict, after: dict) -> bool:
    matching = []

    for b_k, b_v in before.items():
        matching.append(str(b_v) == str(after[b_k]))

    return not all(matching)
