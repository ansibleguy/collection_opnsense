from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.main import \
    validate_int_fields, is_ip, get_selected, is_unset
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.cls import BaseModule


class Domain(BaseModule):
    FIELD_ID = 'name'
    CMDS = {
        'add': 'addPrimaryDomain',
        'del': 'delDomain',
        'set': 'setDomain',
        'search': 'get',
        'toggle': 'toggleDomain',
    }
    API_KEY_PATH = 'domain.domains.domain'
    API_MOD = 'bind'
    API_CONT = 'domain'
    API_CONT_REL = 'service'
    API_CMD_REL = 'reconfigure'
    FIELDS_CHANGE = [
        'mode', 'primary', 'transfer_key_algo', 'transfer_key_name', 'transfer_key',
        'allow_notify', 'transfer_acl', 'query_acl', 'ttl', 'refresh', 'retry',
        'expire', 'negative', 'admin_mail', 'server',
        # 'serial',
    ]
    FIELDS_ALL = ['enabled', FIELD_ID]
    FIELDS_ALL.extend(FIELDS_CHANGE)
    FIELDS_TRANSLATE = {
        'name': 'domainname',
        'mode': 'type',
        'primary': 'primaryip',
        'transfer_key_algo': 'transferkeyalgo',
        'transfer_key_name': 'transferkeyname',
        'transfer_key': 'transferkey',
        'allow_notify': 'allownotifysecondary',
        'transfer_acl': 'allowtransfer',
        'query_acl': 'allowquery',
        'admin_mail': 'mailadmin',
        'server': 'dnsserver',
    }
    FIELDS_TYPING = {
        'bool': ['enabled'],
        'list': ['primary', 'allow_notify', 'transfer_acl', 'query_acl'],
        'select': ['mode', 'transfer_key_algo'],
    }
    INT_VALIDATIONS = {
        'ttl': {'min': 60, 'max': 86400},
        'refresh': {'min': 60, 'max': 86400},
        'retry': {'min': 60, 'max': 86400},
        'expire': {'min': 60, 'max': 10000000},
        'negative': {'min': 60, 'max': 86400},
    }
    EXIST_ATTR = 'domain'
    # FIELDS_DIFF_EXCLUDE = ['serial']

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None):
        BaseModule.__init__(self=self, m=module, r=result, s=session)
        self.domain = {}
        self.existing_acls = None
        self.existing_records = None
        self.acls_needed = False

    def check(self) -> None:
        if self.p['state'] == 'present':
            validate_int_fields(module=self.m, data=self.p, field_minmax=self.INT_VALIDATIONS)

            for field in ['allow_notify', 'primary']:
                for ip in self.p[field]:
                    if not is_ip(ip, ignore_empty=True):
                        self.m.fail_json(
                            f"It seems you provided an invalid IP address as '{field}': '{is_ip}'"
                        )

            if self.p['mode'] != 'primary':
                self.CMDS['add'] = 'addSecondaryDomain'

            if not is_unset(self.p['query_acl']) or not is_unset(self.p['transfer_acl']):
                self.acls_needed = True
                self._search_acls()

        self.b.find(match_fields=[self.FIELD_ID])

        if self.exists:
            if self.p['state'] != 'present':
                # checking if domain has any record left before removing it; plugin seems to lack validation
                self._search_records()

                if self.existing_records is not None and len(self.existing_records) > 0:
                    for record in self.existing_records.values():
                        if get_selected(record['domain']) == self.domain['uuid']:
                            self.m.fail_json(
                                f"Unable to remove domain '{self.domain['name']}' - it has at least "
                                f"one existing record: '{get_selected(record['type'])}: "
                                f"{record['name']}.{self.domain['name']}'"
                            )

        if self.p['state'] == 'present':
            if self.acls_needed:
                self.b.find_multiple_links(
                    field='query_acl',
                    existing=self.existing_acls,
                )
                self.b.find_multiple_links(
                    field='transfer_acl',
                    existing=self.existing_acls,
                )

            self.r['diff']['after'] = self.b.build_diff(data=self.p)

    def _search_acls(self) -> None:
        self.existing_acls = self.s.get(cnf={
            **self.call_cnf, **{'command': self.CMDS['search'], 'controller': 'acl'}
        })['acl']['acls']['acl']

    def _search_records(self) -> None:
        # to check if domain is still in use
        self.existing_records = self.s.get(cnf={
            **self.call_cnf, **{'command': self.CMDS['search'], 'controller': 'record'}
        })['record']['records']['record']
