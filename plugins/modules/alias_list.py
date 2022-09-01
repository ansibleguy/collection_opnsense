#!/usr/bin/python3

# Copyright: (C) 2022, AnsibleGuy <guy@ansibleguy.net>
# GNU General Public License v3.0+ (see https://www.gnu.org/licenses/gpl-3.0.txt)

# see: https://docs.opnsense.org/development/api/core/firewall.html

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.defaults import OPN_MOD_ARGS
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.alias_obj import Alias
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.alias_helper import builtin_alias

DOCUMENTATION = 'https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_alias.md'
EXAMPLES = 'https://github.com/ansibleguy/collection_opnsense/blob/stable/tests/alias.yml'


def run_module():
    module_args = dict(
        filter=dict(
            type='str', required=False,
            choices=['enabled', 'disabled']
        ),
        filter_builtin=dict(type='bool', required=False, default=True),
        **OPN_MOD_ARGS
    )

    result = dict(
        changed=False,
        aliases={},
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True,  # practically not - but it will not change anything
    )

    alias = Alias(module=module, result={})

    # building dict out of list of dicts
    for _alias in alias.search_call():
        _values = _alias.copy()
        _values.pop('name')

        # filtering output if needed
        if module.params['filter_builtin'] and builtin_alias(_alias['name']):
            # ignore built-in aliases
            continue

        elif module.params['filter'] is not None:
            if _alias['enabled'] in [1, '1', True]:
                if module.params['filter'] == 'enabled':
                    result['aliases'][_alias['name']] = _values

            elif module.params['filter'] == 'disabled':
                result['aliases'][_alias['name']] = _values

        else:
            result['aliases'][_alias['name']] = _values

    alias.s.close()
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
