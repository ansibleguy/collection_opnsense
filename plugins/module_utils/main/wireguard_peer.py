from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.main import \
    validate_int_fields, validate_str_fields, is_ip, validate_port, is_ip_or_network, \
    is_unset
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.cls import BaseModule
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.validate import \
    is_valid_domain


class Peer(BaseModule):
    FIELD_ID = 'name'
    CMDS = {
        'add': 'addClient',
        'del': 'delClient',
        'set': 'setClient',
        'search': 'get',
        'toggle': 'toggleClient',
    }
    API_KEY_PATH = 'client.clients.client'
    API_MOD = 'wireguard'
    API_CONT = 'client'
    API_CONT_REL = 'service'
    API_CMD_REL = 'reconfigure'
    FIELDS_CHANGE = [
        'public_key', 'psk', 'port', 'allowed_ips', 'endpoint', 'keepalive',
    ]
    FIELDS_ALL = [FIELD_ID, 'enabled']
    FIELDS_ALL.extend(FIELDS_CHANGE)
    FIELDS_TRANSLATE = {
        'public_key': 'pubkey',
        'allowed_ips': 'tunneladdress',
        'endpoint': 'serveraddress',
        'port': 'serverport',
    }
    FIELDS_TYPING = {
        'bool': ['enabled'],
        'list': ['allowed_ips'],
        'int': ['port', 'keepalive'],
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
        BaseModule.__init__(self=self, m=module, r=result, s=session)
        self.peer = {}
        self.existing_peers = None

    def check(self) -> None:
        if self.p['state'] == 'present':
            validate_port(module=self.m, port=self.p['port'])
            validate_int_fields(module=self.m, data=self.p, field_minmax=self.INT_VALIDATIONS)
            validate_str_fields(
                module=self.m, data=self.p,
                field_regex=self.STR_VALIDATIONS,
                field_minmax_length=self.STR_LEN_VALIDATIONS
            )

            if is_unset(self.p['public_key']):
                self.m.fail_json(
                    "You need to provide a 'public_key' if you want to create a peer!"
                )

            if is_unset(self.p['allowed_ips']):
                self.m.fail_json(
                    "You need to provide at least one 'allowed_ips' entry "
                    "of the peer to create!"
                )

        for entry in self.p['allowed_ips']:
            if not is_ip_or_network(entry):
                self.m.fail_json(
                    f"Allowed-ip entry '{entry}' is neither a valid IP-address "
                    f"nor a valid network!"
                )

        if self.p['endpoint'] != '' and \
                not is_ip(self.p['endpoint']) and not is_valid_domain(self.p['endpoint']):
            self.m.fail_json(
                f"Peer endpoint '{self.p['endpoint']}' is neither a valid IP-address "
                f"nor a valid domain!"
            )

        self._base_check()
