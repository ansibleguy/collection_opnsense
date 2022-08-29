from ipaddress import ip_network
import validators


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


def equal_type(existing: str, configured: str) -> bool:
    e = existing.lower().replace(' ', '').split('(', 1)[0]
    return configured == e


def alias_in_use_by_rule(rules: dict, alias: str) -> bool:
    in_use = False

    if len(rules) > 0:
        for rule in rules.values():
            if rule['source_net'] == alias or rule['destination_net'] == alias:
                in_use = True
                break

    return in_use
