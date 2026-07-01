from re import match as regex_match
from typing import Callable

from ansible_collections.oxlorg.opnsense.plugins.module_utils.defaults.main import \
    BUILTIN_ALIASES, BUILTIN_INTERFACE_ALIASES_REG
from ansible_collections.oxlorg.opnsense.plugins.module_utils.helper.validate import \
    is_valid_partial_mac_address, is_valid_url, validate_port_or_range, is_valid_network, is_valid_host, is_ip
from ansible_collections.oxlorg.opnsense.plugins.module_utils.helper.main import is_unset


# This should be kept aligned with getValidators from the AliasContentField
# https://github.com/opnsense/core/blob/master/src/opnsense/mvc/app/models/OPNsense/Firewall/FieldTypes/AliasContentField.php
def validate_values(cnf: dict, error_func: Callable, existing_entries: dict) -> None:
    """Validates alias values against existing entries and type requirements."""
    v_type = cnf['type']

    if isinstance(existing_entries, dict):
        existing_entries = [
            a['name']
            for a in existing_entries.values()
        ]

    else:
        existing_entries = [
            a['name']
            for a in existing_entries
        ]

    for value in cnf['content']:
        if value in existing_entries:
            continue

        error = f"Value '{value}' is invalid for type '{v_type}'!"

        if v_type == 'port':
            validate_port_or_range(module=None, port=value, error_func=error_func, range_sep=':')

        elif v_type == 'host' and not is_valid_host(value):
            error_func(error)

        #elif v_type == 'geoip':
        #    pass

        elif v_type == 'network' and not is_valid_network(value):
            error_func(error)

        elif v_type == 'networkgroup':
            error_func(f"Value '{value}' is not a valid alias!")

        elif v_type == 'mac' and not is_valid_partial_mac_address(value):
            error_func(error)

        elif v_type == 'dynipv6host' and not is_ip(f"0000{value}"):
            error_func(error)

        elif v_type == 'asn':
            try:
                if int(value) < 1 or int(value) > 4294967296:
                    error_func(error)

            except ValueError:
                error_func(error)

        #elif v_type == 'authgroup':
        #    pass

        # OPNsense has no validation for urls in the API
        elif v_type in ['url', 'urltable', 'urljson'] and not is_valid_url(value):
            error_func(error)


def compare_aliases(existing: dict, configured: dict) -> tuple:
    before = list(map(str, existing['content']))
    after = list(map(str, configured['content']))
    before.sort()
    after.sort()
    return before != after, before, after


def builtin_alias(name: str) -> bool:
    # ignore built-in aliases
    return name in BUILTIN_ALIASES or \
           regex_match(BUILTIN_INTERFACE_ALIASES_REG, name) is not None


def filter_builtin_alias(aliases: list) -> list:
    filtered = []

    for alias in aliases:
        # ignore built-in aliases
        if not builtin_alias(alias['name']):
            filtered.append(alias)

    return filtered


DEFAULT_UPDATEFREQ_DAYS_URLTABLE = 7  # see: https://github.com/O-X-L/ansible-opnsense/pull/270


def build_updatefreq(updatefreq: (int, float, str), default: bool = False) -> (int, float):
    if is_unset(updatefreq):
        if default:
            return DEFAULT_UPDATEFREQ_DAYS_URLTABLE

        return updatefreq

    updatefreq = float(updatefreq)
    dec = 1
    if str(updatefreq).endswith('.0'):
        dec = None

    return round(updatefreq, dec)
