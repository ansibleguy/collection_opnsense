import validators

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.main import \
    get_matching, is_true, validate_int_fields, get_selected_list
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.base import Base


class Alert:
    CMDS = {
        'add': 'addAlert',
        'del': 'delAlert',
        'set': 'setAlert',
        'search': 'get',
        'toggle': 'toggleAlert',
    }
    API_KEY = 'alert'
    API_KEY_1 = 'monit'
    API_MOD = 'monit'
    API_CONT = 'settings'
    API_CONT_REL = 'service'
    API_CMD_REL = 'reconfigure'
    FIELDS_CHANGE = ['recipient', 'not_on', 'events', 'format', 'reminder', 'description']
    FIELDS_ALL = ['enabled']
    FIELDS_ALL.extend(FIELDS_CHANGE)
    FIELDS_TRANSLATE = {
        'not_on': 'noton',
    }
    INT_VALIDATIONS = {
        'reminder': {'min': 0, 'max': 86400},
    }
    EXIST_ATTR = 'alert'

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None):
        self.m = module
        self.p = module.params
        self.r = result
        self.s = Session(module=module) if session is None else session
        self.exists = False
        self.alert = {}
        self.call_cnf = {  # config shared by all calls
            'module': self.API_MOD,
            'controller': self.API_CONT,
        }
        self.existing_alerts = None
        self.b = Base(instance=self)

    def check(self):
        validate_int_fields(module=self.m, data=self.p, field_minmax=self.INT_VALIDATIONS)

        if self.p['state'] == 'present':
            if not validators.email(self.p['recipient']):
                self.m.fail_json(
                    f"The recipient value '{self.p['recipient']}' is not a "
                    f"valid email address!"
                )

        # checking if item exists
        self._find_alert()
        if self.exists:
            self.call_cnf['params'] = [self.alert['uuid']]

        if self.p['state'] == 'present':
            self.r['diff']['after'] = self.b.build_diff(data=self.p)

    def _find_alert(self):
        if self.existing_alerts is None:
            self.existing_alerts = self._search_call()

        match = get_matching(
            module=self.m, existing_items=self.existing_alerts,
            compare_item=self.p, match_fields=self.p['match_fields'],
            simplify_func=self._simplify_existing,
        )

        if match is not None:
            self.alert = match
            self.r['diff']['before'] = self.b.build_diff(data=self.alert)
            self.exists = True

    @staticmethod
    def _simplify_existing(alert: dict) -> dict:
        # makes processing easier
        return {
            'enabled': is_true(alert['enabled']),
            'uuid': alert['uuid'],
            'recipient': alert['recipient'],
            'not_on': is_true(alert['noton']),
            'events': get_selected_list(alert['events']),
            'format': alert['format'],
            'reminder': int(alert['reminder']),
            'description': alert['description'],
        }

    def process(self):
        self.b.process()

    def _search_call(self) -> list:
        return self.b.search()

    def get_existing(self) -> list:
        return self.b.get_existing()

    def create(self):
        self.b.create()

    def update(self):
        self.b.update()

    def delete(self):
        self.b.delete()

    def reload(self):
        self.b.reload()
