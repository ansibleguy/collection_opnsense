from ansible.module_utils.basic import AnsibleModule

from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.oxlorg.opnsense.plugins.module_utils.helper.validate import \
    is_ip, is_ip_or_network, is_unset
from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.module import BaseModule
from ansible_collections.oxlorg.opnsense.plugins.module_utils.helper.validate import \
    is_valid_domain


class Peer(BaseModule):
    FIELD_ID = 'name'
    CMDS = {
        'add': 'add_client',
        'del': 'del_client',
        'set': 'set_client',
        'search': 'search_client',
        'detail': 'get_client',
        'toggle': 'toggle_client',
    }
    API_KEY_PATH = 'client'
    API_MOD = 'wireguard'
    API_CONT = 'client'
    API_CONT_REL = 'service'
    FIELDS_CHANGE = [
        'public_key', 'psk', 'port', 'allowed_ips', 'server', 'keepalive', 'servers',
    ]
    FIELDS_ALL = [FIELD_ID, 'enabled']
    FIELDS_ALL.extend(FIELDS_CHANGE)
    FIELDS_TRANSLATE = {
        'public_key': 'pubkey',
        'allowed_ips': 'tunneladdress',
        'server': 'serveraddress',
        'port': 'serverport',
    }
    FIELDS_TYPING = {
        'bool': ['enabled'],
        'list': ['allowed_ips', 'servers'],
        'int': ['port', 'keepalive'],
    }
    FIELDS_OPTIONAL = ['keepalive']
    FIELDS_DIFF_NO_LOG = ['psk']
    INT_VALIDATIONS = {
        'keepalive': {'min': 1, 'max': 86400},
        'port': {'min': 1, 'max': 65535},
    }
    STR_VALIDATIONS = {
        'name': r'^([0-9a-zA-Z._\-]){1,64}$'
    }
    EXIST_ATTR = 'peer'
    FIELDS_DIFF_EXCLUDE = []

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None, fail: dict = None):
        BaseModule.__init__(self=self, m=module, r=result, s=session, f=fail)
        self.peer = {}
        self.existing_servers = None
        self.existing_peers = None

    def check(self) -> None:
        if self.p['state'] == 'present':
            if is_unset(self.p['public_key']):
                self.m.fail_json(
                    "You need to provide a 'public_key' if you want to create a peer!"
                )

            if is_unset(self.p['allowed_ips']):
                self.m.fail_json(
                    "You need to provide at least one 'allowed_ips' entry "
                    "of the peer to create!"
                )

        link_servers = not is_unset(self.p['servers']) or self.p['link_servers']
        if not link_servers:
            self.FIELDS_CHANGE.remove('servers')
            self.FIELDS_DIFF_EXCLUDE.append('servers')

        for entry in self.p['allowed_ips']:
            if not is_ip_or_network(entry):
                self.m.fail_json(
                    f"Allowed-ip entry '{entry}' is neither a valid IP-address "
                    f"nor a valid network!"
                )

        if not is_unset(self.p['server']) and \
                not is_ip(self.p['server']) and not is_valid_domain(self.p['server']):
            self.m.fail_json(
                f"Peer endpoint/server '{self.p['server']}' is neither a valid IP-address "
                f"nor a valid domain!"
            )

        self.find(match_fields=[self.FIELD_ID])
        if self.p['state'] == 'present' and not is_unset(self.p['servers']):
            self.p['servers'] = self._translate_servers(self.p['servers'])

        if self.exists:
            if link_servers:
                self.peer['servers'] = self._translate_servers(self.r['diff']['before']['servers'])

            self.r['diff']['before'] = self.build_diff(data=self.peer)

        self._base_check()

    def _translate_servers(self, search_in: list) -> list:
        from ansible_collections.oxlorg.opnsense.plugins.module_utils.main.wireguard_server import Server

        servers = []
        existing = {}

        if self.existing_servers is None:
            self.existing_servers = Server(
                module=self.m, result={}, session=self.s
            ).get_existing()

        if len(search_in) == 0:
            return []

        for srv in self.existing_servers:
            existing[srv['name']] = srv['uuid']

        for srv in search_in:
            if srv not in existing and srv not in existing.values():
                self.m.fail_json(f"Server '{srv}' does not exist!")

            if srv in existing:
                servers.append(existing[srv])

            else:
                servers.append(srv)

        return servers
