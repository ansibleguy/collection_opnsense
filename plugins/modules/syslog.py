#!/usr/bin/python3

# Copyright: (C) 2022, AnsibleGuy <guy@ansibleguy.net>
# GNU General Public License v3.0+ (see https://www.gnu.org/licenses/gpl-3.0.txt)

# see: https://docs.opnsense.org/development/api/core/syslog.html

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.handler import \
    module_dependency_error, MODULE_EXCEPTIONS

try:
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.utils import profiler
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.main import diff_remove_empty
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.defaults.main import \
        OPN_MOD_ARGS, STATE_MOD_ARG, RELOAD_MOD_ARG
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.main.syslog import Syslog

except MODULE_EXCEPTIONS:
    module_dependency_error()

PROFILE = False  # create log to profile time consumption

DOCUMENTATION = 'https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_syslog.md'
EXAMPLES = 'https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_syslog.md'


def run_module():
    module_args = dict(
        target=dict(
            type='str', required=True, aliases=['hostname', 'tgt', 'server', 'srv'],
            description='Server to forward the logs to'
        ),
        port=dict(type='int', required=False, default=514, aliases=['p']),
        transport=dict(
            type='str', required=False, default='udp4', aliases=['trans', 't'],
            choises=['udp4', 'tcp4', 'udp6', 'tcp6', 'tls4', 'tls6'],
        ),
        level=dict(
            type='list', required=False, aliases=['lv', 'lvl'], elements='str',
            default=['info', 'notice', 'warn', 'err', 'crit', 'alert', 'emerg'],
            choices=['debug', 'info', 'notice', 'warn', 'err', 'crit', 'alert', 'emerg'],
        ),
        program=dict(
            type='list', required=False, aliases=['prog'], default=[], elements='str',
            description='Limit applications to send logs from'
        ),
        facility=dict(
            type='list', required=False, aliases=['fac'], default=[], elements='str',
            choices=[
                'kern', 'user', 'mail', 'daemon', 'auth', 'syslog', 'lpr', 'news', 'uucp', 'cron', 'authpriv',
                'ftp', 'ntp', 'security', 'console', 'local0', 'local1', 'local2', 'local3', 'local4',
                'local5', 'local6', 'local7',
            ],
        ),
        certificate=dict(type='str', required=False, aliases=['cert'], default=''),
        rfc5424=dict(type='bool', required=False, default=False),  # not getting current value from response
        description=dict(type='str', required=False, default='', aliases=['desc']),
        match_fields=dict(
            type='list', required=False, elements='str',
            description='Fields that are used to match configured syslog-destinations with the running config - '
                        "if any of those fields are changed, the module will think it's a new entry",
            choises=[
                'target', 'transport', 'facility', 'program', 'level',
                'port', 'description',
            ],
            default=['target', 'facility', 'program'],
        ),
        **RELOAD_MOD_ARG,
        **STATE_MOD_ARG,
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

    module.params['level'].sort()

    syslog = Syslog(module=module, result=result)

    def process():
        syslog.check()
        syslog.process()
        if result['changed'] and module.params['reload']:
            syslog.reload()

    if PROFILE or module.params['debug']:
        profiler(check=process, log_file='syslog.log')
        # log in /tmp/ansibleguy.opnsense/

    else:
        process()

    syslog.s.close()
    result['diff'] = diff_remove_empty(result['diff'])
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
