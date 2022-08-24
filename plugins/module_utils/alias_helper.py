from collections import Counter
import validators
from ipaddress import ip_address, ip_network

from ansible.module_utils.basic import AnsibleModule


def get_only_values(rows: list) -> list:
    values = []

    for row in rows:
        if type(row) == dict:
            values.extend(row.values())

        else:
            values.append(row)

    return values


def alias_changed(existing: list, configured: list) -> bool:
    return Counter(get_only_values(existing)) != Counter(configured)


def validate_values(module: AnsibleModule) -> None:
    v_type = module.params['type']

    for value in module.params['values']:
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
