#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (C) 2025, Pascal Rath <contact+opnsense@OXL.at>
# GNU General Public License v3.0+ (see https://www.gnu.org/licenses/gpl-3.0.txt)

# see: https://docs.opnsense.org/development/api/core/firewall.html

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.handler import \
    module_dependency_error, MODULE_EXCEPTIONS

try:
    from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.wrapper import \
        module_multi_wrapper
    from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.multi import \
        build_multi_mod_args, MultiModuleCallbacks
    from ansible_collections.oxlorg.opnsense.plugins.module_utils.defaults.main import \
        RELOAD_MOD_ARG_DEF_FALSE, OPN_MOD_ARGS
    from ansible_collections.oxlorg.opnsense.plugins.module_utils.defaults.alias import \
        ALIAS_MOD_ARGS
    from ansible_collections.oxlorg.opnsense.plugins.module_utils.main.alias import Alias
    from ansible_collections.oxlorg.opnsense.plugins.module_utils.helper.main import ensure_list
    from ansible_collections.oxlorg.opnsense.plugins.module_utils.helper.alias import \
        builtin_alias, build_updatefreq, filter_builtin_alias
    from ansible_collections.oxlorg.opnsense.plugins.module_utils.helper.translate import \
        get_simple_existing

except MODULE_EXCEPTIONS:
    module_dependency_error()


# DOCUMENTATION = 'https://ansible-opnsense.oxl.app/modules/alias.html'
# EXAMPLES = 'https://ansible-opnsense.oxl.app/modules/alias.html'


class MultiCallbacks(MultiModuleCallbacks):
    @staticmethod
    def get_existing(meta_entry: Alias) -> dict:
        existing_raw = meta_entry.search()
        return {
            'main': filter_builtin_alias(
                get_simple_existing(
                    entries=existing_raw,
                    simplify_func=meta_entry.simplify_existing,
                )
            ),
            'categories': meta_entry._get_category_selection(),
        }

    @staticmethod
    def set_existing(entry: Alias, cache: dict):
        entry.existing_entries = cache['main']
        entry.existing_categories = cache['categories']

    @staticmethod
    def build(entry: dict) -> dict:
        entry['content'] = list(map(str, ensure_list(entry['content'])))
        if 'updatefreq_days' in entry:
            entry['updatefreq_days'] = build_updatefreq(entry['updatefreq_days'])

        return entry

    @staticmethod
    def purge_exclude(entry: dict) -> bool:
        return builtin_alias(entry['name'])


def run_module():
    entry_multi_args = build_multi_mod_args(
        mod_args=ALIAS_MOD_ARGS,
        aliases=['aliases'],
        not_required=['name'],
    )

    module_args = dict(
        **entry_multi_args,
        **OPN_MOD_ARGS,
        **RELOAD_MOD_ARG_DEF_FALSE,  # default-true takes pretty long sometimes (urltables and so on)
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
        }
    )

    module_multi_wrapper(
        module=module,
        result=result,
        obj=Alias,
        kind='alias',
        entry_args=entry_multi_args,
        callbacks=MultiCallbacks(),
    )
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
