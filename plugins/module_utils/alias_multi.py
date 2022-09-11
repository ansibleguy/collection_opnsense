from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.alias_defaults import \
    ALIAS_DEFAULTS, ALIAS_MOD_ARGS, ALIAS_MOD_ARG_ALIASES
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper import \
    diff_remove_empty, ensure_list
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.api import Session
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.multi_helper import \
    validate_single, convert_aliases
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.alias_obj import Alias
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.rule_obj import Rule


def process(m: AnsibleModule, p: dict, r: dict, ):
    session = Session(module=m)
    meta_alias = Alias(module=m, session=session, result={})
    existing_aliases = meta_alias.search_call()
    existing_rules = Rule(module=m, session=session, result={}).search_call()

    overrides = {'debug': p['debug']}

    if p['state'] is not None:
        overrides['state'] = p['state']

    if p['enabled'] is not None:
        overrides['enabled'] = p['enabled']

    # build list of valid aliases or fail if invalid config is not permitted
    valid_aliases = []
    for alias_name, alias_config in p['aliases'].items():
        # build config and validate it the same way the module initialization would do
        if alias_config is None:
            alias_config = {}

        alias_config = convert_aliases(cnf=alias_config, aliases=ALIAS_MOD_ARG_ALIASES)

        real_cnf = {
            **ALIAS_DEFAULTS,
            **alias_config,
            **{
                'name': alias_name,
                'firewall': p['firewall'],
            },
            **overrides,
        }
        real_cnf['content'] = list(map(str, ensure_list(real_cnf['content'])))

        if real_cnf['debug']:
            m.warn(f"Validating alias: '{alias_config}'")

        if validate_single(
                module=m, module_args=ALIAS_MOD_ARGS, log_mod='rule',
                key=alias_name, cnf=real_cnf,
        ):
            valid_aliases.append(real_cnf)

    for alias_config in valid_aliases:
        # process single alias like in the 'alias' module
        alias_result = dict(
            changed=False,
            diff={
                'before': {},
                'after': {},
            }
        )

        p['debug'] = alias_config['debug']  # per rule switch

        if p['debug'] or p['output_info']:
            m.warn(f"Processing alias: '{alias_config}'")

        alias = Alias(
            module=m,
            result=alias_result,
            cnf=alias_config,
            session=session,
            fail=p['fail_verification'],
        )
        # save on requests
        alias.existing_aliases = existing_aliases
        alias.existing_rules = existing_rules

        alias.check()
        alias.process()

        if alias_result['changed']:
            r['changed'] = True
            alias_result['diff'] = diff_remove_empty(alias_result['diff'])

            if 'before' in alias_result['diff']:
                r['diff']['before'].update(alias_result['diff']['before'])

            if 'after' in alias_result['diff']:
                r['diff']['after'].update(alias_result['diff']['after'])

    if r['changed'] and p['reload']:
        meta_alias.reload()

    session.close()
