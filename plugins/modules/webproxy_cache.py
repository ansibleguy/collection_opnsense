#!/usr/bin/env python3

# Copyright: (C) 2022, AnsibleGuy <guy@ansibleguy.net>
# GNU General Public License v3.0+ (see https://www.gnu.org/licenses/gpl-3.0.txt)

# template to be copied to implement new modules

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.handler import \
    module_dependency_error, MODULE_EXCEPTIONS

try:
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.utils import profiler
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.main import \
        diff_remove_empty
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.defaults.main import \
        OPN_MOD_ARGS, RELOAD_MOD_ARG
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.main.webproxy_cache import Cache

except MODULE_EXCEPTIONS:
    module_dependency_error()

PROFILE = False  # create log to profile time consumption

DOCUMENTATION = 'https://opnsense.ansibleguy.net/en/latest/modules/webproxy.html'
EXAMPLES = 'https://opnsense.ansibleguy.net/en/latest/modules/webproxy.html'

BLANK_VALUES = {
    'memory_cache_mode': 'default',
}


def run_module():
    module_args = dict(
        memory_mb=dict(
            type='int', required=False, default=256, aliases=['memory', 'mem'],
            description='The cache memory size to use or zero to disable completely'
        ),
        size_mb=dict(
            type='int', required=False, default=100, aliases=['size'],
            description='The storage size for the local cache'
        ),
        directory=dict(
            type='str', required=False, default='/var/squid/cache', aliases=['dir'],
            description='The location for the local cache'
        ),
        layer_1=dict(
            type='int', required=False, default=16, aliases=['layer1', 'l1'],
            description='The number of first-level subdirectories for the local cache'
        ),
        layer_2=dict(
            type='int', required=False, default=256, aliases=['layer2', 'l2'],
            description='The number of second-level subdirectories for the local cache'
        ),
        size_mb_max=dict(
            type='int', required=False, default=4,
            aliases=['maximum_object_size', 'max_size'],
            description='The maximum object size'
        ),
        memory_kb_max=dict(
            type='int', required=False, default=512,
            aliases=['maximum_object_size_in_memory', 'max_memory', 'max_mem'],
            description='The maximum object size'
        ),
        memory_cache_mode=dict(
            type='str', required=False, default='default',
            aliases=['cache_mode', 'mode'],
            choices=['always', 'disk', 'network', 'default'],
            description='Controls which objects to keep in the memory cache (cache_mem) always: '
                        'Keep most recently fetched objects in memory (default) disk: Only disk '
                        'cache hits are kept in memory, which means an object must first be '
                        'cached on disk and then hit a second time before cached in memory. '
                        'network: Only objects fetched from network is kept in memory'
        ),
        cache_linux_packages=dict(
            type='bool', required=False, default=False,
            description='Enable or disable the caching of packages for linux distributions. '
                        'This makes sense if you have multiple servers in your network and do '
                        'not host your own package mirror. This will reduce internet traffic '
                        'usage but increase disk access'
        ),
        cache_windows_updates=dict(
            type='bool', required=False, default=False,
            description='Enable or disable the caching of Windows updates. This makes sense '
                        "if you don't have a WSUS server. If you can setup a WSUS server, "
                        'this solution should be preferred'
        ),
        **RELOAD_MOD_ARG,
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

    for field, value in BLANK_VALUES.items():
        if module.params[field] == value:
            module.params[field] = ''  # BlankDesc

    c = Cache(module=module, result=result)

    def process():
        c.check()
        c.process()
        if result['changed'] and module.params['reload']:
            c.reload()

    if PROFILE or module.params['debug']:
        profiler(check=process, log_file='webproxy_cache.log')
        # log in /tmp/ansibleguy.opnsense/

    else:
        process()

    c.s.close()
    result['diff'] = diff_remove_empty(result['diff'])
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
