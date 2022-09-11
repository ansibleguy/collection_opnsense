from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.multi_helper import \
    validate_single, convert_aliases
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.rule_defaults import \
    RULE_MOD_ARGS, RULE_DEFAULTS, RULE_MOD_ARG_ALIASES
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper import diff_remove_empty
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.api import Session
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.rule_obj import Rule


def process(m: AnsibleModule, p: dict, r: dict):
    s = Session(module=m)
    existing_rules = Rule(module=m, session=s, result={}).search_call()

    if isinstance(p['key_field'], list):
        # edge case
        p['key_field'] = p['key_field'][0]

    overrides = {
        **p['override'],
        'match_fields': p['match_fields'],
        'debug': p['debug']
    }

    if p['state'] is not None:
        overrides['state'] = p['state']

    if p['enabled'] is not None:
        overrides['enabled'] = p['enabled']

    # build list of valid rules or fail if invalid config is not permitted
    valid_rules = {}
    for rule_key, rule_config in p['rules'].items():
        # build config and validate it the same way the module initialization would do

        if rule_config is None:
            rule_config = {}

        rule_config = convert_aliases(cnf=rule_config, aliases=RULE_MOD_ARG_ALIASES)

        real_cnf = {
            **RULE_DEFAULTS,
            **p['defaults'],
            **rule_config,
            **{
                p['key_field']: rule_key,
                'firewall': p['firewall'],
            },
            **overrides,
        }

        if real_cnf['debug']:
            m.warn(f"Validating rule: '{rule_key} => {real_cnf}'")

        if validate_single(
                module=m, module_args=RULE_MOD_ARGS, log_mod='rule',
                key=rule_key, cnf=real_cnf,
        ):
            valid_rules[rule_key] = real_cnf

    # manage rules
    for rule_key, rule_config in valid_rules.items():
        # process single rule like in the 'rule' module
        rule_result = dict(
            changed=False,
            diff={
                'before': {},
                'after': {},
            }
        )

        p['debug'] = rule_config['debug']  # per rule switch

        if p['debug'] or p['output_info']:
            m.warn(f"Processing rule: '{rule_key} => {rule_config}'")

        rule = Rule(
            module=m,
            result=rule_result,
            cnf=rule_config,
            session=s,
            fail=p['fail_verification'],
        )
        # save on requests
        rule.existing_rules = existing_rules

        rule.check()
        rule.process()

        if rule_result['changed']:
            r['changed'] = True
            rule_result['diff'] = diff_remove_empty(rule_result['diff'])

            if 'before' in rule_result['diff']:
                r['diff']['before'][rule_key] = rule_result['diff']['before']

            if 'after' in rule_result['diff']:
                r['diff']['after'][rule_key] = rule_result['diff']['after']

    s.close()
