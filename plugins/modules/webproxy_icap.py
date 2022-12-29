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
        OPN_MOD_ARGS, EN_ONLY_MOD_ARG, RELOAD_MOD_ARG
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.main.webproxy_icap import General

except MODULE_EXCEPTIONS:
    module_dependency_error()

PROFILE = False  # create log to profile time consumption

DOCUMENTATION = 'https://opnsense.ansibleguy.net/en/latest/modules/webproxy.html'
EXAMPLES = 'https://opnsense.ansibleguy.net/en/latest/modules/webproxy.html'


def run_module():
    module_args = dict(
        request_url=dict(
            type='str', required=False, default='icap://[::1]:1344/avscan',
            aliases=['request', 'request_target'],
            description='The url where the REQMOD requests should be sent to'
        ),
        response_url=dict(
            type='str', required=False, default='icap://[::1]:1344/avscan',
            aliases=['response', 'response_target'],
            description='The url where the RESPMOD requests should be sent to'
        ),
        ttl=dict(
            type='int', required=False, default=60, aliases=['default_ttl']
        ),
        send_client_ip=dict(
            type='bool', required=False, default=True, aliases=['send_client'],
            description='If you enable this option, the client IP address will be sent to '
                        'the ICAP server. This can be useful if you want to filter traffic '
                        'based on IP addresses'
        ),
        send_username=dict(
            type='bool', required=False, default=False, aliases=['send_user'],
            description='If you enable this option, the username of the client will be sent '
                        'to the ICAP server. This can be useful if you want to filter traffic '
                        'based on usernames. Authentication is required to use usernames'
        ),
        encode_username=dict(
            type='bool', required=False, default=False,
            aliases=['user_encode', 'encode_user', 'enc_user'],
            description='Use this option if your usernames need to be encoded'
        ),
        header_username=dict(
            type='str', required=False, default='X-Username',
            aliases=['header_user', 'user_header'],
            description='The header which should be used to send the username to the ICAP server'
        ),
        preview=dict(
            type='bool', required=False, default=True,
            description='If you use previews, only a part of the data is sent '
                        'to the ICAP server. Setting this option can improve the performance'
        ),
        preview_size=dict(
            type='int', required=False, default=1024,
            description='Size of the preview which is sent to the ICAP server'
        ),
        exclude=dict(
            type='list', elements='str', required=False, default=[],
            description='Exclusion list destination domains.You may use a regular expression, '
                        'use a comma or press Enter for new item. Examples: "mydomain.com" matches '
                        'on "*.mydomain.com"; "https://([a-zA-Z]+)\\.mydomain\\." matches on '
                        '"http(s)://textONLY.mydomain.*"; "\\.gif$" matches on "\\*.gif" but not on '
                        '"\\*.gif\\test"; "\\[0-9]+\\.gif$" matches on "\\123.gif" but not on "\\test.gif"'
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

    g = General(module=module, result=result)

    def process():
        g.check()
        g.process()
        if result['changed'] and module.params['reload']:
            g.reload()

    if PROFILE or module.params['debug']:
        profiler(check=process, log_file='webproxy_icap.log')
        # log in /tmp/ansibleguy.opnsense/

    else:
        process()

    g.s.close()
    result['diff'] = diff_remove_empty(result['diff'])
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
