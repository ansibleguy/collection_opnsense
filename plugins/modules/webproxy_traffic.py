#!/usr/bin/env python3

# Copyright: (C) 2023, AnsibleGuy <guy@ansibleguy.net>
# GNU General Public License v3.0+ (see https://www.gnu.org/licenses/gpl-3.0.txt)

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.handler import \
    module_dependency_error, MODULE_EXCEPTIONS

try:
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.utils import profiler
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.main import \
        diff_remove_empty
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.defaults.main import \
        OPN_MOD_ARGS, EN_ONLY_MOD_ARG, RELOAD_MOD_ARG
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.main.webproxy_traffic import Traffic

except MODULE_EXCEPTIONS:
    module_dependency_error()

PROFILE = False  # create log to profile time consumption

DOCUMENTATION = 'https://opnsense.ansibleguy.net/en/latest/modules/webproxy.html'
EXAMPLES = 'https://opnsense.ansibleguy.net/en/latest/modules/webproxy.html'


def run_module():
    module_args = dict(
        download_kb_max=dict(
            type='str', required=False, default='2048',
            aliases=['download_max', 'download', 'dl_max', 'dl'],
            description='The maximum size for downloads in kilobytes (leave empty to disable)'
        ),
        upload_kb_max=dict(
            type='str', required=False, default='1024',
            aliases=['upload_max', 'upload', 'ul_max', 'ul'],
            description='The maximum size for uploads in kilobytes (leave empty to disable)'
        ),
        throttle_kb_bandwidth=dict(
            type='str', required=False, default='1024',
            aliases=['throttle_bandwidth', 'throttle_bw', 'bandwidth', 'bw'],
            description='The allowed overall bandwidth in kilobits per second (leave empty to disable)'
        ),
        throttle_kb_host_bandwidth=dict(
            type='str', required=False, default='256',
            aliases=['throttle_host_bandwidth', 'throttle_host_bw', 'host_bandwidth', 'host_bw'],
            description='The allowed per host bandwidth in kilobits per second (leave empty to disable)'
        ),
        **RELOAD_MOD_ARG,
        **EN_ONLY_MOD_ARG,
        **OPN_MOD_ARGS,
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

    t = Traffic(module=module, result=result)

    def process():
        t.check()
        t.process()
        if result['changed'] and module.params['reload']:
            t.reload()

    if PROFILE or module.params['debug']:
        profiler(check=process, log_file='webproxy_traffic.log')
        # log in /tmp/ansibleguy.opnsense/

    else:
        process()

    t.s.close()
    result['diff'] = diff_remove_empty(result['diff'])
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
