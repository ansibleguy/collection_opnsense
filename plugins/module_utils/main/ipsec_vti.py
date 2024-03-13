from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.main import \
    validate_int_fields, is_unset
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.cls import BaseModule


class Vti(BaseModule):
    FIELD_ID = 'name'
    CMDS = {
        'add': 'add',
        'del': 'del',
        'set': 'set',
        'search': 'search',
        'detail': 'get',
        'toggle': 'toggle',
    }
    API_KEY_PATH = 'vti'
    API_MOD = 'ipsec'
    API_CONT = 'vti'
    API_CONT_REL = 'service'
    API_CMD_REL = 'reconfigure'
    FIELDS_CHANGE = [
        'request_id', 'local_address', 'remote_address',
        'local_tunnel_address', 'remote_tunnel_address',
    ]
    FIELDS_ALL = ['enabled', FIELD_ID]
    FIELDS_ALL.extend(FIELDS_CHANGE)
    FIELDS_TRANSLATE = {
        'name': 'description',
        'request_id': 'reqid',
        'local_address': 'local',
        'remote_address': 'remote',
        'local_tunnel_address': 'tunnel_local',
        'remote_tunnel_address': 'tunnel_remote',
    }
    FIELDS_TYPING = {
        'int': ['request_id'],
    }
    INT_VALIDATIONS = {
        'request_id': {'min': 1, 'max': 65535},
    }
    EXIST_ATTR = 'vti'

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None):
        BaseModule.__init__(self=self, m=module, r=result, s=session)
        self.vti = {}

    def check(self) -> None:
        if self.p['state'] == 'present':
            validate_int_fields(module=self.m, data=self.p, field_minmax=self.INT_VALIDATIONS)

            if is_unset(self.p['local_address']) or is_unset(self.p['remote_address']) or \
                    is_unset(self.p['local_tunnel_address']) or \
                    is_unset(self.p['remote_tunnel_address']):
                self.m.fail_json(
                    "You need to provide a 'local_address', 'remote_address', "
                    "'local_tunnel_address' and 'remote_tunnel_address' to create an IPSec VTI!"
                )

        self._base_check()
