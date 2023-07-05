from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.main import \
    is_ip, is_port
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.validate import \
    is_valid_domain


def validate_domain(module: AnsibleModule, domain: str) -> None:
    test_domain = domain

    if domain.find('.') == -1:
        # TLD-only will fail the domain validation
        test_domain = f'dummy.{domain}'

    if not is_valid_domain(test_domain):
        module.fail_json(f"Value '{domain}' is an invalid domain!")


def validate_server(module: AnsibleModule, server: str) -> None:
    server_parts = server.split('@')
    server_parts_len = len(server_parts)

    if server_parts_len > 2:
        module.fail_json(f"Value '{server}' is not a valid IP-address and port number combination!")

    if not is_ip(server_parts[0]):
        module.fail_json(f"Value '{server_parts[0]}' is not a valid IP-address!")

    if server_parts_len == 2 and not is_port(server_parts[1]):
        module.fail_json(f"Value '{server_parts[1]}' is not a valid port!")
