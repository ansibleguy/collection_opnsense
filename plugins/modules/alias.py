#!/usr/bin/python3

# Copyright: (C) 2022, AnsibleGuy <guy@ansibleguy.net>
# GNU General Public License v3.0+ (see https://www.gnu.org/licenses/gpl-3.0.txt)

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.alias_obj import Alias
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.alias_defaults import ALIAS_DEFAULTS, ALIAS_MOD_ARGS

DOCUMENTATION = 'https://github.com/ansibleguy/collection_opnsense/blob/stable/use_alias.md'
EXAMPLES = 'https://github.com/ansibleguy/collection_opnsense/blob/stable/use_alias.md'


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

    # if module.params['updatefreq_days'] is None:
    #     module.params['updatefreq_days'] = ''

    alias = Alias(module=module, result=result)
    alias.check()

    if alias.cnf['state'] == 'absent':
        if alias.exists:
            alias.delete()

    else:
        if alias.cnf['content'] is not None and len(alias.cnf['content']) > 0:
            if alias.exists:
                alias.update()

            else:
                alias.create()

        # dis-/enabling
        if alias.exists:
            if alias.cnf['enabled']:
                alias.enable()

            else:
                alias.disable()

    alias.s.close()
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
