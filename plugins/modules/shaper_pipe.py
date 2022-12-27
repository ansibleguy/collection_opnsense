#!/usr/bin/env python3

# Copyright: (C) 2022, AnsibleGuy <guy@ansibleguy.net>
# GNU General Public License v3.0+ (see https://www.gnu.org/licenses/gpl-3.0.txt)

# see: https://docs.opnsense.org/development/api/core/trafficshaper.html

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.handler import \
    module_dependency_error, MODULE_EXCEPTIONS

try:
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.utils import profiler
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.main import diff_remove_empty
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.defaults.main import \
        OPN_MOD_ARGS, STATE_MOD_ARG, RELOAD_MOD_ARG
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.main.shaper_pipe import Pipe

except MODULE_EXCEPTIONS:
    module_dependency_error()

PROFILE = False  # create log to profile time consumption

DOCUMENTATION = 'https://opnsense.ansibleguy.net/en/latest/modules/shaper.html'
EXAMPLES = 'https://opnsense.ansibleguy.net/en/latest/modules/shaper.html'


def run_module():
    module_args = dict(
        # id=dict(type='int', required=True, alises=['number']),  # ignored and set automatically
        bandwidth=dict(
            type='int', required=False, aliases=['bw']
        ),
        bandwidth_metric=dict(
            type='str', required=False, default='Mbit', aliases=['bw_metric'],
            choises=['bit', 'Kbit', 'Mbit', 'Gbit'],
        ),
        queue=dict(type='str', required=False, default=''),
        mask=dict(
            type='str', required=False, default='none', choices=['none', 'src-ip', 'dst-ip']
        ),
        buckets=dict(type='str', required=False, default=''),
        scheduler=dict(
            type='str', required=False, default='',
            choises=['', 'fifo', 'rr', 'qfq', 'fq_codel', 'fq_pie']
        ),
        pie_enable=dict(type='bool', required=False, default=False, aliases=['pie']),
        codel_enable=dict(type='bool', required=False, default=False, aliases=['codel']),
        codel_ecn_enable=dict(type='bool', required=False, default=False, aliases=['codel_ecn']),
        codel_target=dict(type='str', required=False, default=''),
        codel_interval=dict(type='str', required=False, default=''),
        fqcodel_quantum=dict(type='str', required=False, default=''),
        fqcodel_limit=dict(type='str', required=False, default=''),
        fqcodel_flows=dict(type='str', required=False, default=''),
        delay=dict(type='str', required=False, default=''),
        description=dict(type='str', required=True, aliases=['desc']),
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

    pipe = Pipe(module=module, result=result)

    def process():
        pipe.check()
        pipe.process()
        if result['changed'] and module.params['reload']:
            pipe.reload()

    if PROFILE or module.params['debug']:
        profiler(check=process, log_file='shaper_pipe.log')
        # log in /tmp/ansibleguy.opnsense/

    else:
        process()

    pipe.s.close()
    result['diff'] = diff_remove_empty(result['diff'])
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
