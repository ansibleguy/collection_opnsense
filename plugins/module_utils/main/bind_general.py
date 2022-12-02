from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.main import \
    simplify_translate, validate_int_fields, is_ip
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.base import Base


class General:
    CMDS = {
        'set': 'set',
        'search': 'get',
    }
    API_KEY = 'general'
    API_MOD = 'bind'
    API_CONT = 'general'
    API_CONT_REL = 'service'
    API_CMD_REL = 'reconfigure'
    FIELDS_CHANGE = [
        'ipv6', 'response_policy_zones', 'port', 'listen_ipv4', 'listen_ipv6',
        'query_source_ipv4', 'query_source_ipv6', 'transfer_source_ipv4', 'transfer_source_ipv6',
        'forwarders', 'filter_aaaa_v4', 'filter_aaaa_v6', 'filter_aaaa_acl', 'log_size',
        'cache_size', 'recursion_acl', 'transfer_acl', 'dnssec_validation', 'hide_hostname',
        'hide_version', 'prefetch', 'ratelimit', 'ratelimit_count', 'ratelimit_except',
        'enabled',
    ]
    FIELDS_ALL = FIELDS_CHANGE
    FIELDS_TRANSLATE = {
        'ipv6': 'disablev6',
        'response_policy_zones': 'enablerpz',
        'listen_ipv4': 'listenv4',
        'listen_ipv6': 'listenv6',
        'query_source_ipv4': 'querysource',
        'query_source_ipv6': 'querysourcev6',
        'transfer_source_ipv4': 'transfersource',
        'transfer_source_ipv6': 'transfersourcev6',
        'filter_aaaa_v4': 'filteraaaav4',
        'filter_aaaa_v6': 'filteraaaav6',
        'filter_aaaa_acl': 'filteraaaaacl',
        'log_size': 'logsize',
        'cache_size': 'maxcachesize',
        'recursion_acl': 'recursion',
        'transfer_acl': 'allowtransfer',
        'dnssec_validation': 'dnssecvalidation',
        'hide_hostname': 'hidehostname',
        'hide_version': 'hideversion',
        'prefetch': 'disableprefetch',
        'ratelimit': 'enableratelimiting',
        'ratelimit_count': 'ratelimitcount',
        'ratelimit_except': 'ratelimitexcept',
    }
    FIELDS_BOOL_INVERT = ['ipv6', 'prefetch']
    FIELDS_TYPING = {
        'bool': [
            'ipv6', 'response_policy_zones', 'filter_aaaa_v4', 'filter_aaaa_v6', 'hide_hostname',
            'hide_version', 'prefetch', 'ratelimit', 'enabled',
        ],
        'list': ['ratelimit_except', 'filter_aaaa_acl', 'forwarders', 'listen_ipv6', 'listen_ipv4'],
        'select': ['dnssec_validation', 'recursion_acl', 'transfer_acl'],
    }
    INT_VALIDATIONS = {
        'ratelimit_count': {'min': 1, 'max': 1000},
        'cache_size': {'min': 1, 'max': 99},
        'log_size': {'min': 1, 'max': 1000},
        'port': {'min': 1, 'max': 65535},
    }
    EXIST_ATTR = 'settings'

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None):
        self.m = module
        self.p = module.params
        self.r = result
        self.s = Session(module=module) if session is None else session
        self.exists = False
        self.settings = {}
        self.call_cnf = {  # config shared by all calls
            'module': self.API_MOD,
            'controller': self.API_CONT,
        }
        self.existing_entries = None
        self.existing_acls = None
        self.acls_needed = False
        self.b = Base(instance=self)

    def check(self):
        validate_int_fields(module=self.m, data=self.p, field_minmax=self.INT_VALIDATIONS)

        for field in [
            'listen_ipv4', 'query_source_ipv4', 'transfer_source_ipv4',
            'listen_ipv6', 'query_source_ipv6', 'transfer_source_ipv6',
        ]:
            if isinstance(self.p[field], list):
                for ip in self.p[field]:
                    if not is_ip(ip, ignore_empty=True):
                        self.m.fail_json(
                            f"It seems you provided an invalid IP address as '{field}': '{ip}'"
                        )

                if len(self.p[field]) == 0:
                    self.m.fail_json(
                        f"You need to supply at least one value as '{field}'! "
                        'Leave it empty to only use localhost.'
                    )

            else:
                ip = self.p[field]
                if not is_ip(ip, ignore_empty=True):
                    self.m.fail_json(
                        f"It seems you provided an invalid IP address as '{field}': '{ip}'"
                    )

        if self.p['recursion_acl'] != '' or self.p['transfer_acl'] != '':
            # to save time on call if not needed
            self.acls_needed = True

        self.settings = self._search_call()

        if self.acls_needed:
            self._find_links()

        self.r['diff']['before'] = self.settings
        self.r['diff']['after'] = {
            k: v for k, v in self.p.items() if k in self.settings
        }

    def _search_call(self) -> dict:
        if self.acls_needed:
            self.existing_acls = self.s.get(cnf={
                **self.call_cnf, **{'command': self.CMDS['search'], 'controller': 'acl'}
            })['acl']['acls']['acl']

        return simplify_translate(
            existing=self.s.get(cnf={
                **self.call_cnf, **{'command': self.CMDS['search']}
            })[self.API_KEY],
            translate=self.FIELDS_TRANSLATE,
            typing=self.FIELDS_TYPING,
            bool_invert=self.FIELDS_BOOL_INVERT,
        )

    def _find_links(self):
        fields = ['recursion_acl', 'transfer_acl']

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

    def process(self):
        self.update()

    def get_existing(self) -> dict:
        return self._search_call()

    def update(self):
        self.b.update()

    def reload(self):
        self.b.reload()
