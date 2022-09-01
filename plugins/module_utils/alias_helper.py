from ipaddress import ip_network
from re import match as regex_match
import validators

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.defaults import \
    BUILTIN_ALIASES, BUILTIN_INTERFACE_ALIASES_REG


def validate_values(error_func, cnf: dict) -> None:
    v_type = cnf['type']

    for value in cnf['content']:
        error = f"Value '{value}' is invalid for type '{v_type}'!"

        if v_type == 'network':
            value = value[1:] if value.startswith('!') else value

            try:
                ip_network(value)

            except ValueError:
                error_func(value)

        elif v_type == 'port':
            if str(value).find(':') != -1:
                to_check = value.split(':')

            else:
                to_check = [value]

            for _value in to_check:
                try:
                    if not validators.between(int(_value), 1, 65535):
                        error_func(error)

                except ValueError:
                    error_func(error)

        elif v_type == 'mac':
            # todo: support for partial mac addresses?
            if not validators.mac_address(value):
                error_func(error)

        elif v_type in ['url', 'urltable']:
            if not validators.url(value):
                error_func(error)

        # unable to check because of alias-nesting support and ip-ranges
        # if v_type == 'host':
        #     try:
        #         ip_address(value)
        #
        #     except ValueError:
        #         if not validators.domain(value):
        #             error_func(error)


def get_alias(name: str, aliases: list) -> dict:
    alias = {}

    for existing in aliases:
        if existing['name'] == name:
            alias = existing
            break

    return alias


def convert_existing_type(existing: str) -> str:
    return existing.lower().replace(' ', '').split('(', 1)[0]


def equal_type(existing: str, configured: str) -> bool:
    return configured == convert_existing_type(existing)


def simplify_existing_alias(existing: dict) -> dict:
    existing['type'] = convert_existing_type(existing['type'])
    return existing


def alias_in_use_by_rule(rules: dict, alias: str) -> bool:
    in_use = False

    if len(rules) > 0:
        for rule in rules.values():
            if alias in (rule['source_net'], rule['destination_net']):
                in_use = True
                break

    return in_use


def check_purge_filter(module: AnsibleModule, existing_rule: dict) -> bool:
    to_purge = True

    for filter_key, filter_value in module.params['filters'].items():
        if module.params['filter_invert']:
            # purge all except matches
            if module.params['filter_partial']:
                if str(existing_rule[filter_key]).find(filter_value) != -1:
                    to_purge = False
                    break

            else:
                if existing_rule[filter_key] == filter_value:
                    to_purge = False
                    break

        else:
            # purge only matches
            if module.params['filter_partial']:
                if str(existing_rule[filter_key]).find(filter_value) == -1:
                    to_purge = False
                    break

            else:
                if existing_rule[filter_key] != filter_value:
                    to_purge = False
                    break

    return to_purge


def compare_aliases(existing: dict, configured: dict) -> tuple:
    before = list(map(str, existing['content'].split(',')))
    after = list(map(str, configured['content']))
    before.sort()
    after.sort()
    return before != after, before, after


def check_purge_configured(module: AnsibleModule, existing_alias: dict) -> bool:
    to_purge = True
    existing_name = existing_alias['name']

    for alias_name in module.params['aliases'].keys():
        if existing_name == alias_name:
            to_purge = False
            break

    return to_purge


def builtin_alias(name: str) -> bool:
    # ignore built-in aliases
    return name in BUILTIN_ALIASES or \
           regex_match(BUILTIN_INTERFACE_ALIASES_REG, name) is not None
