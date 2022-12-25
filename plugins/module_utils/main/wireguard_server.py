from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.main import \
    validate_int_fields, validate_str_fields, is_ip, validate_port, is_ip_or_network
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.main.wireguard_peer import Peer
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.cls import BaseModule


class Server(BaseModule):
    FIELD_ID = 'name'
    CMDS = {
        'add': 'addServer',
        'del': 'delServer',
        'set': 'setServer',
        'search': 'get',
        'toggle': 'toggleserver',
    }
    API_KEY_PATH = 'server.servers.server'
    API_MOD = 'wireguard'
    API_CONT = 'server'
    API_CONT_REL = 'service'
    API_CMD_REL = 'reconfigure'
    FIELDS_CHANGE = [
        'public_key', 'private_key', 'port', 'mtu', 'dns_servers', 'allowed_ips',
        'disable_routes', 'gateway', 'peers',
    ]
    FIELDS_ALL = [FIELD_ID, 'enabled']
    FIELDS_ALL.extend(FIELDS_CHANGE)
    FIELDS_TRANSLATE = {
        'dns_servers': 'dns',
        'public_key': 'pubkey',
        'private_key': 'privkey',
        'allowed_ips': 'tunneladdress',
        'disable_routes': 'disableroutes',
    }
    FIELDS_TYPING = {
        'bool': ['enabled', 'disable_routes'],
        'list': ['dns_servers', 'allowed_ips', 'peers'],
        'int': ['port', 'mtu', 'instance'],
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
        BaseModule.__init__(self=self, m=module, r=result, s=session)
        self.server = {}
        self.existing_peers = None

    def check(self):
        validate_port(module=self.m, port=self.p['port'])
        validate_int_fields(module=self.m, data=self.p, field_minmax=self.INT_VALIDATIONS)
        validate_str_fields(
            module=self.m, data=self.p,
            field_regex=self.STR_VALIDATIONS,
            field_minmax_length=self.STR_LEN_VALIDATIONS
        )

        if self.p['state'] == 'present':
            if len(self.p['allowed_ips']) == 0:
                self.m.fail_json(
                    "You need to provide at least one 'allowed_ips' entry "
                    "to create a server!"
                )

            if self.p['gateway'] != '' and not is_ip(self.p['gateway']):
                self.m.fail_json(
                    f"Gateway '{self.p['gateway']}' is not a valid IP-address!"
                )

        for entry in self.p['allowed_ips']:
            if not is_ip_or_network(entry):
                self.m.fail_json(
                    f"Allowed-ip entry '{entry}' is neither a valid IP-address "
                    f"nor a valid network!"
                )

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
            self.p['peers'] = self._find_peers()
            self.r['diff']['after'] = self.b.build_diff(data=self.p)

    def _find_peers(self) -> list:
        peers = []
        existing = {}

        if self.existing_peers is None:
            self.existing_peers = Peer(
                module=self.m, result={}, session=self.s
            ).get_existing()

        if len(self.p['peers']) > 0:
            for peer in self.existing_peers:
                existing[peer['name']] = peer['uuid']

            for peer in self.p['peers']:
                if peer not in existing:
                    self.m.fail_json(f"Peer '{peer}' does not exist!")

                peers.append(existing[peer])

        return peers
