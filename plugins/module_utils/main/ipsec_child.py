from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.main import \
    validate_int_fields, is_unset
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.cls import BaseModule


class Child(BaseModule):
    FIELD_ID = 'name'
    CMDS = {
        'add': 'addChild',
        'del': 'delChild',
        'set': 'setChild',
        'search': 'get',
        'toggle': 'toggleChild',
    }
    API_KEY_PATH = 'swanctl.children.child'
    API_MOD = 'ipsec'
    API_CONT = 'connections'
    API_CONT_REL = 'service'
    API_CMD_REL = 'reconfigure'
    FIELDS_CHANGE = [
        'connection', 'request_id', 'esp_proposals', 'sha256_96', 'start_action',
        'close_action', 'dpd_action', 'mode', 'policies', 'local_net', 'remote_net',
        'rekey_seconds',
    ]
    FIELDS_ALL = ['enabled', FIELD_ID]
    FIELDS_ALL.extend(FIELDS_CHANGE)
    FIELDS_TRANSLATE = {
        'name': 'description',
        'request_id': 'reqid',
        'rekey_seconds': 'rekey_time',
        'local_net': 'local_ts',
        'remote_net': 'remote_ts',
    }
    FIELDS_TYPING = {
        'bool': ['enabled', 'policies', 'sha256_96'],
        'list': ['esp_proposals', 'local_net', 'remote_net'],
        'select': ['mode', 'dpd_action', 'close_action', 'start_action', 'connection'],
        'int': ['rekey_seconds', 'request_id'],
    }
    INT_VALIDATIONS = {
        'request_id': {'min': 1, 'max': 65535},
        'rekey_seconds': {'min': 0, 'max': 500000},
    }
    EXIST_ATTR = 'child'
    SEARCH_ADDITIONAL = {
        'existing_conns': 'swanctl.Connections.Connection',
    }

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None):
        BaseModule.__init__(self=self, m=module, r=result, s=session)
        self.child = {}
        self.existing_conns = None

    def check(self) -> None:
        if self.p['state'] == 'present':
            validate_int_fields(module=self.m, data=self.p, field_minmax=self.INT_VALIDATIONS)

            for field in ['connection', 'local_net', 'remote_net']:
                if is_unset(self.p[field]):
                    self.m.fail_json(
                        f"You need to provide a '{field}' to create an IPSec child!"
                    )

        self._base_check()
        if self.p['state'] == 'present':
            self.b.find_single_link(
                field='connection',
                existing=self.existing_conns,
                existing_field_id='description',
            )
