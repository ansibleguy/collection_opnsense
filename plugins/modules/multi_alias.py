#!/usr/bin/python3

# Copyright: (C) 2022, AnsibleGuy <guy@ansibleguy.net>
# GNU General Public License v3.0+ (see https://www.gnu.org/licenses/gpl-3.0.txt)

# see: https://docs.opnsense.org/development/api/core/firewall.html

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.defaults import OPN_MOD_ARGS
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.alias_defaults import ALIAS_DEFAULTS, ALIAS_MOD_ARGS
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper import diff_remove_empty, ensure_list
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.api import Session
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.alias_obj import Alias
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.alias_main import process_alias
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.rule_obj import Rule
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.multi_helper import validate_single

DOCUMENTATION = 'https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_multi_alias.md'
EXAMPLES = 'https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/tests/multi_alias.yml'


def run_module():
    module_args = dict(
        aliases=dict(type='dict', required=True),
        fail_verification=dict(
            type='bool', required=False, default=False,
            description='Fail module if single alias fails the verification.'
        ),
        state=dict(type='str', default='unset', required=False, choices=['present', 'absent', 'unset']),
        enabled=dict(type='bool', required=False, default=None),
        **OPN_MOD_ARGS
    )

    result = dict(
        changed=False,
        diff={
            'before': {},
            'after': {},
        }
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True,
    )

    session = Session(module=module)
    existing_aliases = Alias(module=module, session=session, result={}).search_call()
    existing_rules = Rule(module=module, session=session, result={}).search_call()

    overrides = {}

    if module.params['state'] != 'unset':
        overrides['state'] = module.params['state']

    if module.params['enabled'] is not None:
        overrides['enabled'] = module.params['enabled']

    # build list of valid rules or fail if invalid config is not permitted
    valid_aliases = []
    for alias_name, alias_config in module.params['aliases'].items():
        # build config and validate it the same way the module initialization would do
        if alias_config is None:
            alias_config = {}

        real_cnf = {
            **ALIAS_DEFAULTS,
            **alias_config,
            **{
                'name': alias_name,
                'firewall': module.params['firewall'],
            },
            **overrides,
        }
        real_cnf['content'] = list(map(str, ensure_list(real_cnf['content'])))

        if validate_single(
                module=module, module_args=ALIAS_MOD_ARGS, log_mod='rule',
                key=alias_name, cnf=real_cnf,
        ):
            valid_aliases.append(real_cnf)

    for alias_config in valid_aliases:
        # process single alias like in the 'alias' module
        alias_result = dict(
            changed=False,
            diff={
                'before': {},
                'after': {},
            }
        )
        module.params['debug'] = alias_config['debug']  # per rule switch
        alias = Alias(
            module=module,
            result=alias_result,
            cnf=alias_config,
            session=session,
            fail=module.params['fail_verification'],
        )
        # save on requests
        alias.existing_aliases = existing_aliases
        alias.existing_rules = existing_rules

        alias.check()
        process_alias(alias=alias)

        if alias_result['changed']:
            result['changed'] = True
            alias_result['diff'] = diff_remove_empty(alias_result['diff'])

            if 'before' in alias_result['diff']:
                result['diff']['before'].update(alias_result['diff']['before'])

            if 'after' in alias_result['diff']:
                result['diff']['after'].update(alias_result['diff']['after'])

    # todo: add purging option => or create additional module for it

    session.close()
    result['diff'] = diff_remove_empty(result['diff'])
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
