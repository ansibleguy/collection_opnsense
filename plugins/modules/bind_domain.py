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
        OPN_MOD_ARGS, STATE_MOD_ARG, RELOAD_MOD_ARG
    from ansible_collections.ansibleguy.opnsense.plugins.module_utils.main.bind_domain import \
        Domain

except MODULE_EXCEPTIONS:
    module_dependency_error()

PROFILE = False  # create log to profile time consumption

# DOCUMENTATION = 'https://opnsense.ansibleguy.net/en/latest/modules/bind.html'
# EXAMPLES = 'https://opnsense.ansibleguy.net/en/latest/modules/bind.html'


def run_module():
    module_args = dict(
        name=dict(type='str', required=True, aliases=['domain_name', 'domain']),
        mode=dict(
            type='str', required=False, default='primary', choices=['primary', 'secondary']
        ),
        primary=dict(
            type='list', elements='str', required=False, aliases=['primary_ip', 'master', 'master_ip'], default=[],
            description='Set the IP address of primary server when using secondary mode'
        ),
        transfer_key_algo=dict(
            type='str', required=False, default='',
            choices=[
                'hmac-sha512', 'hmac-sha384', 'hmac-sha256', 'hmac-sha224',
                'hmac-sha1', 'hmac-md5', '',
            ]
        ),
        transfer_key_name=dict(type='str', required=False, default=''),
        transfer_key=dict(type='str', required=False, default='', no_log=True),
        allow_notify=dict(
            type='list', elements='str', required=False, default=[],
            aliases=['allow_notify_secondary', 'allow_notify_slave'],
            description='A list of allowed IP addresses to receive notifies from'
        ),
        transfer_acl=dict(
            type='list', elements='str', required=False, default=[], aliases=['allow_transfer'],
            description='An ACL where you allow which server can retrieve this zone'
        ),
        query_acl=dict(
            type='list', elements='str', required=False, default=[], aliases=['allow_query'],
            description='An ACL where you allow which client are allowed '
                        'to query this zone'
        ),
        ttl=dict(
            type='int', required=False, default=86400,
            description='The general Time To Live for this zone'
        ),
        refresh=dict(
            type='int', required=False, default=21600,
            description='The time in seconds after which name servers should '
                        'refresh the zone information'
        ),
        retry=dict(
            type='int', required=False, default=3600,
            description='The time in seconds after which name servers should '
                        'retry requests if the primary does not respond'
        ),
        expire=dict(
            type='int', required=False, default=3542400,
            description='The time in seconds after which name servers should '
                        'stop answering requests if the primary does not respond'
        ),
        negative=dict(
            type='int', required=False, default=3600,
            description='The time in seconds after which an entry for a '
                        'non-existent record should expire from cache'
        ),
        admin_mail=dict(
            type='str', required=False, default='mail.opnsense.localdomain',
            description='The mail address of zone admin. A @-sign will '
                        'automatically be replaced with a dot in the zone data'
        ),
        server=dict(
            type='str', required=False, default='opnsense.localdomain', aliases=['dns_server'],
            description='Set the DNS server hosting this file. This should usually '
                        'be the FQDN of your firewall where the BIND plugin is installed'
        ),
        # serial=dict(type='str', required=False, default=''),
        **STATE_MOD_ARG,
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

    d = Domain(module=module, result=result)

    def process():
        d.check()
        d.process()
        if result['changed'] and module.params['reload']:
            d.reload()

    if PROFILE or module.params['debug']:
        profiler(check=process, log_file='bind_domain.log')
        # log in /tmp/ansibleguy.opnsense/

    else:
        process()

    d.s.close()
    result['diff'] = diff_remove_empty(result['diff'])
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
