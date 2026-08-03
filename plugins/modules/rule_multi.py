#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (C) 2025, Pascal Rath <contact+opnsense@OXL.at>
# GNU General Public License v3.0+ (see https://www.gnu.org/licenses/gpl-3.0.txt)

# see: https://docs.opnsense.org/development/api/plugins/firewall.html

from ansible.module_utils.basic import AnsibleModule


from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.handler import \
    module_dependency_error, MODULE_EXCEPTIONS

try:
    from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.wrapper import \
        module_multi_wrapper
    from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.multi import \
        build_multi_mod_args, MultiModuleCallbacks
    from ansible_collections.oxlorg.opnsense.plugins.module_utils.defaults.main import \
        OPN_MOD_ARGS, RELOAD_MOD_ARG
    from ansible_collections.oxlorg.opnsense.plugins.module_utils.defaults.rule import \
        RULE_MOD_ARGS, RULE_MATCH_FIELDS_ARG
    from ansible_collections.oxlorg.opnsense.plugins.module_utils.helper.translate import \
        get_simple_existing
    from ansible_collections.oxlorg.opnsense.plugins.module_utils.main.rule import Rule

except MODULE_EXCEPTIONS:
    module_dependency_error()


# DOCUMENTATION = 'https://ansible-opnsense.oxl.app/modules/rule.html'
# EXAMPLES = 'https://ansible-opnsense.oxl.app/modules/rule.html'


class MultiCallbacks(MultiModuleCallbacks):
    @staticmethod
    def get_existing(meta_entry: Rule) -> dict:
        existing_raw = meta_entry.search(match_fields=meta_entry.p['match_fields'])
        return {
            'main': get_simple_existing(
                entries=existing_raw,
                simplify_func=meta_entry.simplify_existing,
            ),
            'categories': meta_entry._get_category_selection(),
        }

    @staticmethod
    def set_existing(entry: Rule, cache: dict):
        entry.existing_entries = cache['main']
        entry.existing_categories = cache['categories']


def run_module():
    entry_multi_args = build_multi_mod_args(
        mod_args=RULE_MOD_ARGS,
        aliases=['rules'],
    )

    module_args = dict(
        **entry_multi_args,
        **OPN_MOD_ARGS,
        **RELOAD_MOD_ARG,
        **RULE_MATCH_FIELDS_ARG,
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True,
        required_one_of=[
            ('multi', 'multi_purge', 'multi_control.purge_all'),
        ],
    )

    result = dict(
        changed=False,
        diff={
            'before': {},
            'after': {},
        },
    )

    module_multi_wrapper(
        module=module,
        result=result,
        obj=Rule,
        kind='rule',
        entry_args=entry_multi_args,
        callbacks=MultiCallbacks(),
    )
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
