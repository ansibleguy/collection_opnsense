#!/usr/bin/python3

# Copyright: (C) 2022, AnsibleGuy <guy@ansibleguy.net>
# GNU General Public License v3.0+ (see https://www.gnu.org/licenses/gpl-3.0.txt)

# see: https://docs.opnsense.org/development/api/core/routes.html

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.defaults import \
    OPN_MOD_ARGS
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.route_obj import Route

DOCUMENTATION = 'https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_route.md'
EXAMPLES = 'https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_route.md'


def run_module():
    module_args = dict(
        **OPN_MOD_ARGS,
    )

    result = dict(
        changed=False,
        routes=[]
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True,  # practically not - but it will not change anything
    )

    route = Route(module=module, result=result)
    result['routes'] = route.search_call()

    route.s.close()
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
