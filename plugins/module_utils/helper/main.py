from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.handler import \
    exit_cnf


def diff_remove_empty(diff: dict, to_none: bool = False) -> dict:
    """
        Cleans a dictionary by removing empty lists or sub-dictionaries.

        :param diff: The original diff dictionary.
        :param to_none: If True, sets empty values to None instead of removing the key.
        :return: A cleaned version of the diff dictionary.
    """
    d = diff.copy()
    for k in diff:
        if len(diff[k]) == 0:
            if to_none:
                d[k] = None

            else:
                d.pop(k)

    return d


def ensure_list(data: (int, str, list, None)) -> list:
    """
        Normalizes input to ensure it is always returned as a list.

        :param data: Input data (scalar, list, or None).
        :return: A list containing the input or an empty list if input was None.
    """
    # if user supplied a string instead of a list => convert it to match our expectations
    if isinstance(data, list):
        return data

    if data is None:
        return []

    return [data]


def is_true(data: (str, int, bool)) -> bool:
    """Checks if input equates to a boolean 'True' (1, '1', or True)."""
    return data in [1, '1', True]


def to_digit(data: bool) -> int:
    """Converts a boolean to an integer (1 or 0)."""
    return 1 if data else 0


def format_int(data: (int, str)) -> (int, str, None):
    """Safely converts numeric strings to integers while preserving None or non-numeric strings."""
    if isinstance(data, int):
        return data

    if data is None:
        return None

    if data.isnumeric():
        return int(data)

    return data


def sort_param_lists(params: dict) -> None:
    """In-place sorts list values within a parameters dictionary."""
    for k in params:
        if isinstance(params[k], list):
            try:
                params[k].sort()

            except TypeError:
                pass


def is_unset(value: (str, None, list, dict)) -> bool:
    """Determines if a value is effectively 'empty' (None, empty string, or empty collection)."""
    if isinstance(value, (list, dict)):
        return len(value) == 0

    if isinstance(value, str):
        value = value.strip()

    return value in ['', None]


def unset_check_error(params: dict, field: str, fail: bool) -> bool:
    """Validates that a required field is set; optionally exits the module on failure."""
    if is_unset(params[field]):
        if fail:
            exit_cnf(f"Field '{field}' must be set!")

        return False

    return True
