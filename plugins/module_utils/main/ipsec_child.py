from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.main import \
    validate_int_fields, is_unset
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.cls import BaseModule


class Child(BaseModule):
    FIELD_ID = 'description'
    CMDS = {
        'add': 'addChild',
        'del': 'delChild',
        'set': 'setChild',
        'search': 'get',
        'toggle': 'toggleChild',
    }
    API_KEY_PATH = 'ipsec.children.child'
    API_MOD = 'ipsec'
    API_CONT = 'connections'
    API_CONT_REL = 'service'
    API_CMD_REL = 'reconfigure'
    FIELDS_CHANGE = [
        'connection', 'request_id', 'eap_proposals', 'sha256_96', 'start_action',
        'close_action', 'dpd_action', 'mode', 'policies', 'local_ts', 'remote_ts',
        'rekey_seconds',
    ]
    FIELDS_ALL = ['enabled', FIELD_ID]
    FIELDS_ALL.extend(FIELDS_CHANGE)
    FIELDS_TRANSLATE = {
        'request_id': 'reqid',
        'rekey_seconds': 'rekey_time',
    }
    FIELDS_TYPING = {
        'bool': ['enabled', 'policies', 'sha256_96'],
        'list': ['eap_proposals', 'local_ts', 'remote_ts'],
        'select': ['mode', 'dpd_action', 'close_action', 'start_action', 'connection'],
        'int': ['rekey_seconds', 'request_id'],
    }
    INT_VALIDATIONS = {
        'request_id': {'min': 1, 'max': 65535},
        'rekey_seconds': {'min': 0, 'max': 500000},
    }
    EXIST_ATTR = 'child'

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None):
        BaseModule.__init__(self=self, m=module, r=result, s=session)
        self.child = {}

    def check(self) -> None:
        if self.p['state'] == 'present':
            validate_int_fields(module=self.m, data=self.p, field_minmax=self.INT_VALIDATIONS)

            if is_unset(self.p['connection']):
                self.m.fail_json(
                    "You need to provide a 'connection' to create an IPSec child!"
                )

        self._base_check()
