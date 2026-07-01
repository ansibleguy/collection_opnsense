from ansible.module_utils.basic import AnsibleModule

from ansible_collections.oxlorg.opnsense.plugins.module_utils.helper.translate import \
    get_key_by_value_from_selection
from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.module import BaseModule


class Privilege(BaseModule):
    FIELD_PK = 'id'
    FIELD_ID = 'id'
    CMDS = {
        'set': 'set_item',
        'search': 'search',
        'detail': 'get_item',
    }
    API_KEY_PATH = 'priv'
    API_MOD = 'auth'
    API_CONT = 'priv'
    FIELDS_CHANGE = ['user', 'group']
    FIELDS_TYPING = {
        'list': ['user', 'group'],
    }
    FIELDS_TRANSLATE = {
        'user': 'users',
        'group': 'groups',
    }
    FIELDS_ALL = ['id']
    FIELDS_ALL.extend(FIELDS_CHANGE)
    EXIST_ATTR = 'privilege'

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None):
        BaseModule.__init__(self=self, m=module, r=result, s=session)
        self.privilege = {}

    def process(self) -> None:
        if not self.exists:
            self.m.fail_json(f"Privilege {self.p['id']} not found")

        self.p['user'] = [
            get_key_by_value_from_selection(self.raw['users'], u)
            for u in self.p['user']
        ]
        self.p['group'] = [
            get_key_by_value_from_selection(self.raw['groups'], g)
            for g in self.p['group']
        ]

        if self.p['state'] == 'present':
            self.p['user'] = list(set(self.p['user'] + self.privilege['user']))
            self.p['group'] = list(set(self.p['group'] + self.privilege['group']))

        elif self.p['state'] == 'absent':
            self.p['user'] = list(set(self.privilege['user']).difference(self.p['user']))
            self.p['group'] = list(set(self.privilege['group']).difference(self.p['group']))

        self.update()
