from typing import Callable

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.handler import \
    exit_bug


def _sanitize_module_args(args: dict) -> dict:
    """Removes sensitive credentials (API key/secret) from a dictionary before logging/debugging."""
    args.pop('api_key', None)
    args.pop('api_secret', None)
    return args


def get_matching(
        module: AnsibleModule, existing_items: (dict, list), compare_item: dict,
        match_fields: list, simplify_func: Callable = None,
) -> (dict, None):
    """
        Finds a single existing item that matches the provided item based on specified fields.

        :param module: Ansible module object used for logging debug warnings.
        :param existing_items: Data source (dict or list) to search within.
        :param compare_item: The item dictionary to match against.
        :param match_fields: List of keys to verify equality on.
        :param simplify_func: Optional function to sanitize existing items before comparing.
        :return: The matching item dictionary, or None if no match is found.
    """
    matching = None
    if len(existing_items) == 0:
        return matching

    existing_items_list = []
    if isinstance(existing_items, list):
        existing_items_list = existing_items

    elif isinstance(existing_items, dict):
        for uuid, existing in existing_items.items():
            existing['uuid'] = uuid
            existing_items_list.append(existing)

    for existing in existing_items_list:
        _matching = []

        if simplify_func is not None:
            existing = simplify_func(existing)

        try:
            if not isinstance(match_fields, list):
                exit_bug(f"Failed because 'match_fields' are not a list: {type(match_fields)} '{match_fields}'")

            for field in match_fields:
                _matching.append(str(existing[field]) == str(compare_item[field]))

                if module.params['debug']:
                    if existing[field] != compare_item[field]:
                        module.warn(
                            f"NOT MATCHING: "
                            f"'{existing[field]}' != '{compare_item[field]}'"
                        )

        except KeyError as error:
            exit_bug(
                "Failed to match existing entry with provided one: "
                f"{existing} <=> {_sanitize_module_args(compare_item)}; "
                f"Error while comparing: {error}"
            )

        if all(_matching):
            matching = existing
            break

    return matching


def get_multiple_matching(
        module: AnsibleModule, existing_items: (dict, list), compare_item: dict,
        match_fields: list, simplify_func: Callable = None,
) -> list:
    """
        Similar to get_matching, but returns a list of all items that match.

        :return: A list of matching item dictionaries.
    """
    matching = []
    if len(existing_items) == 0:
        return matching

    existing_items_list = []
    if isinstance(existing_items, list):
        existing_items_list = existing_items

    elif isinstance(existing_items, dict):
        for uuid, existing in existing_items.items():
            existing['uuid'] = uuid
            existing_items_list.append(existing)

    for existing in existing_items_list:
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
