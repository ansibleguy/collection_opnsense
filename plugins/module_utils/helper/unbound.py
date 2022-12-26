from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.validate import domain


def validate_domain(module: AnsibleModule, domain: str):
    test_domain = domain

    if domain.find('.') == -1:
        # TLD-only will fail the domain validation
        test_domain = f'dummy.{domain}'

    if not domain(test_domain):
        module.fail_json(f"Value '{domain}' is an invalid domain!")
