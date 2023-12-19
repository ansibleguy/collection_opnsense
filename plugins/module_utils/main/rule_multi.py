from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.handler import \
    ModuleSoftError
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.multi import \
    validate_single, convert_aliases
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.defaults.rule import \
    RULE_MOD_ARGS, RULE_DEFAULTS, RULE_MOD_ARG_ALIASES
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.main import diff_remove_empty
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.api import Session
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.main.rule import Rule


# pylint: disable=R0915
def process(m: AnsibleModule, p: dict, r: dict) -> None:
    s = Session(module=m)
    meta_rule = Rule(module=m, session=s, result={})
    existing_rules = meta_rule.get_existing()

    if isinstance(p['key_field'], list):
        # edge case
        p['key_field'] = p['key_field'][0]

    defaults = {}
    overrides = {
        **p['override'],
        'reload': False,
        'match_fields': p['match_fields'],
        'debug': p['debug'],
        'firewall': p['firewall'],
    }

    if p['state'] is not None:
        defaults['state'] = p['state']

    if p['enabled'] is not None:
        defaults['enabled'] = p['enabled']

    # build list of valid rules or fail if invalid config is not permitted
    valid_rules = {}
    for rule_key, rule_config in p['rules'].items():
        # build config and validate it the same way the module initialization would do

        if rule_config is None:
            rule_config = {}

        rule_config = convert_aliases(cnf=rule_config, aliases=RULE_MOD_ARG_ALIASES)

        real_cnf = {
            **RULE_DEFAULTS,
            **defaults,
            **p['defaults'],
            **rule_config,
            p['key_field']: rule_key,
            **overrides,
        }

        if real_cnf['debug']:
            m.warn(f"Validating rule: '{rule_key} => {real_cnf}'")

        if validate_single(
                module=m, module_args=RULE_MOD_ARGS, log_mod='rule',
                key=rule_key, cnf=real_cnf,
        ):
            # NOTE: parameter type-casting not done automatically
            if 'interface' in real_cnf and isinstance(real_cnf['interface'], str):
                real_cnf['interface'] = [real_cnf['interface']]

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

        try:
            rule = Rule(
                module=m,
                result=rule_result,
                cnf=rule_config,
                session=s,
                fail_verify=p['fail_verification'],
                fail_proc=p['fail_processing'],
            )
            # save on requests
            rule.existing_entries = existing_rules

            rule.check()
            rule.process()

            if rule_result['changed']:
                r['changed'] = True
                rule_result['diff'] = diff_remove_empty(rule_result['diff'])

                if 'before' in rule_result['diff']:
                    r['diff']['before'][rule_key] = rule_result['diff']['before']

                if 'after' in rule_result['diff']:
                    r['diff']['after'][rule_key] = rule_result['diff']['after']

        except ModuleSoftError:
            continue

    meta_rule.reload()
    s.close()
