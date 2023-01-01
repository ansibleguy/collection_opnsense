from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.main import \
    validate_int_fields
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.cls import BaseModule


class AsPath(BaseModule):
    FIELD_ID = 'description'
    CMDS = {
        'add': 'addAspath',
        'del': 'delAspath',
        'set': 'setAspath',
        'search': 'get',
        'toggle': 'toggleAspath',
    }
    API_KEY_PATH = 'bgp.aspaths.aspath'
    API_MOD = 'quagga'
    API_CONT = 'bgp'
    API_CONT_REL = 'service'
    API_CMD_REL = 'reconfigure'
    FIELDS_CHANGE = ['number', 'action', 'as_pattern']
    FIELDS_ALL = [FIELD_ID, 'enabled']
    FIELDS_ALL.extend(FIELDS_CHANGE)
    FIELDS_TRANSLATE = {
        'as_pattern': 'as',
    }
    FIELDS_TYPING = {
        'bool': ['enabled'],
        'select': ['action'],
    }
    INT_VALIDATIONS = {
        'number': {'min': 10, 'max': 99},
    }
    EXIST_ATTR = 'as_path'

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None):
        BaseModule.__init__(self=self, m=module, r=result, s=session)
        self.as_path = {}

    def check(self) -> None:
        if self.p['state'] == 'present':
            if self.p['number'] in ['', None] or self.p['as_pattern'] in ['', None] \
                    or self.p['action'] in ['', None]:
                self.m.fail_json(
                    'To create a BGP as-path you need to provide a number, '
                    'as_pattern and action!'
                )

            validate_int_fields(module=self.m, data=self.p, field_minmax=self.INT_VALIDATIONS)

        self.b.find(match_fields=[self.FIELD_ID])
        if self.exists:
            self.call_cnf['params'] = [self.as_path['uuid']]

        if self.p['state'] == 'present':
            self.r['diff']['after'] = self.b.build_diff(data=self.p)
