#!/usr/bin/env python3

# Copyright: (C) 2023, AnsibleGuy <guy@ansibleguy.net>
# GNU General Public License v3.0+ (see https://www.gnu.org/licenses/gpl-3.0.txt)

# see: https://docs.opnsense.org/development/api/plugins/bind.html

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.handler import \
    module_dependency_error, MODULE_EXCEPTIONS

try:
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.utils import profiler
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.main import \
        diff_remove_empty
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.defaults.main import \
        OPN_MOD_ARGS, EN_ONLY_MOD_ARG, RELOAD_MOD_ARG
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.main.bind_blocklist import Blocklist

except MODULE_EXCEPTIONS:
    module_dependency_error()

PROFILE = False  # create log to profile time consumption

DOCUMENTATION = 'https://opnsense.ansibleguy.net/en/latest/modules/bind.html'
EXAMPLES = 'https://opnsense.ansibleguy.net/en/latest/modules/bind.html'

BL_MAPPING = {
    'AdAway List': 'aa',
    'AdGuard List': 'ag',
    'Blocklist.site Ads': 'bla',
    'Blocklist.site Fraud': 'blf',
    'Blocklist.site Phishing': 'blp',
    'Cameleon List': 'ca',
    'Easy List': 'el',
    'EMD Malicious Domains List': 'emd',
    'Easyprivacy List': 'ep',
    'hpHosts Ads': 'hpa',
    'hpHosts FSA': 'hpf',
    'hpHosts PSH': 'hpp',
    'hpHosts PUP': 'hup',
    'Malwaredomain List': 'mw',
    'NoCoin List': 'nc',
    'PornTop1M List': 'pt',
    'Ransomware Tracker List': 'rw',
    'Simple Ad List': 'sa',
    'Simple Tracker List': 'st',
    'Steven Black List': 'sb',
    'WindowsSpyBlocker (spy)': 'ws',
    'WindowsSpyBlocker (update)': 'wsu',
    'WindowsSpyBlocker (extra)': 'wse',
    'YoYo List': 'yy',
}


def run_module():
    module_args = dict(
        block=dict(
            type='list', elements='str', required=False, choices=list(BL_MAPPING.keys()),
            aliases=['lists'], default=[],
            description="Blocklist's you want to enable"
        ),
        exclude=dict(
            type='list', elements='str', required=False, default=[],
            aliases=['safe_list'],
            description='Domains to exclude from the filter'
        ),
        safe_google=dict(
            type='bool', required=False, default=False, aliases=['safe_search_google'],
        ),
        safe_duckduckgo=dict(
            type='bool', required=False, default=False, aliases=['safe_search_duckduckgo'],
        ),
        safe_youtube=dict(
            type='bool', required=False, default=False, aliases=['safe_search_youtube'],
        ),
        safe_bing=dict(
            type='bool', required=False, default=False, aliases=['safe_search_bing'],
        ),
        **EN_ONLY_MOD_ARG,
        **OPN_MOD_ARGS,
        **RELOAD_MOD_ARG,
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

    translated_lists = []
    for k in module.params['block']:
        translated_lists.append(BL_MAPPING[k])

    module.params['block'] = translated_lists

    bl = Blocklist(module=module, result=result)

    def process():
        bl.check()
        bl.process()
        if result['changed'] and module.params['reload']:
            bl.reload()

    if PROFILE or module.params['debug']:
        profiler(check=process, log_file='bind_blocklist.log')
        # log in /tmp/ansibleguy.opnsense/

    else:
        process()

    bl.s.close()
    result['diff'] = diff_remove_empty(result['diff'])
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
