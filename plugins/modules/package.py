#!/usr/bin/python3

# Copyright: (C) 2022, AnsibleGuy <guy@ansibleguy.net>
# GNU General Public License v3.0+ (see https://www.gnu.org/licenses/gpl-3.0.txt)

# see: https://docs.opnsense.org/development/api/core/firmware.html

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.handler import \
    module_dependency_error, MODULE_EXCEPTIONS

try:
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.utils import profiler
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.main.package_main import process
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.defaults.main import OPN_MOD_ARGS

except MODULE_EXCEPTIONS:
    module_dependency_error()

PROFILE = False  # create log to profile time consumption

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
        post_sleep=dict(
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

    if PROFILE or module.params['debug']:
        profiler(
            check=process, kwargs=dict(
                m=module, p=module.params, r=result,
            ),
            log_file='package.log'  # /tmp/ansibleguy.opnsense/
        )

    else:
        process(m=module, p=module.params, r=result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
