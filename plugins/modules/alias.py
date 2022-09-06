#!/usr/bin/python3

# Copyright: (C) 2022, AnsibleGuy <guy@ansibleguy.net>
# GNU General Public License v3.0+ (see https://www.gnu.org/licenses/gpl-3.0.txt)

# see: https://docs.opnsense.org/development/api/core/firewall.html

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper import diff_remove_empty
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.alias_obj import Alias
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.alias_defaults import ALIAS_MOD_ARGS

DOCUMENTATION = 'https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_alias.md'
EXAMPLES = 'https://github.com/ansibleguy/collection_opnsense/blob/stable/tests/alias.yml'


def run_module():
    result = dict(
        changed=False,
        diff={
            'before': {},
            'after': {},
        }
    )

    module = AnsibleModule(
        argument_spec=ALIAS_MOD_ARGS,
        supports_check_mode=True,
    )

    alias = Alias(module=module, result=result)
    alias.check()
    alias.process()
    if result['changed']:
        alias.reconfigure()

    alias.s.close()
    result['diff'] = diff_remove_empty(result['diff'])
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
