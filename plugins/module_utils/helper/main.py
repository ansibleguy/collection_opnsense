from ipaddress import ip_address, ip_network
from re import match as regex_match

import validators

from ansible.module_utils.basic import AnsibleModule


def diff_remove_empty(diff: dict) -> dict:
    d = diff.copy()
    for k in diff.keys():
        if len(diff[k]) == 0:
            d.pop(k)

    return d


def ensure_list(data: (int, str, list, None)) -> list:
    # if user supplied a string instead of a list => convert it to match our expectations
    if isinstance(data, list):
        return data

    elif data is None:
        return []

    return [data]


def is_ip(host: str, ignore_empty: bool = False) -> bool:
    if ignore_empty and host in ['', ' ']:
        return True

    valid_ip = False

    try:
        ip_address(host)
        valid_ip = True

    except ValueError:
        pass

    return valid_ip


def is_ip_or_network(entry: str, strict: bool = False) -> bool:
    valid = is_ip(entry)

    if not valid:
        try:
            ip_network(entry, strict=strict)
            valid = True

        except ValueError:
            valid = False

    return valid


def valid_hostname(name: str) -> bool:
    _valid_domain = validators.domain(name)
    # see: https://en.wikipedia.org/wiki/Hostname#Restrictions_on_valid_host_names
    expr_hostname = r'^[a-zA-Z0-9-\.]{1,253}$'
    _valid_hostname = regex_match(expr_hostname, name) is not None
    return all([_valid_domain, _valid_hostname])


def get_matching(
        module: AnsibleModule, existing_items: (dict, list), compare_item: dict,
        match_fields: list, simplify_func=None,
) -> (dict, None):
    matching = None

    if len(existing_items) > 0:
        if isinstance(existing_items, dict):
            _existing_items_list = []
            for uuid, existing in existing_items.items():
                existing['uuid'] = uuid
                _existing_items_list.append(existing)

            existing_items = _existing_items_list

        for existing in existing_items:
            _matching = []

            if simplify_func is not None:
                existing = simplify_func(existing)

            for field in match_fields:
                _matching.append(str(existing[field]) == str(compare_item[field]))

                if module.params['debug']:
                    if existing[field] != compare_item[field]:
                        module.warn(
                            f"NOT MATCHING: "
                            f"'{existing[field]}' != '{compare_item[field]}'"
                        )

            if all(_matching):
                matching = existing
                break

    return matching


def get_multiple_matching(
        module: AnsibleModule, existing_items: (dict, list), compare_item: dict,
        match_fields: list, simplify_func=None,
) -> list:
    matching = []

    if len(existing_items) > 0:
        if isinstance(existing_items, dict):
            _existing_items_list = []
            for uuid, existing in existing_items.items():
                existing['uuid'] = uuid
                _existing_items_list.append(existing)

            existing_items = _existing_items_list

        for existing in existing_items:
            _simple = get_matching(
                module=module,
                existing_items=[existing],
                compare_item=compare_item,
                match_fields=match_fields,
                simplify_func=simplify_func,
            )
            if _simple is not None:
                matching.append(_simple)

    return matching


def validate_port(module: AnsibleModule, port: (int, str), error_func=None) -> bool:
    if error_func is None:
        error_func = module.fail_json

    if port in ['any', '']:
        return True

    try:
        if int(port) < 1 or int(port) > 65535:
            error_func(f"Value '{port}' is an invalid port!")
            return False

    except (ValueError, TypeError):
        error_func(f"Value '{port}' is an invalid port!")
        return False

    return True


def validate_int_fields(module: AnsibleModule, data: dict, field_minmax: dict, error_func=None):
    if error_func is None:
        error_func = module.fail_json

    for field, valid in field_minmax.items():
        try:
            if int(data[field]) < valid['min'] or int(data[field]) > valid['max']:
                error_func(
                    f"Value of field '{field}' is not valid - "
                    f"Must be between {valid['min']} and {valid['max']}!"
                )

        except (TypeError, ValueError):
            pass


def is_true(data: (str, int, bool)) -> bool:
    return data in [1, '1', True]


def get_selected(data: dict) -> str:
    for key, values in data.items():
        if is_true(values['selected']):
            return key


def get_selected_list(data: dict, remove_empty: bool = False) -> list:
    selected = []
    if len(data) > 0:
        for key, values in data.items():
            if remove_empty and key in [None, '', ' ']:
                continue

            if is_true(values['selected']):
                selected.append(key)

    selected.sort()
    return selected


def to_digit(data: bool) -> int:
    return 1 if data else 0


def get_simple_existing(entries: (dict, list), add_filter=None, simplify_func=None) -> list:
    simple_entries = []

    if isinstance(entries, dict):
        _entries = []
        for uuid, entry in entries.items():
            entry['uuid'] = uuid
            _entries.append(entry)

        entries = _entries

    for entry in entries:
        if simplify_func is not None and add_filter is not None:
            simple_entries.append(add_filter(simplify_func(entry)))

        elif simplify_func is not None:
            simple_entries.append(simplify_func(entry))

        else:
            simple_entries.append(entries)

    return simple_entries


def validate_str_fields(module: AnsibleModule, data: dict, field_regex: dict = None, field_minmax_length: dict = None):
    if field_minmax_length is not None:
        for field, min_max_length in field_minmax_length.items():
            if min_max_length['min'] < len(data[field]) > min_max_length['max']:
                module.fail_json(
                    f"Value of field '{field}' is not valid - "
                    f"Invalid length must be between {min_max_length['min']} and {min_max_length['max']}!"
                )

    if field_regex is not None:
        for field, regex in field_regex.items():
            if regex_match(regex, data[field]) is None:
                module.fail_json(
                    f"Value of field '{field}' is not valid - "
                    f"Must match regex '{regex}'!"
                )


def format_int(data: str) -> (int, str):
    if data.isnumeric():
        return int(data)

    return data


def sort_param_lists(params: dict):
    for k in params:
        if isinstance(params[k], list):
            params[k].sort()


def simplify_translate(
        existing: dict, translate: dict = None, typing: dict = None,
        bool_invert: list = None,
) -> dict:
    simple = {}
    translate_fields = []
    if translate is None:
        translate = {}

    if typing is None:
        typing = {}

    if bool_invert is None:
        bool_invert = []

    # translate api-fields to ansible-fields
    for k, v in translate.items():
        translate_fields.append(v)

        if v in existing:
            simple[k] = existing[v]

    for k in existing:
        if k not in translate_fields:
            simple[k] = existing[k]

    # correct value types to match (for diff-checks)
    for t, fields in typing.items():
        for f in fields:
            if t == 'bool':
                simple[f] = is_true(simple[f])

            elif t == 'int':
                simple[f] = int(simple[f])

            elif t == 'list':
                simple[f] = get_selected_list(simple[f])

            elif t == 'select':
                simple[f] = get_selected(simple[f])

    for k, v in simple.items():
        if isinstance(v, str) and v.isnumeric():
            simple[k] = int(simple[k])

        elif isinstance(v, bool) and k in bool_invert:
            simple[k] = not simple[k]

    return simple
