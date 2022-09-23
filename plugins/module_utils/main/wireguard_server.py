from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.main import \
    is_true, validate_int_fields, validate_str_fields, is_ip, validate_port, \
    get_selected_list, format_int
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.base import Base


class Server:
    FIELD_ID = 'name'
    CMDS = {
        'add': 'addServer',
        'del': 'delServer',
        'set': 'setServer',
        'search': 'get',
        'toggle': 'toggleserver',
    }
    API_KEY = 'server'
    API_KEY_1 = 'server'
    API_KEY_2 = 'servers'
    API_MOD = 'wireguard'
    API_CONT = 'server'
    API_CONT_REL = 'service'
    API_CMD_REL = 'reconfigure'
    FIELDS_CHANGE = [
        'public_key', 'private_key', 'port', 'mtu', 'dns_servers', 'tunnel_ips',
        'disable_routes', 'gateway', 'peers',
    ]
    FIELDS_ALL = [FIELD_ID, 'enabled']
    FIELDS_ALL.extend(FIELDS_CHANGE)
    FIELDS_TRANSLATE = {
        'dns_servers': 'dns',
        'public_key': 'pubkey',
        'private_key': 'privkey',
        'tunnel_ips': 'tunneladdress',
        'disable_routes': 'disableroutes',
    }
    FIELDS_DIFF_EXCLUDE = ['private_key']
    INT_VALIDATIONS = {
        'mtu': {'min': 1, 'max': 9300},
    }
    STR_VALIDATIONS = {
        'name': r'^([0-9a-zA-Z._\-]){1,64}$'
    }
    STR_LEN_VALIDATIONS = {
        'name': {'min': 1, 'max': 64}
    }
    EXIST_ATTR = 'server'

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None):
        self.m = module
        self.p = module.params
        self.r = result
        self.s = Session(module=module) if session is None else session
        self.exists = False
        self.server = {}
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

        for tun_ip in self.p['tunnel_ips']:
            if not is_ip(tun_ip):
                self.m.fail_json(f"Tunnel address '{tun_ip}' is not a valid IP-address!")

        for dns in self.p['dns_servers']:
            if not is_ip(dns):
                self.m.fail_json(f"DNS-value '{dns}' is not a valid IP-address!")

        self.b.find(match_fields=[self.FIELD_ID])
        if self.exists:
            self.call_cnf['params'] = [self.server['uuid']]
            if self.p['public_key'] is None or self.p['private_key'] is None:
                self.p['public_key'] = self.server['public_key']
                self.p['private_key'] = self.server['private_key']

        if self.p['state'] == 'present':
            self.r['diff']['after'] = self.b.build_diff(data=self.p)

    @staticmethod
    def _simplify_existing(server: dict) -> dict:
        # makes processing easier
        return {
            'enabled': is_true(server['enabled']),
            'uuid': server['uuid'],
            'name': server['name'],
            'instance': format_int(server['instance']),
            'public_key': server['pubkey'],
            'private_key': server['privkey'],
            'port': format_int(server['port']),
            'mtu': format_int(server['mtu']),
            'dns_servers': server['dns'],
            'tunnel_ips': get_selected_list(data=server['tunneladdress'], remove_empty=True),
            'disable_routes': is_true(server['disableroutes']),
            'gateway': server['gateway'],
            'peers': server['peers'],
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
