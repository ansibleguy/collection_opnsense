from ansible.module_utils.basic import AnsibleModule

from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.module import BaseModule
from ansible_collections.oxlorg.opnsense.plugins.module_utils.helper.validate import \
    is_valid_email


class Alert(BaseModule):
    CMDS = {
        'add': 'add_alert',
        'del': 'del_alert',
        'set': 'set_alert',
        'search': 'get',
        'toggle': 'toggle_alert',
    }
    API_KEY_PATH = 'monit.alert'
    API_MOD = 'monit'
    API_CONT = 'settings'
    API_CONT_REL = 'service'
    FIELDS_CHANGE = ['recipient', 'not_on', 'events', 'format', 'reminder', 'description']
    FIELDS_ALL = ['enabled']
    FIELDS_ALL.extend(FIELDS_CHANGE)
    FIELDS_TRANSLATE = {
        'not_on': 'noton',
    }
    FIELDS_TYPING = {
        'bool': ['enabled', 'not_on'],
        'list': ['events'],
        'int': ['reminder'],
    }
    INT_VALIDATIONS = {
        'reminder': {'min': 0, 'max': 86400},
    }
    EXIST_ATTR = 'alert'

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None, fail: dict = None):
        BaseModule.__init__(self=self, m=module, r=result, s=session, f=fail)
        self.alert = {}

    def check(self) -> None:
        if self.p['state'] == 'present':
            if not is_valid_email(self.p['recipient']):
                self.m.fail_json(
                    f"The recipient value '{self.p['recipient']}' is not a "
                    f"valid email address!"
                )

        self._base_check()
