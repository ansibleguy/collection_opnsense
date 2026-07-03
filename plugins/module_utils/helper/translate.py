from typing import Callable

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
        entry_processed = entry.copy()
        if simplify_func is not None:
            entry_processed = simplify_func(entry_processed)

        if add_filter is not None:
            entry_processed = add_filter(entry_processed)

        simple_entries.append(entry_processed)

    return simple_entries


class SimplifyTranslate:
    """
        Maps and converts OPNsense API response data into the canonical format used by Ansible.
        Handles field translation, type casting (bool/int/list), and value mapping.
    """

    FLAG_PROCESSED = '__ansible_translated'

    def __init__(
            self,
            translate: dict[str, str] = None,
            typing: dict[str, str] = None,
            value_map: dict = None,
            bool_invert: list[str] = None,
            ignore: list[str] = None,
            optional: list[str] = None,
    ):
        self._fields_translate: dict[str, str] = translate if translate is not None else {}
        self._fields_typing: dict[str, str] = typing if typing is not None else {}
        self._value_map: dict = value_map if value_map is not None else {}
        self._fields_bool_invert: list[str] = bool_invert if bool_invert is not None else []
        self._fields_ignore: list[str] = ignore if ignore is not None else []
        self._fields_optional: list[str] = optional if optional is not None else []

    def translate(self, existing: dict) -> dict:
        translated = {}
        try:
            if self.FLAG_PROCESSED in existing:
                # already translated
                return existing

            translated = self._translate_field_names_api_to_ansible(existing)
            self._ensure_field_value_typing(translated)
            self._apply_field_value_mapping(translated)
            translated[self.FLAG_PROCESSED] = ''
            return translated

        except KeyError as err:
            # DEBUG:
            # raise err
            exit_bug(
                f"Failed to translate API entry to Ansible entry! Maybe the API changed lately? "
                f"Failed field: {err} | "
                f"API entry: '{existing}' '{translated}'"
            )
            return {}

    def _translate_field_names_api_to_ansible(self, existing: dict) -> dict:
        # Ensure the fields returned by the OPNsense API are translated to the ones used by the ansible-modules
        # This allows us to have clean module-argument
        translated = {}

        for field_ansible, field_api in self._fields_translate.items():
            if isinstance(field_api, tuple):
                # handle nested fields
                current_level = existing.copy()
                skip_optional = False

                for key in field_api:
                    if field_ansible in self._fields_optional and key not in current_level:
                        # OPNsense API may conditionally omit some fields from API-responses :(
                        skip_optional = True
                        break

                    current_level = current_level[key]

                if skip_optional:
                    continue

                translated[field_ansible] = current_level

            elif isinstance(field_api, list):
                # for edge-cases where the get and set API has different field-names for the same "value" :'(
                found = False
                for field_api_option in field_api:
                    if field_api_option in existing:
                        translated[field_ansible] = existing[field_api_option]
                        found = True
                        break

                if not found:
                    raise KeyError(field_api)

            else:
                if field_ansible in self._fields_optional and field_api not in existing:
                    # OPNsense API may conditionally omit some fields from API-responses :(
                    continue

                translated[field_ansible] = existing[field_api]

        # passthrough for fields that do not have to be translated and should not be "ignored"
        translate_fields = self._fields_translate.values()
        for field in existing:
            if field not in translate_fields and field not in self._fields_ignore:
                translated[field] = existing[field]

        return translated

    def _ensure_field_value_typing(self, existing: dict):
        for type_key, fields in self._fields_typing.items():
            for f in fields:
                if f in self._fields_ignore:
                    continue

                if f in self._fields_optional and f not in existing:
                    # OPNsense API may conditionally omit some fields from API-responses :(
                    continue

                if type_key == 'bool':
                    existing[f] = is_true(existing[f])

                elif type_key == 'int':
                    existing[f] = format_int(existing[f])

                elif type_key == 'list':
                    existing[f] = get_selected_list(data=existing[f], remove_empty=True, get_value=False)

                elif type_key == 'list_value':
                    existing[f] = get_selected_list(data=existing[f], remove_empty=True, get_value=True)

                elif type_key == 'select':
                    existing[f] = get_selected(existing[f])

                elif type_key == 'select_opt_list':
                    existing[f] = get_selected_opt_list(existing[f])

                elif type_key == 'select_opt_list_idx':
                    existing[f] = get_selected_opt_list_idx(existing[f])

        for f, value in existing.items():
            if isinstance(value, str) and value.isnumeric():
                existing[f] = int(existing[f])

            elif isinstance(value, bool) and f in self._fields_bool_invert:
                existing[f] = not existing[f]

    def _apply_field_value_mapping(self, existing: dict):
        for f, vmap in self._value_map.items():
            try:
                for pretty_value, opn_value in vmap.items():
                    if existing[f] == opn_value:
                        existing[f] = pretty_value
                        break

            except KeyError:
                pass


def simplify_translate(
        existing: dict, translate: dict = None, typing: dict = None,
        bool_invert: list = None, ignore: list = None, value_map: dict = None, optional: list = None,
) -> dict:
    # Wrapper-function for SimplifyTranslate
    s = SimplifyTranslate(
        translate=translate,
        typing=typing,
        value_map=value_map,
        bool_invert=bool_invert,
        ignore=ignore,
        optional=optional,
    )
    return s.translate(existing)
