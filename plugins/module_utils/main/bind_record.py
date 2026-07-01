from ansible.module_utils.basic import AnsibleModule

from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.handler import \
    ModuleSoftError
from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.oxlorg.opnsense.plugins.module_utils.helper.match import \
    get_multiple_matching
from ansible_collections.oxlorg.opnsense.plugins.module_utils.helper.validate import \
    is_ip4, is_ip6, is_unset
from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.module import BaseModule
from ansible_collections.oxlorg.opnsense.plugins.module_utils.main.bind_domain import Domain


class Record(BaseModule):
    MULTI_DIFF_KEY = 'name'
    CMDS = {
        'add': 'addRecord',
        'del': 'delRecord',
        'set': 'setRecord',
        'search': 'searchRecord',
        'detail': 'getRecord',
        'toggle': 'toggleRecord',
    }
    API_KEY_PATH = 'record'
    API_MOD = 'bind'
    API_CONT = 'record'
    API_CONT_REL = 'service'
    FIELDS_CHANGE = ['value']
    FIELDS_ALL = ['domain', 'name', 'type', 'enabled']
    FIELDS_ALL.extend(FIELDS_CHANGE)
    FIELDS_TYPING = {
        'bool': ['enabled'],
        'select': ['type', 'domain'],
    }
    FIELDS_RR_MATCH = ['domain', 'name', 'type', 'value']
    EXIST_ATTR = 'record'

    def __init__(
            self, module: AnsibleModule, result: dict, multi: dict = None,
            session: Session = None, fail: dict = None,
    ):
        BaseModule.__init__(self=self, m=module, r=result, s=session, f=fail, multi=multi)
        self.existing = []
        self.record = {}
        self.existing_entries = None
        self.existing_domains = None
        self.existing_domain_mapping = None
        self.exists = False
        self.exists_rr = False

    # pylint: disable=R0915
    def check(self) -> None:
        if self.p['state'] == 'present':
            if is_unset(self.p['value']):
                self._error(
                    'You need to supply a value to create the record '
                    f"'{self.p['name']}.{self.p['domain']}'"
                )

            else:
                if self.p['type'] == 'A' and not is_ip4(self.p['value']):
                    self.m.fail_json(f"Value '{self.p['value']}' is not a valid IPv4-address!")

                elif self.p['type'] == 'AAAA' and not is_ip6(self.p['value']):
                    self.m.fail_json(f"Value '{self.p['value']}' is not a valid IPv6-address!")

        # custom matching as dns round-robin allows for multiple records to match..
        self.search_call_domains()
        if self.existing_entries is None:
            self.existing_entries = self.get_existing()

        if len(self.existing_domains) == 0:
            if self.p['state'] == 'present':
                self._error('No existing domain found! Create one before managing its records.')

        else:
            domain_found = False
            if self.existing_domain_mapping is None:
                for uuid, dom in self.existing_domains.items():
                    if dom['domainname'] == self.p['domain'] or uuid == self.p['domain']:
                        self.p['domain'] = uuid
                        domain_found = True
                        break

            else:
                if self.p['domain'] in self.existing_domain_mapping:
                    self.p['domain'] = self.existing_domain_mapping[self.p['domain']]
                    domain_found = True

            if not domain_found:
                self._error(
                    f"The provided domain '{self.p['domain']}' was not found! "
                    'You may have to create it before managing its records.'
                )

            self.existing = get_multiple_matching(
                module=self.m, existing_items=self.existing_entries,
                compare_item=self.p, match_fields=self.p['match_fields'],
                simplify_func=self.simplify_existing,
            )

            self.exists_rr = len(self.existing) > 1
            self.exists = len(self.existing) == 1

            if self.exists_rr or self.p.get('round_robin', False):
                self.r['diff']['before'] = self.existing

            else:
                if self.exists:
                    self.record = self.existing[0]
                    self.r['diff']['before'] = self.record
                    self.call_cnf['params'] = [self.record['uuid']]

        self._base_check()

    def search_call(self) -> list:
        self.search_call_domains()

        existing = []
        for uuid in self.existing_domains:
            existing.extend(self.api_search_post(
                cnf={
                    'module': self.API_MOD,
                    'controller': self.API_CONT,
                    'command': self.CMDS['search'],
                },
                data={'domain': uuid}
            ))

        return existing

    def search_call_domains(self):
        if self.existing_domains is not None:
            return

        data = self.s.get(cnf={
            'module': Domain.API_MOD,
            'controller': Domain.API_CONT,
            'command': Domain.CMDS['search'],
        })
        for k in Domain.API_KEY_PATH.split('.'):
            data = data[k]

        self.existing_domains = data

    def _error(self, msg: str, verification: bool = True) -> None:
        if (verification and self.fail_verify) or (not verification and self.fail_process):
            self.m.fail_json(msg)

        else:
            self.m.warn(msg)
            raise ModuleSoftError

    def _delete_rr(self) -> None:
        self.r['diff']['after'] = {}

        for record in self.existing:
            self.call_cnf['params'] = [record['uuid']]
            self.delete()

    def process(self) -> None:
        if self.exists_rr or self.p['round_robin']:
            # round-robin exists
            if not self.p['round_robin']:
                if self.p['state'] == 'present':
                    self._error(
                        msg='Multiple records with the provided domain/type/name combination exist! '
                            "To create 'round_robin' records - set the argument to 'true'. "
                            "Else remove all existing records by re-calling the module with 'state=absent'",
                        verification=False,
                    )

                else:
                    if self.exists_rr:
                        self._delete_rr()

                    else:
                        self.delete()

            else:
                if self.p['state'] == 'present':
                    if not self._exists_rr():
                        self._diff_rr()
                        self.create()

                else:
                    self._delete_rr()

        else:
            # single record
            self._base_process()

    def _exists_rr(self) -> bool:
        # check if exact same record already exists if using round-robin
        for e in self.existing:
            matching = []
            for f in self.FIELDS_RR_MATCH:
                matching.append(e[f] == self.p[f])

            if all(matching):
                return True

        return False

    def _diff_rr(self) -> None:
        def _key(item: dict, idx: int) -> str:
            return f"{item['type']}:{item['name']}.{item['domain']}#{idx}"

        _before = {}
        _after = {}

        _idx = 0
        for e in self.existing:
            _before[_key(item=e, idx=_idx)] = e
            _idx += 1

        _new = self.build_diff(data=self.p)
        _after[_key(item=_new, idx=_idx)] = _new

        self.r['diff']['after'] = {**_before, **_after}
        self.r['diff']['before'] = _before
