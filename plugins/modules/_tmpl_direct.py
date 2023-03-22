#!/usr/bin/env python3

# Copyright: (C) 2022, AnsibleGuy <guy@ansibleguy.net>
# GNU General Public License v3.0+ (see https://www.gnu.org/licenses/gpl-3.0.txt)

# template to be copied to implement new modules

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.handler import \
    module_dependency_error, MODULE_EXCEPTIONS

try:
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.main import \
        diff_remove_empty
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.api import Session
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.defaults.main import \
        OPN_MOD_ARGS, STATE_MOD_ARG

except MODULE_EXCEPTIONS:
    module_dependency_error()

DOCUMENTATION = 'https://opnsense.ansibleguy.net/en/latest/modules/_tmpl.html'
EXAMPLES = 'https://opnsense.ansibleguy.net/en/latest/modules/_tmpl.html'


def run_module():
    module_args = dict(
        name=dict(type='str', required=True),
        description=dict(type='str', required=False, default='', aliases=['desc']),
        content=dict(type='list', required=False, default=[], elements='str'),
        type=dict(type='str', required=False, choices=['1', '2'], default='1'),
        **STATE_MOD_ARG,
        **OPN_MOD_ARGS,
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

    # do api interactions here
    exists = True  # check via api if the item already exists
    # session.get(cnf={
    #     'module': 'API-Module',
    #     'controller': 'API-Controller',
    #     'command': 'API-info-command',
    #     'data': {'tests'}
    # })

    if exists:
        result['diff']['before'] = 'test'  # set to current value for diff-mode

    if module.params['state'] == 'absent':
        if exists:
            result['changed'] = True
            if not module.check_mode:
                # remove item via api if not in check-mode
                # session.post(cnf={
                #     'module': 'API-Module',
                #     'controller': 'API-Controller',
                #     'command': 'API-delete-command',
                #     'params': ['uuid'],
                # })
                pass

    else:
        if exists:
            value_changed = True  # compare existing item config with configured one
            if value_changed:
                result['diff']['after'] = 'tests'  # set to configured value(s)
                if not module.check_mode:
                    # update item via api if not in check-mode
                    # session.post(cnf={
                    #     'module': 'API-Module',
                    #     'controller': 'API-Controller',
                    #     'command': 'API-update-command',
                    #     'data': {'tests'},
                    #     'params': ['uuid'],
                    # })
                    pass

        else:
            result['diff']['after'] = 'tests'  # set to configured value(s)
            if not module.check_mode:
                # create item via api if not in check-mode
                # session.post(cnf={
                #     'module': 'API-Module',
                #     'controller': 'API-Controller',
                #     'command': 'API-add-command',
                #     'data': {'tests'},
                # })
                pass

    # don't forget to call the 'reload' endpoint to activate the changes (if available/needed)

    # cleanup and exit

    session.close()
    result['diff'] = diff_remove_empty(result['diff'])
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
