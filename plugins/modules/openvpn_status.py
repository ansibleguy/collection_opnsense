#!/usr/bin/env python3

# Copyright: (C) 2024, AnsibleGuy <guy@ansibleguy.net>
# GNU General Public License v3.0+ (see https://www.gnu.org/licenses/gpl-3.0.txt)

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.handler import \
    module_dependency_error, MODULE_EXCEPTIONS

try:
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.defaults.main import \
        OPN_MOD_ARGS
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.api import single_get

except MODULE_EXCEPTIONS:
    module_dependency_error()

# DOCUMENTATION = 'https://opnsense.ansibleguy.net/en/latest/modules/openvpn.html'
# EXAMPLES = 'https://opnsense.ansibleguy.net/en/latest/modules/openvpn.html'

TARGET_MAPPING = {
    'sessions': 'searchSessions',
    'routes': 'searchRoutes',
}


def run_module():
    module_args = dict(
        target=dict(
            type='str', required=False, default='sessions', aliases=['kind'],
            choices=['sessions', 'routes'],
            description='What information to query'
        ),
        **OPN_MOD_ARGS,
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True,
    )

    info = single_get(
        module=module,
        cnf={
            'module': 'openvpn',
            'controller': 'service',
            'command': TARGET_MAPPING[module.params['target']],
        }
    )

    if 'rows' in info:
        info = info['rows']

        if isinstance(info, str):
            info = info.strip()

    module.exit_json(data=info)


def main():
    run_module()


if __name__ == '__main__':
    main()
