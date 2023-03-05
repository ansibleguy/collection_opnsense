from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.main import \
    is_unset, validate_int_fields, validate_str_fields
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.cls import BaseModule


class BaseAuth(BaseModule):
    FIELD_ID = 'description'
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
        'authentication': 'auth',
        'public_keys': 'pubkeys',
        'certificates': 'certs',
    }
    FIELDS_TYPING = {
        'bool': ['enabled'],
        'list': ['certificates', 'public_keys'],
        'select': ['connection', 'authentication', 'unique', 'certificates', 'public_keys'],
        'int': ['round'],
    }
    STR_VALIDATIONS = {
        'id': r'^([0-9a-zA-Z\.\-,_\:\@]){0,1024}$',
        'eap_id': r'^([0-9a-zA-Z\.\-,_\:\@]){0,1024}$',
    }
    INT_VALIDATIONS = {
        'round': {'min': 0, 'max': 10},
    }
    EXIST_ATTR = 'auth'

    def __init__(self, m: AnsibleModule, r: dict, s: Session = None):
        BaseModule.__init__(self=self, m=m, r=r, s=s)
        self.auth = {}

    def check(self) -> None:
        if self.p['state'] == 'present':
            validate_int_fields(module=self.m, data=self.p, field_minmax=self.INT_VALIDATIONS)
            validate_str_fields(module=self.m, data=self.p, field_regex=self.b.i.STR_VALIDATIONS)

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
