from ipaddress import ip_address, ip_network
import validators


def validate_values(error_func, cnf: dict) -> None:
    v_type = cnf['type']

    for value in cnf['content']:
        error = f"Value '{value}' is invalid for type '{v_type}'!"
        if v_type == 'host':
            try:
                ip_address(value)

            except ValueError:
                if not validators.domain(value):
                    error_func(error)

        elif v_type == 'network':
            try:
                ip_network(value)

            except ValueError:
                error_func(error)

        elif v_type == 'port':
            try:
                if not validators.between(int(value), 1, 65535):
                    error_func(error)

            except ValueError:
                error_func(error)

        elif v_type == 'mac':
            if not validators.mac_address(value):
                error_func(error)

        elif v_type in ['url', 'urltable']:
            if not validators.url(value):
                error_func(error)


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
