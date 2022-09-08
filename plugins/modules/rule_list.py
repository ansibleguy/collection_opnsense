#!/usr/bin/python3

# Copyright: (C) 2022, AnsibleGuy <guy@ansibleguy.net>
# GNU General Public License v3.0+ (see https://www.gnu.org/licenses/gpl-3.0.txt)

# see: https://docs.opnsense.org/development/api/plugins/firewall.html

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.handler import \
    module_dependency_error, MODULE_EXCEPTIONS

try:
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.defaults import OPN_MOD_ARGS
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.rule_obj import Rule
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper import is_true

except MODULE_EXCEPTIONS:
    module_dependency_error()

DOCUMENTATION = 'https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_rule.md'
EXAMPLES = 'https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_rule.md'


def run_module():
    module_args = dict(
        filter=dict(
            type='str', required=False,
            choices=['enabled', 'disabled']
        ),
        **OPN_MOD_ARGS
    )

    result = dict(
        changed=False,
        rules={},
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True,  # practically not - but it will not change anything
    )

    rule = Rule(module=module, result={})
    result['rules'] = rule.search_call()

    # filtering output if needed
    if module.params['filter'] is not None:
        filtered_rules = {}

        if len(result['rules']) > 0:
            for _uuid, _rule in result['rules'].items():
                if is_true(_rule['enabled']):
                    if module.params['filter'] == 'enabled':
                        filtered_rules[_uuid] = _rule

                elif module.params['filter'] == 'disabled':
                    filtered_rules[_uuid] = _rule

        result['rules'] = filtered_rules

    rule.s.close()
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
