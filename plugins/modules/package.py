#!/usr/bin/python3

# Copyright: (C) 2022, AnsibleGuy <guy@ansibleguy.net>
# GNU General Public License v3.0+ (see https://www.gnu.org/licenses/gpl-3.0.txt)

# see: https://docs.opnsense.org/development/api/core/firmware.html

from time import sleep

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.api import Session
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.defaults import OPN_MOD_ARGS
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.package_obj import Package

DOCUMENTATION = 'https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_package.md'
EXAMPLES = 'https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_package.md'


def run_module():
    module_args = dict(
        name=dict(
            type='list', required=True, elements='str',
            description='Package or list of packages to process'
        ),
        action=dict(
            type='str', required=True,
            choices=['install', 'reinstall', 'remove', 'lock', 'unlock']
        ),
        wait_time=dict(
            type='int', required=False, default=3,
            description='The firewall needs some time to update package info'
        ),
        timeout=dict(type='float', required=False, default=30.0),
        # timeout because of box might update its package info
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
    session.start(timeout=module.params['timeout'])

    # pulling stati of all packages
    package_stati = Package(module=module, session=session, name='').search_call()

    for pkg_name in module.params['name']:
        pkg = Package(module=module, name=pkg_name, session=session,)
        pkg.package_stati = package_stati
        pkg.check()

        # execute action if needed
        if pkg.r['diff']['before']['installed'] and \
                module.params['action'] in ['reinstall', 'remove', 'lock', 'unlock']:
            pkg.change_state()

        elif not pkg.r['diff']['before']['installed'] and \
                module.params['action'] == 'install':
            pkg.install()

        if pkg.r['changed']:
            sleep(module.params['wait_time'])  # time for the box to update package info
            result['changed'] = True

        result['diff']['before'][pkg_name] = pkg.r['diff']['before']
        result['diff']['after'][pkg_name] = pkg.r['diff']['after']

    session.close()
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
