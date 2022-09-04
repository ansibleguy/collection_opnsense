#!/usr/bin/python3

# Copyright: (C) 2022, AnsibleGuy <guy@ansibleguy.net>
# GNU General Public License v3.0+ (see https://www.gnu.org/licenses/gpl-3.0.txt)

# see: https://docs.opnsense.org/development/api/core/unbound.html

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.defaults import OPN_MOD_ARGS
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.unbound_host_alias_obj import Alias

DOCUMENTATION = 'https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_unbound_host_alias.md'
EXAMPLES = 'https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_unbound_host_alias.md'


def run_module():
    result = dict(
        changed=False,
        aliases={},
    )

    module = AnsibleModule(
        argument_spec=OPN_MOD_ARGS,
        supports_check_mode=True,
    )

    alias = Alias(module=module, result=result)

    raw_aliases = alias.search_call()

    # filter to get prettier output
    if len(raw_aliases) > 0:
        for uuid, alias_item in raw_aliases.items():
            for host_uuid, host_item in alias_item['host'].items():
                if host_item['selected'] in [1, '1', True]:
                    result['aliases'][uuid] = dict(
                        description=alias_item['description'],
                        domain=alias_item['domain'],
                        enabled=alias_item['enabled'] in [1, '1', True],
                        hostname=alias_item['hostname'],
                        target={host_uuid: host_item['value']}
                    )
                    break

    alias.s.close()
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
