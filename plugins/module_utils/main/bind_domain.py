from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.main import \
    validate_int_fields, is_ip, get_selected
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.cls import BaseModule


class Domain(BaseModule):
    FIELD_ID = 'name'
    CMDS = {
        'add': 'addMasterDomain',
        'del': 'delDomain',
        'set': 'setDomain',
        'search': 'get',
        'toggle': 'toggleDomain',
    }
    API_KEY = 'domain'
    API_KEY_1 = 'domain'
    API_KEY_2 = 'domains'
    API_MOD = 'bind'
    API_CONT = 'domain'
    API_CONT_REL = 'service'
    API_CMD_REL = 'reconfigure'
    FIELDS_CHANGE = [
        'mode', 'master', 'transfer_key_algo', 'transfer_key_name', 'transfer_key',
        'allow_notify', 'transfer_acl', 'query_acl', 'ttl', 'refresh', 'retry',
        'expire', 'negative', 'admin_mail', 'server',
    ]
    FIELDS_ALL = ['enabled', FIELD_ID]
    FIELDS_ALL.extend(FIELDS_CHANGE)
    FIELDS_TRANSLATE = {
        'name': 'domainname',
        'mode': 'type',
        'master': 'masterip',
        'transfer_key_algo': 'transferkeyalgo',
        'transfer_key_name': 'transferkeyname',
        'transfer_key': 'transferkey',
        'allow_notify': 'allownotifyslave',
        'transfer_acl': 'allowtransfer',
        'query_acl': 'allowquery',
        'admin_mail': 'mailadmin',
        'server': 'dnsserver',
    }
    FIELDS_TYPING = {
        'bool': ['enabled'],
        'list': ['master', 'allow_notify'],
        'select': [
            'mode', 'transfer_acl', 'query_acl', 'transfer_key_algo'
        ],
    }
    INT_VALIDATIONS = {
        'ttl': {'min': 60, 'max': 86400},
        'refresh': {'min': 60, 'max': 86400},
        'retry': {'min': 60, 'max': 86400},
        'expire': {'min': 60, 'max': 10000000},
        'negative': {'min': 60, 'max': 86400},
    }
    EXIST_ATTR = 'domain'

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None):
        BaseModule.__init__(self=self, m=module, r=result, s=session)
        self.domain = {}
        self.existing_acls = None
        self.existing_records = None
        self.acls_needed = False

    def check(self):
        if self.p['state'] == 'present':
            validate_int_fields(module=self.m, data=self.p, field_minmax=self.INT_VALIDATIONS)

            for field in ['allow_notify', 'master']:
                for ip in self.p[field]:
                    if not is_ip(ip, ignore_empty=True):
                        self.m.fail_json(
                            f"It seems you provided an invalid IP address as '{field}': '{is_ip}'"
                        )

            if self.p['mode'] != 'master':
                self.CMDS['add'] = 'addSlaveDomain'

            if self.p['query_acl'] != '' or self.p['transfer_acl'] != '':
                self.acls_needed = True
                self._search_acls()

        self.b.find(match_fields=[self.FIELD_ID])

        if self.exists:
            self.call_cnf['params'] = [self.domain['uuid']]

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

        if self.acls_needed:
            self._find_links()

        if self.p['state'] == 'present':
            self.r['diff']['after'] = self.b.build_diff(data=self.p)

    def _find_links(self):
        fields = ['transfer_acl', 'query_acl']

        for field in fields:
            if self.p[field] != '':
                found = False
                if len(self.existing_acls) > 0:
                    for uuid, acl in self.existing_acls.items():
                        if acl['name'] == self.p[field]:
                            self.p[field] = uuid
                            found = True

                if not found:
                    self.m.fail_json(
                        f"Provided {field} '{self.p[field]}' was not found!"
                    )

    def _search_acls(self):
        self.existing_acls = self.s.get(cnf={
            **self.call_cnf, **{'command': self.CMDS['search'], 'controller': 'acl'}
        })['acl']['acls']['acl']

    def _search_records(self):
        # to check if domain is still in use
        self.existing_records = self.s.get(cnf={
            **self.call_cnf, **{'command': self.CMDS['search'], 'controller': 'record'}
        })['record']['records']['record']
