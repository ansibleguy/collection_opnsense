import validators

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.main import \
    is_true, validate_int_fields, validate_str_fields, is_ip, validate_port, \
    get_selected_list, format_int
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.base import Base


class Peer:
    FIELD_ID = 'name'
    CMDS = {
        'add': 'addClient',
        'del': 'delClient',
        'set': 'setClient',
        'search': 'get',
        'toggle': 'toggleClient',
    }
    API_KEY = 'client'
    API_KEY_1 = 'client'
    API_KEY_2 = 'clients'
    API_MOD = 'wireguard'
    API_CONT = 'client'
    API_CONT_REL = 'service'
    API_CMD_REL = 'reconfigure'
    FIELDS_CHANGE = [
        'public_key', 'psk', 'port', 'tunnel_ips', 'target', 'keepalive',
    ]
    FIELDS_ALL = [FIELD_ID, 'enabled']
    FIELDS_ALL.extend(FIELDS_CHANGE)
    FIELDS_TRANSLATE = {
        'public_key': 'pubkey',
        'tunnel_ips': 'tunneladdress',
        'target': 'serveraddress',
        'port': 'serverport',
    }
    FIELDS_DIFF_EXCLUDE = ['psk']
    INT_VALIDATIONS = {
        'keepalive': {'min': 1, 'max': 86400},
    }
    STR_VALIDATIONS = {
        'name': r'^([0-9a-zA-Z._\-]){1,64}$'
    }
    STR_LEN_VALIDATIONS = {
        'name': {'min': 1, 'max': 64}
    }
    EXIST_ATTR = 'peer'

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None):
        self.m = module
        self.p = module.params
        self.r = result
        self.s = Session(module=module) if session is None else session
        self.exists = False
        self.peer = {}
        self.call_cnf = {  # config shared by all calls
            'module': self.API_MOD,
            'controller': self.API_CONT,
        }
        self.existing_entries = None
        self.existing_peers = None
        self.b = Base(instance=self)

    def check(self):
        validate_port(module=self.m, port=self.p['port'])
        validate_int_fields(module=self.m, data=self.p, field_minmax=self.INT_VALIDATIONS)
        validate_str_fields(
            module=self.m, data=self.p,
            field_regex=self.STR_VALIDATIONS,
            field_minmax_length=self.STR_LEN_VALIDATIONS
        )

        if self.p['state'] == 'present':
            if self.p['public_key'] is None:
                self.m.fail_json(
                    "You need to provide a 'public_key' if you want to create a peer!"
                )

            if len(self.p['tunnel_ips']) == 0:
                self.m.fail_json(
                    "You need to provide at least one 'tunnel_ip' of the peer to create!"
                )

        for tun_ip in self.p['tunnel_ips']:
            if not is_ip(tun_ip):
                self.m.fail_json(f"Tunnel address '{tun_ip}' is not a valid IP-address!")

        if self.p['target'] != '' and \
                not is_ip(self.p['target']) and not validators.domain(self.p['target']):
            self.m.fail_json(
                f"Peer target '{self.p['target']}' is neither a valid IP-address "
                f"nor a valid domain!"
            )

        self.b.find(match_fields=[self.FIELD_ID])
        if self.exists:
            self.call_cnf['params'] = [self.peer['uuid']]

        if self.p['state'] == 'present':
            self.r['diff']['after'] = self.b.build_diff(data=self.p)

    @staticmethod
    def _simplify_existing(peer: dict) -> dict:
        # makes processing easier
        return {
            'enabled': is_true(peer['enabled']),
            'uuid': peer['uuid'],
            'name': peer['name'],
            'public_key': peer['pubkey'],
            'psk': peer['psk'],
            'tunnel_ips': get_selected_list(peer['tunneladdress'], remove_empty=True),
            'target': peer['serveraddress'],
            'port': format_int(peer['serverport']),
            'keepalive': format_int(peer['keepalive']),
        }

    def process(self):
        self.b.process()

    def _search_call(self) -> list:
        return self.b.search()

    def get_existing(self) -> list:
        return self.b.get_existing()

    def create(self):
        self.b.create()

    def update(self):
        self.b.update(enable_switch=True)

    def delete(self):
        self.b.delete()

    def enable(self):
        self.b.enable()

    def disable(self):
        self.b.disable()

    def reload(self):
        self.b.reload()
