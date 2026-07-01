from typing import Callable
from functools import reduce

from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.handler import \
    exit_bug
from ansible_collections.oxlorg.opnsense.plugins.module_utils.helper.main import \
    is_true, format_int


def get_selected(data: dict) -> (str, None):
    """
        Extracts the key of the selected item from a standard OPNsense selection dictionary.

        :param data: A dictionary where values contain a 'selected' key (e.g., {'key': {'selected': '1'}}).
        :return: The key string where 'selected' is True, or an empty string if none are selected.
    """
    if isinstance(data, dict):
        for key, values in data.items():
            if is_true(values['selected']):
                return key

        return ''  # none selected

    # if function is re-applied
    return data


def get_selected_value(data: (dict, list)) -> (str, None):
    """
        Extracts the 'value' field from the selected item in a dictionary or list.

        :param data: The selection structure to parse.
        :return: The 'value' attribute of the selected item, or an empty string if none found.
    """
    if isinstance(data, dict):
        for values in data.values():
            if is_true(values['selected']) and 'value' in values:
                return values['value']

        return ''  # none selected

    if isinstance(data, list):
        for values in data:
            if is_true(values['selected']) and 'value' in values:
                return values['value']

        return ''  # none selected

    # if function is re-applied
    return data


def get_selected_opt_list(data: (dict, list)) -> (str, None):
    """
        Wrapper function to determine whether to use get_selected or get_selected_value based on input type.
    """
    if isinstance(data, dict):
        return get_selected(data)

    return get_selected_value(data)


def get_selected_opt_list_idx(data: list) -> int:
    """
        Finds the integer index of the first selected item in a list.

        :param data: A list of item dictionaries.
        :return: The index of the selected item, defaulting to 0.
    """
    idx = 0
    for values in data:
        if is_true(values['selected']):
            return idx

        idx += 1

    return 0


def get_selected_multi(data: (dict, list), get_value: bool = False) -> list:
    """
        Handles multi-select inputs, returning either keys or values of all selected items.

        :param data: Input dictionary or list of items.
        :param get_value: If True, returns the 'value' field; otherwise, returns the dictionary key.
        :return: A list of selected keys or values.
    """
    if isinstance(data, list) and len(data) > 0 and not isinstance(data[0], dict):
        # if function is re-applied
        return data

    selected_values = []
    if isinstance(data, dict):
        for key, values in data.items():
            if is_true(values['selected']):
                if not get_value:
                    selected_values.append(key)

                if get_value and 'value' in values:
                    selected_values.append(values['value'])

    if isinstance(data, list):
        for values in data:
            if is_true(values['selected']) and 'value' in values:
                selected_values.append(values['value'])

    return selected_values


def get_selected_list(data: dict, remove_empty: bool = False, get_value: bool = False) -> list:
    """
        Parses complex selection structures into a clean, sorted list.

        :param data: Input selection data.
        :param remove_empty: If True, strips None/empty strings from the final list.
        :param get_value: If True, uses the 'value' field instead of keys.
        :return: A sorted list of selected identifiers or values.
    """
    if isinstance(data, list):
        if len(data) == 0:
            return []

        if not isinstance(data[0], dict):
            # if function is re-applied
            return data

    if isinstance(data, str):
        if data.strip() == '':
            return []

        return data.split(',')

    selected = get_selected_multi(data=data, get_value=get_value)
    if remove_empty:
        for key in [None, '', ' ']:
            if key in selected:
                selected.remove(key)

    if 'System: Deny config write' in selected:
        raise exit_bug(f"TEST: {data}")

    selected.sort()
    return selected


def get_key_by_value_from_selection(selection: dict, value: str) -> (str, None):
    """Finds the dictionary key where the nested 'value' matches exactly."""
    if isinstance(selection, dict):
        for key, values in selection.items():
            if 'value' in values and values['value'] == value:
                return key

    return None


def get_key_by_value_end_from_selection(selection: dict, value: str) -> (str, None):
    """Finds the dictionary key where the nested 'value' ends with the provided string."""
    if isinstance(selection, dict):
        for key, values in selection.items():
            if 'value' in values and values['value'].endswith(value):
                return key

    return None


def get_key_by_value_beg_from_selection(selection: dict, value: str) -> (str, None):
    """Finds the dictionary key where the nested 'value' starts with the provided string."""
    if isinstance(selection, dict):
        for key, values in selection.items():
            if 'value' in values and values['value'].startswith(value):
                return key

    return None


def get_simple_existing(
        entries: (dict, list), add_filter: Callable = None,
        simplify_func: Callable = None
) -> list:
    """
        Transforms API-provided entries into a simplified list format for easier comparison.
    """
    simple_entries = []

    if isinstance(entries, dict):
        _entries = []
        for uuid, entry in entries.items():
            if not isinstance(entry, dict):
                exit_bug(f"The provided entry is not a dictionary => '{entry}'")

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


# pylint: disable=R0912,R0914,R0915
def simplify_translate(
        existing: dict, translate: dict = None, typing: dict = None,
        bool_invert: list = None, ignore: list = None, value_map: dict = None,
) -> dict:
    """
        Maps and converts OPNsense API response data into the canonical format used by Ansible.
        Handles field translation, type casting (bool/int/list), and value mapping.
    """
    simple = {}
    if translate is None:
        translate = {}

    if typing is None:
        typing = {}

    if bool_invert is None:
        bool_invert = []

    if ignore is None:
        ignore = []

    if value_map is None:
        value_map = {}

    try:
        # translate api-fields to ansible-fields
        for k, v in translate.items():
            if v in existing:
                simple[k] = existing[v]
            elif isinstance(v, tuple):
                simple[k] = reduce(lambda e, i: e[i], v, existing)

        translate_fields = translate.values()
        for k in existing:
            if k not in translate_fields and k not in ignore:
                simple[k] = existing[k]

        # correct value types to match (for diff-checks)
        for t, fields in typing.items():
            for f in fields:
                if f in ignore:
                    continue

                if t == 'bool':
                    simple[f] = is_true(simple[f])

                elif t == 'int':
                    simple[f] = format_int(simple[f])

                elif t == 'list':
                    simple[f] = get_selected_list(data=simple[f], remove_empty=True, get_value=False)

                elif t == 'list_value':
                    simple[f] = get_selected_list(data=simple[f], remove_empty=True, get_value=True)

                elif t == 'select':
                    simple[f] = get_selected(simple[f])

                elif t == 'select_opt_list':
                    simple[f] = get_selected_opt_list(simple[f])

                elif t == 'select_opt_list_idx':
                    simple[f] = get_selected_opt_list_idx(simple[f])

        for f, vmap in value_map.items():
            try:
                for pretty_value, opn_value in vmap.items():
                    if simple[f] == opn_value:
                        simple[f] = pretty_value
                        break

            except KeyError:
                pass

        for k, v in simple.items():
            if isinstance(v, str) and v.isnumeric():
                simple[k] = int(simple[k])

            elif isinstance(v, bool) and k in bool_invert:
                simple[k] = not simple[k]

    except KeyError as err:
        exit_bug(
            f"Failed to translate API entry to Ansible entry! Maybe the API changed lately? "
            f"Failed field: {err} | "
            f"API entry: '{existing}' '{simple}'"
        )

    return simple
