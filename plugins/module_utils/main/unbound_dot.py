from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.main import \
    is_ip, valid_hostname, get_matching, validate_port, is_true
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.base import Base
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.unbound import \
    validate_domain


class DnsOverTls:
    CMDS = {
        'add': 'addForward',
        'del': 'delForward',
        'set': 'setForward',
        'search': 'get',
    }
    API_KEY = 'dot'
    API_MOD = 'unbound'
    API_CONT = 'settings'
    API_CONT_REL = 'service'
    API_CMD_REL = 'reconfigure'
    FIELDS_CHANGE = ['domain', 'target', 'enabled', 'port', 'verify']
    FIELDS_ALL = ['type']
    FIELDS_ALL.extend(FIELDS_CHANGE)
    FIELDS_TRANSLATE = {
        'target': 'server',
    }
    EXIST_ATTR = 'dot'

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None):
        self.m = module
        self.p = module.params
        self.r = result
        self.s = Session(module=module) if session is None else session
        self.exists = False
        self.dot = {}
        self.call_cnf = {  # config shared by all calls
            'module': self.API_MOD,
            'controller': self.API_CONT,
        }
        self.existing_dots = None
        self.b = Base(instance=self)

    def check(self):
        validate_domain(module=self.m, domain=self.p['domain'])
        validate_port(module=self.m, port=self.p['port'])

        if self.p['verify'] not in ['', None] and \
                not is_ip(self.p['verify']) and \
                not valid_hostname(self.p['verify']):
            self.m.fail_json(
                f"Verify-value '{self.p['verify']}' is neither a valid IP-Address "
                f"nor a valid hostname!"
            )

        # checking if item exists
        self._find_dot()
        self.r['diff']['after'] = self.b.build_diff(data=self.p)

    def _find_dot(self):
        if self.existing_dots is None:
            self.existing_dots = self._search_call()

        match = get_matching(
            module=self.m, existing_items=self.existing_dots,
            compare_item=self.p, match_fields=['domain', 'target'],
            simplify_func=self._simplify_existing,
        )

        if match is not None:
            self.dot = match
            self.exists = True
            self.r['diff']['before'] = self.b.build_diff(data=self.dot)
            self.call_cnf['params'] = [self.dot['uuid']]

    def _search_call(self) -> list:
        dots = []
        raw = self.s.get(cnf={
            **self.call_cnf, **{'command': self.CMDS['search']}
        })['unbound']['dots'][self.API_KEY]

        if len(raw) > 0:
            for uuid, dot in raw.items():
                if is_true(dot['type']['dot']['selected']):
                    dot.pop('type')
                    dot['uuid'] = uuid
                    dots.append(dot)

        return dots

    @staticmethod
    def _simplify_existing(dot: dict) -> dict:
        # makes processing easier
        return {
            'uuid': dot['uuid'],
            'domain': dot['domain'],
            'target': dot['server'],
            'port': int(dot['port']),
            'verify': dot['verify'],
            'enabled': is_true(dot['enabled']),
        }

    def get_existing(self) -> list:
        return self.b.get_existing()

    def create(self):
        self.b.create()

    def update(self):
        self.b.update()

    def process(self):
        self.b.process()

    def delete(self):
        self.b.delete()

    def reload(self):
        self.b.reload()
