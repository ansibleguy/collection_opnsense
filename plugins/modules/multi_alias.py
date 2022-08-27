#!/usr/bin/python3

# Copyright: (C) 2022, AnsibleGuy <guy@ansibleguy.net>
# GNU General Public License v3.0+ (see https://www.gnu.org/licenses/gpl-3.0.txt)

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.common.arg_spec import ModuleArgumentSpecValidator

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper import diff_remove_empty
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.api import Session
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.defaults import OPN_MOD_ARGS
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.alias_defaults import ALIAS_DEFAULTS, ALIAS_MOD_ARGS
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.alias_obj import Alias
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.alias_main import process_alias


DOCUMENTATION = 'https://github.com/ansibleguy/collection_opnsense/blob/stable/use_multi_alias.md'
EXAMPLES = 'https://github.com/ansibleguy/collection_opnsense/blob/stable/use_multi_alias.md'


def run_module():
    module_args = dict(
        aliases=dict(type='dict', required=True),
        fail_verification=dict(
            type='bool', required=False, default=False,
            description='Fail module if single alias fails the verification.'
        ),
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

    validator = ModuleArgumentSpecValidator(ALIAS_MOD_ARGS,
                                            module.mutually_exclusive,
                                            module.required_together,
                                            module.required_one_of,
                                            module.required_if,
                                            module.required_by)

    session = Session(module=module)
    existing_aliases = Alias(module=module, session=session, result={}).pull_call()

    for _name, _config in module.params['aliases'].items():
        # build config and validate it the same way the module initialization would do
        alias_cnf = {
            **ALIAS_DEFAULTS,
            **{
                'name': _name,
                'firewall': module.params['firewall']
            },
            **_config
        }
        validation_result = validator.validate(parameters=alias_cnf)

        try:
            validation_error = validation_result.errors[0]

        except IndexError:
            validation_error = None

        if validation_error:
            error_msg = validation_result.errors.msg
            if module.params['fail_verification']:
                module.fail_json(f"Got invalid config for alias '{_name}': {error_msg}")

            else:
                module.warn(f"Got invalid config for alias '{_name}': {error_msg}")

        else:
            # process single alias like in the 'alias' module
            alias_result = dict(
                changed=False,
                diff={
                    'before': {},
                    'after': {},
                }
            )
            alias = Alias(
                module=module,
                result=alias_result,
                cnf=alias_cnf,
                session=session,
                fail=module.params['fail_verification'],
            )

            alias.check(existing_aliases=existing_aliases)
            process_alias(alias=alias)

            if alias_result['changed']:
                result['changed'] = True
                result['diff']['before'].update(alias_result['diff']['before'])
                result['diff']['after'].update(alias_result['diff']['after'])

    session.close()
    result['diff'] = diff_remove_empty(result['diff'])
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
