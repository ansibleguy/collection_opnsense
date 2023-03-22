from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.main import \
    is_unset, validate_int_fields, validate_str_fields
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.cls import BaseModule
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.handler import \
    ModuleSoftError


class BaseAuth(BaseModule):
    FIELD_ID = 'name'
    API_MOD = 'ipsec'
    API_CONT = 'connections'
    API_CONT_REL = 'service'
    API_CMD_REL = 'reconfigure'
    FIELDS_CHANGE = [
        'connection', 'round', 'authentication', 'id', 'eap_id', 'certificates',
        'public_keys',
    ]
    FIELDS_ALL = ['enabled', FIELD_ID]
    FIELDS_ALL.extend(FIELDS_CHANGE)
    FIELDS_TRANSLATE = {
        'name': 'description',
        'authentication': 'auth',
        'public_keys': 'pubkeys',
        'certificates': 'certs',
    }
    FIELDS_TYPING = {
        'bool': ['enabled'],
        'list': ['certificates', 'public_keys'],
        'select': ['connection', 'authentication', 'certificates', 'public_keys'],
        'int': ['round'],
    }
    STR_LEN_VALIDATIONS = {
        'id': {'min': 0, 'max': 1024},
        'eap_id': {'min': 0, 'max': 1024},
    }
    INT_VALIDATIONS = {
        'round': {'min': 0, 'max': 10},
    }
    EXIST_ATTR = 'auth'
    SEARCH_ADDITIONAL = {
        'existing_conns': 'swanctl.Connections.Connection',
        'existing_local_auth': 'swanctl.locals.local',
        'existing_remote_auth': 'swanctl.remotes.remote',
    }

    def __init__(self, m: AnsibleModule, r: dict, s: Session = None):
        BaseModule.__init__(self=self, m=m, r=r, s=s)
        self.auth = {}
        self.existing_conns = None
        self.pubkey_link_found = False
        self.existing_local_auth = None
        self.existing_remote_auth = None
        self.existing_pubkeys = None
        self.existing_certs = None

    def check(self) -> None:
        if self.p['state'] == 'present':
            validate_int_fields(module=self.m, data=self.p, field_minmax=self.INT_VALIDATIONS)
            validate_str_fields(
                module=self.m, data=self.p, allow_empty=True,
                field_minmax_length=self.STR_LEN_VALIDATIONS
            )

            if is_unset(self.p['connection']):
                self.m.fail_json(
                    "You need to provide a 'connection' to create an IPSec auth!"
                )

            if self.p['authentication'] == 'pubkey' and (
                    is_unset(self.p['certificates']) and
                    is_unset(self.p['public_keys'])
            ):
                self.m.fail_json(
                    "You need to provide at least one certificate or public-key to use the 'pubkey' "
                    'authentication method!'
                )

            if self.p['authentication'] in ['eap_tls', 'eap_mschapv2', 'eap_radius'] and \
                    is_unset(self.p['eap_id']):
                self.m.fail_json(
                    f"You need to provide an 'eap_id' to use the '{self.p['authentication']}' "
                    'authentication method!'
                )

        self._base_check()

        if self.p['state'] == 'present':
            self.b.find_single_link(
                field='connection',
                existing=self.existing_conns,
                existing_field_id='description',
            )

            if self.p['authentication'] == 'pubkey':
                try:
                    self._find_links_pubkeys_certs()
                    self.pubkey_link_found = True

                except ModuleSoftError:
                    # if neither a local nor a remote authentication-entry exists ->
                    #   we must create one first to get the relevant entries
                    pass

    def create(self) -> None:
        if self.p['authentication'] == 'pubkey' and not self.pubkey_link_found:
            # creating dummy-auth-entry to use for getting cert/pubkey infos
            self.p['authentication'] = 'psk'
            certs, pubkeys = self.p['certificates'], self.p['public_keys']
            self.p['certificates'], self.p['public_keys'] = [], []
            self.b.create()

            self.auth = {}
            # pylint: disable=W0201
            self.existing_entries = None
            self.existing_local_auth = None
            self.existing_remote_auth = None

            self.p['certificates'], self.p['public_keys'] = certs, pubkeys
            self.p['authentication'] = 'pubkey'
            self._base_check()
            self._find_links_pubkeys_certs()

            self.b.update()

        else:
            self.b.create()

    def _get_existing_pubkeys_certs(self, search: str, existing_target: str):
        for existing in [self.existing_local_auth, self.existing_remote_auth]:
            if not is_unset(existing):
                first = list(existing.keys())[0]
                if search in existing[first]:
                    setattr(self, existing_target, existing[first][search])

    def _find_links_pubkeys_certs(self):
        if not is_unset(self.p['certificates']):
            self._get_existing_pubkeys_certs(
                search='certs',
                existing_target='existing_certs',
            )
            self.b.find_multiple_links(
                existing_field_id='value',
                field='certificates',
                existing=self.existing_certs,
                fail_soft=True, fail=False,
            )

        else:
            self._get_existing_pubkeys_certs(
                search='pubkeys',
                existing_target='existing_pubkeys',
            )
            self.b.find_multiple_links(
                existing_field_id='value',
                field='public_keys',
                existing=self.existing_pubkeys,
                fail_soft=True, fail=False
            )
