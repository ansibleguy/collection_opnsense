#!/usr/bin/python3

# Copyright: (C) 2022, AnsibleGuy <guy@ansibleguy.net>
# GNU General Public License v3.0+ (see https://www.gnu.org/licenses/gpl-3.0.txt)

# see: https://docs.opnsense.org/development/api/core/monit.html

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.handler import \
    module_dependency_error, MODULE_EXCEPTIONS

try:
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.utils import profiler
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.main import diff_remove_empty
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.defaults.main import \
        OPN_MOD_ARGS, STATE_MOD_ARG, RELOAD_MOD_ARG
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.main.monit_service import Service

except MODULE_EXCEPTIONS as e:
    module_dependency_error()

PROFILE = False  # create log to profile time consumption

DOCUMENTATION = 'https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_monit.md'
EXAMPLES = 'https://github.com/ansibleguy/collection_opnsense/blob/stable/docs/use_monit.md'


def run_module():
    module_args = dict(
        name=dict(type='str', required=True, description='Unique service name'),
        type=dict(
            type='str', required=False,
            choises=[
                'process', 'file', 'fifo', 'filesystem', 'directory', 'host', 'system',
                'custom', 'network',
            ]
        ),
        pidfile=dict(type='path', required=False, default=''),
        match=dict(type='str', required=False, default=''),
        path=dict(
            type='path', required=False, default='',
            description='According to the service type path can be a file or a directory',
        ),
        service_timeout=dict(type='int', required=False, default=300, aliases=['svc_timeout']),
        address=dict(
            type='str', required=False, default='',
            description="The target IP address for 'Remote Host' and 'Network' checks",
        ),
        interface=dict(
            type='str', required=False, default='',
            description="The existing Interface for 'Network' checks"
        ),
        start=dict(
            type='str', required=False, default='',
            description='Absolute path to the executable with its arguments to run '
                        'at service-start',
        ),
        stop=dict(
            type='str', required=False, default='',
            description='Absolute path to the executable with its arguments to run '
                        'at service-stop',
        ),
        tests=dict(type='list', elements='str', required=False, default=[]),
        depends=dict(
            type='list', elements='str', required=False, default=[],
            description='Optionally define a (list of) service(s) which are required '
                        'before monitoring this one, if any of the dependencies are either '
                        'stopped or unmonitored this service will stop/unmonitor too',
        ),
        polltime=dict(
            type='str',  required=False, default='',
            description='Set the service poll time. Either as a number of cycles '
                        "'NUMBER CYCLES' or Cron-style '* 8-19 * * 1-5'"
        ),
        description=dict(type='str', required=False, default='', aliases=['desc']),
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

    svc = Service(module=module, result=result)

    def process():
        svc.check()
        svc.process()
        if result['changed'] and module.params['reload']:
            svc.reload()

    if PROFILE or module.params['debug']:
        profiler(check=process, log_file='monit_service.log')
        # log in /tmp/ansibleguy.opnsense/

    else:
        process()

    svc.s.close()
    result['diff'] = diff_remove_empty(result['diff'])
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
