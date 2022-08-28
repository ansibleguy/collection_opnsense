#!/usr/bin/python3

# Copyright: (C) 2022, AnsibleGuy <guy@ansibleguy.net>
# GNU General Public License v3.0+ (see https://www.gnu.org/licenses/gpl-3.0.txt)

# see: https://docs.opnsense.org/development/api/core/firmware.html

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.api import Session
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.defaults import OPN_MOD_ARGS

DOCUMENTATION = 'https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_package.md'
EXAMPLES = 'https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_package.md'


def run_module():
    module_args = dict(
        name=dict(type='str', required=True),
        action=dict(
            type='str', required=True,
            choices=['install', 'reinstall', 'remove', 'lock', 'unlock']
        ),
        **OPN_MOD_ARGS
    )

    result = dict(
        changed=False,
        version=None,
        installed=False,
        locked=False,
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True,
    )

    session = Session(module=module)
    session.start(timeout=10.0)
    call_cnf = {  # config shared by all calls
        'module': 'core',
        'controller': 'firmware',
    }

    # checking current state of package
    package_stati = session.get(cnf={'command': 'info', **call_cnf})['package']

    for pkg in package_stati:
        if pkg['name'] == module.params['name']:
            if module.params['debug']:
                module.warn(f"Package status: '{pkg}'")

            result['version'] = pkg['version']

            if pkg['installed'] in ['1', 1, True]:
                result['installed'] = True

            if pkg['locked'] in ['1', 1, True]:
                result['locked'] = True

    # execute action if needed
    call_cnf['params'] = [module.params['name']]

    if module.params['action'] in ['reinstall', 'remove', 'install'] and \
            result['locked']:
        module.fail_json(
            f"Unable to execute action '{module.params['action']}' - "
            f"package is locked!"
        )

    if result['installed'] and \
            module.params['action'] in ['reinstall', 'remove', 'lock', 'unlock']:

        if module.params['action'] == 'lock':
            result['locked'] = True

        elif module.params['action'] == 'unlock':
            result['locked'] = False

        result['changed'] = True
        session.post(cnf={
            'command': module.params['action'],
            **call_cnf
        })

    elif not result['installed'] and module.params['action'] == 'install':
        result['changed'] = True
        session.post(cnf={
            'command': module.params['action'],
            **call_cnf
        })

    session.close()
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
