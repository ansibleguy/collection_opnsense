from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.unbound import \
    validate_domain, reload
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.base import Base
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.main import \
    get_matching, validate_port, is_true, get_simple_existing


class Forward:
    CMDS = {
        'add': 'addDot',
        'del': 'delDot',
        'set': 'setDot',
        'search': 'get',
    }
    API_KEY = 'dot'
    API_MOD = 'unbound'
    API_CONT = 'settings'
    API_CONT_REL = 'service'
    API_CMD_REL = 'reconfigure'
    FIELDS_CHANGE = ['domain', 'target', 'enabled', 'port']
    FIELDS_ALL = ['type']
    FIELDS_ALL.extend(FIELDS_CHANGE)
    FIELDS_TRANSLATE = {
        'target': 'server',
    }
    EXIST_ATTR = 'fwd'

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None):
        self.m = module
        self.p = module.params
        self.r = result
        self.s = Session(module=module) if session is None else session
        self.exists = False
        self.fwd = {}
        self.call_cnf = {  # config shared by all calls
            'module': self.API_MOD,
            'controller': self.API_CONT,
        }
        self.call_headers = {
            'Referer': f"https://{self.p['firewall']}:{self.p['api_port']}/ui/unbound/forward",
        }
        # else the type will always be 'dns-over-tls':
        #   https://github.com/opnsense/core/commit/6832fd75a0b41e376e80f287f8ad3cfe599ea3d1
        self.existing_fwds = None
        self.b = Base(instance=self)

    def check(self):
        validate_domain(module=self.m, domain=self.p['domain'])
        validate_port(module=self.m, port=self.p['port'])

        # checking if item exists
        self._find_fwd()
        self.r['diff']['after'] = self.b.build_diff(data=self.p)

    def _find_fwd(self):
        if self.existing_fwds is None:
            self.existing_fwds = self._search_call()

        match = get_matching(
            module=self.m, existing_items=self.existing_fwds,
            compare_item=self.p, match_fields=['domain', 'target'],
            simplify_func=self._simplify_existing,
        )

        if match is not None:
            self.fwd = match
            self.exists = True
            self.r['diff']['before'] = self.b.build_diff(data=self.fwd)
            self.call_cnf['params'] = [self.fwd['uuid']]

    def get_existing(self) -> list:
        return get_simple_existing(
            entries=self._search_call(),
            simplify_func=self._simplify_existing
        )

    def _search_call(self) -> list:
        fwds = []
        raw = self.s.get(cnf={
            **self.call_cnf, **{'command': self.CMDS['search']}
        })['unbound']['dots'][self.API_KEY]

        if len(raw) > 0:
            for uuid, dot in raw.items():
                if is_true(dot['type']['forward']['selected']):
                    dot.pop('type')
                    dot['uuid'] = uuid
                    fwds.append(dot)

        return fwds

    def create(self):
        self.r['changed'] = True

        if not self.m.check_mode:
            self.s.post(
                cnf={
                    **self.call_cnf, **{
                        'command': self.CMDS['add'],
                        'data': self.b.build_request(),
                    }
                },
                headers=self.call_headers,
            )

    def update(self):
        # checking if changed
        for field in self.FIELDS_CHANGE:
            if self.fwd[field] != self.p[field]:
                self.r['changed'] = True
                break

        # update if changed
        if self.r['changed']:
            if self.p['debug']:
                self.m.warn(f"{self.r['diff']}")

            if not self.m.check_mode:
                self.s.post(
                    cnf={
                        **self.call_cnf, **{
                            'command': self.CMDS['set'],
                            'data': self.b.build_request(),
                        }
                    },
                    headers=self.call_headers,
                )

    @staticmethod
    def _simplify_existing(fwd: dict) -> dict:
        # makes processing easier
        return {
            'uuid': fwd['uuid'],
            'domain': fwd['domain'],
            'target': fwd['server'],
            'port': int(fwd['port']),
            'enabled': is_true(fwd['enabled']),
        }

    def _delete_call(self) -> dict:
        return self.s.post(
            cnf={**self.call_cnf, **{'command': self.CMDS['del']}},
            headers=self.call_headers,
        )

    def process(self):
        self.b.process()

    def delete(self):
        self.b.delete()

    def reload(self):
        self.b.reload()
