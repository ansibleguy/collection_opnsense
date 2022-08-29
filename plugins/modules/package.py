#!/usr/bin/python3

# Copyright: (C) 2022, AnsibleGuy <guy@ansibleguy.net>
# GNU General Public License v3.0+ (see https://www.gnu.org/licenses/gpl-3.0.txt)

# pylint: disable=R0912,R0915
# todo: clean up branching

# see: https://docs.opnsense.org/development/api/core/firmware.html

from time import sleep

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.api import Session
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.defaults import OPN_MOD_ARGS

DOCUMENTATION = 'https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_package.md'
EXAMPLES = 'https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_package.md'


def run_module():
    module_args = dict(
        name=dict(type='list', required=True, description='Package or list of packages to process'),
        action=dict(
            type='str', required=True,
            choices=['install', 'reinstall', 'remove', 'lock', 'unlock']
        ),
        wait_time=dict(
            type='int', required=False, default=1,
            description='The firewall needs some time to update package info'
        ),
        **OPN_MOD_ARGS
    )

    result = dict(
        changed=False,
        version=None,
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
    session.start(timeout=10.0)
    call_cnf = {  # config shared by all calls
        'module': 'core',
        'controller': 'firmware',
    }

    # checking current state of package
    package_stati = session.get(cnf={'command': 'info', **call_cnf})['package']

    for pkg_name in module.params['name']:
        _before = {'installed': False, 'locked': False}
        _changed = False

        for pkg_status in package_stati:
            if pkg_status['name'] == pkg_name:
                if module.params['debug']:
                    module.warn(f"Package status: '{pkg_status}'")

                _before['version'] = pkg_status['version']

                if pkg_status['installed'] in ['1', 1, True]:
                    _before['installed'] = True

                if pkg_status['locked'] in ['1', 1, True]:
                    _before['locked'] = True

        _after = _before.copy()

        # execute action if needed
        call_cnf['params'] = [pkg_name]

        if module.params['action'] in ['reinstall', 'remove', 'install'] and \
                _before['locked']:
            module.fail_json(
                f"Unable to execute action '{module.params['action']}' - "
                f"package is locked!"
            )

        if _before['installed'] and \
                module.params['action'] in ['reinstall', 'remove', 'lock', 'unlock']:

            run = False

            if module.params['action'] == 'lock':
                if not _before['locked']:
                    run = True
                    _after['locked'] = True

            elif module.params['action'] == 'unlock':
                if _before['locked']:
                    run = True
                    _after['locked'] = False

            elif module.params['action'] == 'remove':
                _after['installed'] = False

            else:
                run = True

            _changed = True
            if not module.check_mode and run:
                session.post(cnf={
                    'command': module.params['action'],
                    **call_cnf
                })

        elif not _before['installed'] and module.params['action'] == 'install':
            _changed = True
            _after['installed'] = True
            if not module.check_mode:
                session.post(cnf={
                    'command': module.params['action'],
                    **call_cnf
                })

        if _changed:
            sleep(module.params['wait_time'])  # time for the box to update package info
            result['changed'] = True

        result['diff']['before'][pkg_name] = _before
        result['diff']['after'][pkg_name] = _after

    session.close()
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
