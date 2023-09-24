from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.handler import \
    ModuleSoftError
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.multi import \
    validate_single, convert_aliases
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.defaults.bind_record import \
    RECORD_MOD_ARGS, RECORD_DEFAULTS, RECORD_MOD_ARG_ALIASES
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.main import diff_remove_empty
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.api import Session
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.main.bind_record import Record

# pylint: disable=R0912,R0914,R0915


def process(m: AnsibleModule, p: dict, r: dict) -> None:
    s = Session(module=m)
    meta_record = Record(module=m, session=s, result={})
    existing_records = meta_record.get_existing()
    existing_domains = meta_record.search_call_domains()
    existing_domain_mapping = {}

    if len(existing_domains) > 0:
        for uuid, dom in existing_domains.items():
            existing_domain_mapping[dom['domainname']] = uuid

    defaults = {'round_robin': False}
    overrides = {
        'reload': False,
        'match_fields': p['match_fields'],
        'debug': p['debug'],
        'firewall': p['firewall'],
    }

    if p['state'] is not None:
        defaults['state'] = p['state']

    if p['enabled'] is not None:
        defaults['enabled'] = p['enabled']

    # build list of valid records or fail if invalid config is not permitted
    valid_records = {}
    for domain, records in p['records'].items():
        overrides['domain'] = domain

        if domain not in existing_domain_mapping:
            msg = f"The domain '{domain}' does not seem to exist! " \
                  "Create one before managing its records."
            if p['fail_processing']:
                m.fail_json(msg)

            else:
                m.warn(msg)

            continue

        for idx, record in enumerate(records):
            # build config and validate it the same way the module initialization would do
            if isinstance(record, str):
                # allowing only name to be supplied for state-changes
                record = {'name': record}

            record = convert_aliases(cnf=record, aliases=RECORD_MOD_ARG_ALIASES)

            real_cnf = {
                **RECORD_DEFAULTS,
                **defaults,
                **record,
                **overrides,
            }

            try:
                appendix = f'#{idx}' if real_cnf['round_robin'] else ''
                record_key = f"{real_cnf['type']}:{record['name']}.{domain}{appendix}"

            except KeyError:
                # placeholder => will fail verification anyway
                record_key = f"{real_cnf['type']}:NONE.{domain}"

            if real_cnf['debug']:
                m.warn(f"Validating record: '{record_key} => {real_cnf}'")

            if validate_single(
                    module=m, module_args=RECORD_MOD_ARGS, log_mod='bind_record',
                    key=record_key, cnf=real_cnf,
            ):
                valid_records[record_key] = real_cnf

    # manage records
    for record_key, record_config in valid_records.items():
        # process single record like in the 'record' module
        record_result = dict(
            changed=False,
            diff={
                'before': {},
                'after': {},
            }
        )

        p['debug'] = record_config['debug']  # per record switch

        if p['debug'] or p['output_info']:
            m.warn(f"Processing record: '{record_key} => {record_config}'")

        try:
            record = Record(
                module=m,
                result=record_result,
                cnf=record_config,
                session=s,
                fail_verify=p['fail_verification'],
                fail_proc=p['fail_processing'],
            )
            # save on requests
            record.existing_entries = existing_records
            record.existing_domains = existing_domains
            record.existing_domain_mapping = existing_domain_mapping

            record.check()
            record.process()

            if record_result['changed']:
                r['changed'] = True
                record_result['diff'] = diff_remove_empty(record_result['diff'])

                if 'before' in record_result['diff']:
                    r['diff']['before'][record_key] = record_result['diff']['before']

                if 'after' in record_result['diff']:
                    r['diff']['after'][record_key] = record_result['diff']['after']

        except ModuleSoftError:
            continue

    meta_record.reload()
    s.close()
