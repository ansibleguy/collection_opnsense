import validators
from ipaddress import ip_address, ip_network

from ansible.module_utils.basic import AnsibleModule


def validate_values(module: AnsibleModule) -> None:
    v_type = module.params['type']

    for value in module.params['content']:
        error = f"Value '{value}' is invalid for type '{v_type}'!"
        if v_type == 'host':
            try:
                ip_address(value)

            except ValueError:
                if not validators.domain(value):
                    module.fail_json(error)

        elif v_type == 'network':
            try:
                ip_network(value)

            except ValueError:
                module.fail_json(error)

        elif v_type == 'port':
            try:
                if not validators.between(int(value), 1, 65535):
                    module.fail_json(error)

            except ValueError:
                module.fail_json(error)

        elif v_type == 'mac':
            if not validators.mac_address(value):
                module.fail_json(error)

        elif v_type in ['url', 'urltable']:
            if not validators.url(value):
                module.fail_json(error)


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
