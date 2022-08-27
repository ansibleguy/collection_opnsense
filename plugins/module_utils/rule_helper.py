from ipaddress import ip_address, ip_network
import validators


def get_rule(rules: dict, cnf: dict) -> dict:
    rule = {}

    for existing_raw in rules.values():
        existing = _simplify_existing_rule(rule=existing_raw)
        _matching = []

        for field in cnf['match_fields']:
            _matching.append(existing[field] == cnf[field])

        if all(_matching):
            rule = existing

    return rule


def _simplify_existing_rule(rule: dict) -> dict:
    # because the return of api/firewall/filter/get is too verbose for easy access
    simple = {}

    copy_fields = [
        'sequence', 'source_net', 'source_not', 'source_port', 'destination_net',
        'destination_not', 'destination_port', 'log', 'description'
    ]

    for uuid, values in rule.items():
        simple['uuid'] = uuid
        simple['enabled'] = values['enabled'] in [1, '1', True]
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

        simple['interface'] = None

        for interface, interface_values in values['interface'].items():
            if interface_values['selected'] in [1, '1', True]:
                simple['interface'] = interface
                break

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


def validate_values(error_func, cnf: dict) -> None:
    error = "Value '%s' is invalid for the field '%s'!"

    for field in ['source_net', 'destination_net']:
        if cnf[field] not in [None, '', 'any']:
            try:
                ip_network(cnf[field])

            except ValueError:
                try:
                    ip_address(cnf[field])

                except ValueError:
                    error_func(error % (cnf[field], field))

    for field in ['source_port', 'destination_port']:
        if cnf[field] not in [None, '']:
            try:
                if not validators.between(int(cnf[field]), 1, 65535):
                    error_func(error % (cnf[field], field))

            except ValueError:
                error_func(error % (cnf[field], field))

    if cnf['protocol'] in ['TCP/UDP']:
        error_func(error % (cnf['protocol'], 'protocol'))


def diff_filter(cnf: dict) -> dict:
    diff = {}
    relevant_fields = [
        'sequence', 'action', 'interface', 'direction', 'ip_protocol', 'protocol',
        'source_invert', 'source_net', 'source_port',
        'destination_invert', 'destination_net', 'destination_port',
        'gateway', 'log', 'description'
    ]

    for field in relevant_fields:
        diff[field] = cnf[field]

    return diff
