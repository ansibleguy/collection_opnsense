#!/usr/bin/python3

# Copyright: (C) 2022, AnsibleGuy <guy@ansibleguy.net>
# GNU General Public License v3.0+ (see https://www.gnu.org/licenses/gpl-3.0.txt)

# see: https://docs.opnsense.org/development/api/core/unbound.html

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.defaults import OPN_MOD_ARGS
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.unbound_forward_obj import Forward

DOCUMENTATION = 'https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_unbound_forwarding.md'
EXAMPLES = 'https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_unbound_forwarding.md'


def run_module():
    result = dict(
        changed=False,
        forwardings=[],
    )

    module = AnsibleModule(
        argument_spec=OPN_MOD_ARGS,
        supports_check_mode=True,
    )

    fwd = Forward(module=module, result=result)

    result['forwardings'] = fwd.search_call()

    fwd.s.close()
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
