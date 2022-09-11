from ipaddress import IPv6Address, IPv4Address, AddressValueError, NetmaskValueError
import validators

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.api import \
    Session
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper import \
    is_ip, get_matching, validate_port, get_selected, get_selected_list, is_true, to_digit


class Syslog:
    CMDS = {
        'add': 'addDestination',
        'del': 'delDestination',
        'set': 'setDestination',
        'search': 'get',
    }
    API_KEY = 'destination'
    API_MOD = 'syslog'
    API_CONT = 'settings'
    API_CONT_REL = 'service'
    API_CMD_REL = 'reconfigure'
    CHANGE_CHECK_FIELDS = [
        'target', 'transport', 'facility', 'program', 'level', 'certificate',
        'port', 'description', 'enabled',
    ]

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None):
        self.m = module
        self.p = module.params
        self.r = result
        self.s = Session(module=module) if session is None else session
        self.exists = False
        self.dest = {}
        self.call_cnf = {  # config shared by all calls
            'module': self.API_MOD,
            'controller': self.API_CONT,
        }
        self.existing_dests = None

    def process(self):
        if self.p['state'] == 'absent':
            if self.exists:
                self.delete()

        else:
            if self.exists:
                self.update()

            else:
                self.create()

    def check(self):
        if not is_ip(self.p['target']) and \
                not validators.domain(self.p['target']):
            self.m.fail_json(
                f"Value of target '{self.p['target']}' is neither "
                f"a valid IP-Address nor a valid domain-name!"
            )

        if self.p['transport'].startswith('tls') and self.p['certificate'] == '':
            self.m.fail_json(
                "You need to provide a certificate to use encrypted transport!"
            )

        if is_ip(self.p['target']):
            if self.p['transport'].find('6') != -1:
                try:
                    IPv6Address(self.p['target'])

                except (AddressValueError, NetmaskValueError):
                    self.m.fail_json(
                        "Target does not match transport ip-protocol (IPv6)!"
                    )

            else:
                try:
                    IPv4Address(self.p['target'])

                except (AddressValueError, NetmaskValueError):
                    self.m.fail_json(
                        "Target does not match transport ip-protocol (IPv4)!"
                    )

        validate_port(module=self.m, port=self.p['port'])

        # checking if item exists
        self._find_dest()
        if self.exists:
            self.call_cnf['params'] = [self.dest['uuid']]

        self.r['diff']['after'] = self._build_diff_after()

    def _find_dest(self):
        if self.existing_dests is None:
            self.existing_dests = self._search_call()

        match = get_matching(
            module=self.m, existing_items=self.existing_dests,
            compare_item=self.p, match_fields=self.p['match_fields'],
            simplify_func=self._simplify_existing,
        )

        if match is not None:
            self.dest = match
            self.r['diff']['before'] = self.dest
            self.exists = True

    def _error(self, msg: str):
        # for special handling of errors
        self.m.fail_json(msg)

    def get_existing(self) -> list:
        existing_entries = self._search_call()
        simple_entries = []

        if len(existing_entries) > 0:
            for uuid, entry in existing_entries.items():
                entry['uuid'] = uuid
                simple_entries.append(self._simplify_existing(dest=entry))

        return simple_entries

    def _search_call(self) -> dict:
        return self.s.get(cnf={
            **self.call_cnf, **{'command': self.CMDS['search']}
        })['syslog']['destinations']['destination']

    def detail_call(self) -> dict:
        return self.s.get(cnf={
            **self.call_cnf, **{'command': self.CMDS['detail']}
        })['dest']

    def create(self):
        self.r['changed'] = True

        if not self.m.check_mode:
            self.s.post(cnf={
                **self.call_cnf, **{
                    'command': self.CMDS['add'],
                    'data': self._build_request(),
                }
            })

    def update(self):
        # checking if changed
        for field in self.CHANGE_CHECK_FIELDS:
            if str(self.dest[field]) != str(self.p[field]):
                self.r['changed'] = True
                break

        # update if changed
        if self.r['changed']:
            if self.p['debug']:
                self.m.warn(f"{self.r['diff']}")

            if not self.m.check_mode:
                self.s.post(cnf={
                    **self.call_cnf, **{
                        'command': self.CMDS['set'],
                        'data': self._build_request(),
                    }
                })

    @staticmethod
    def _simplify_existing(dest: dict) -> dict:
        # makes processing easier
        return {
            'enabled': is_true(dest['enabled']),
            'rfc5424': is_true(dest['rfc5424']),
            'target': dest['hostname'],
            'description': dest['description'],
            'port': int(dest['port']),
            'uuid': dest['uuid'],
            'certificate': get_selected(data=dest['certificate']),
            'transport': get_selected(data=dest['transport']),
            'program': get_selected_list(data=dest['program']),
            'level': get_selected_list(data=dest['level']),
            'facility': get_selected_list(data=dest['facility']),
        }

    def _build_diff_after(self) -> dict:
        return {
            'uuid': self.dest['uuid'] if 'uuid' in self.dest else None,
            'rfc5424': self.p['rfc5424'],
            'enabled': self.p['enabled'],
            'target': self.p['target'],
            'transport': self.p['transport'],
            'description': self.p['description'],
            'program': self.p['program'],
            'level': self.p['level'],
            'facility': self.p['facility'],
            'certificate': self.p['certificate'],
            'port': self.p['port'],
        }

    def _build_request(self) -> dict:
        return {
            self.API_KEY: {
                'rfc5424': to_digit(self.p['rfc5424']),
                'enabled': to_digit(self.p['enabled']),
                'transport': self.p['transport'],
                'description': self.p['description'],
                'program': ','.join(self.p['program']),
                'level': ','.join(self.p['level']),
                'facility': ','.join(self.p['facility']),
                'hostname': self.p['target'],
                'certificate': self.p['certificate'],
                'port': self.p['port'],
            }
        }

    def delete(self):
        self.r['changed'] = True
        self.r['diff']['after'] = {}

        if not self.m.check_mode:
            self._delete_call()

            if self.p['debug']:
                self.m.warn(f"{self.r['diff']}")

    def _delete_call(self) -> dict:
        return self.s.post(cnf={**self.call_cnf, **{'command': self.CMDS['del']}})

    def enable(self):
        if self.exists and not self.dest['enabled']:
            self.r['changed'] = True
            self.r['diff']['before'] = {'enabled': False}
            self.r['diff']['after'] = {'enabled': True}

            if not self.m.check_mode:
                self._change_enabled_state(1)

    def disable(self):
        if self.exists and self.dest['enabled']:
            self.r['changed'] = True
            self.r['diff']['before'] = {'enabled': True}
            self.r['diff']['after'] = {'enabled': False}

            if not self.m.check_mode:
                self._change_enabled_state(0)

    def _change_enabled_state(self, value: int):
        self.s.post(cnf={
            **self.call_cnf, **{
                'command': self.CMDS['toggle'],
                'params': [self.dest['uuid'], value],
            }
        })

    def reload(self):
        # reload the running config
        if not self.m.check_mode:
            self.s.post(cnf={
                'module': self.call_cnf['module'],
                'controller': self.API_CONT_REL,
                'command': self.API_CMD_REL,
                'params': []
            })
