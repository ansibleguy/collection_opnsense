from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.main import \
    is_ip, valid_hostname, get_selected, is_true, to_digit
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.unbound import \
    validate_domain
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.base import Base


class Host:
    CMDS = {
        'add': 'addHostOverride',
        'del': 'delHostOverride',
        'set': 'setHostOverride',
        'search': 'get',
        'toggle': 'toggleHostOverride',
    }
    API_KEY = 'host'
    API_KEY_1 = 'unbound'
    API_KEY_2 = 'hosts'
    API_MOD = 'unbound'
    API_CONT = 'settings'
    API_CONT_REL = 'service'
    API_CMD_REL = 'reconfigure'
    FIELDS_CHANGE = [
        'hostname', 'domain', 'record_type', 'prio', 'value',
        'description',
    ]
    FIELDS_ALL = ['enabled']
    FIELDS_ALL.extend(FIELDS_CHANGE)
    EXIST_ATTR = 'host'

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None):
        self.m = module
        self.p = module.params
        self.r = result
        self.s = Session(module=module) if session is None else session
        self.exists = False
        self.host = {}
        self.call_cnf = {  # config shared by all calls
            'module': self.API_MOD,
            'controller': self.API_CONT,
        }
        self.existing_entries = None
        self.b = Base(instance=self)

    def check(self):
        if self.p['state'] == 'present':
            if self.p['value'] is None:
                self.m.fail_json(
                    "You need to provide a 'value' to create a host-override!"
                )

            validate_domain(module=self.m, domain=self.p['domain'])

        if self.p['record_type'] == 'MX':
            if not valid_hostname(self.p['value']):
                self.m.fail_json(f"Value '{self.p['value']}' is not a valid hostname!")

        else:
            self.p['prio'] = None

            if self.p['state'] == 'present' and not is_ip(self.p['value']):
                self.m.fail_json(f"Value '{self.p['value']}' is not a valid IP-address!")

        self.b.find(match_fields=self.p['match_fields'])

        if self.p['state'] == 'present':
            self.r['diff']['after'] = self.b.build_diff(data=self.p)

    @staticmethod
    def _simplify_existing(host: dict) -> dict:
        # makes processing easier
        data = {
            'enabled': is_true(host['enabled']),
            'hostname': host['hostname'],
            'uuid': host['uuid'],
            'domain': host['domain'],
            'description': host['description'],
            'record_type': get_selected(host['rr']),
        }

        if data['record_type'] == 'MX':
            data['prio'] = host['mxprio']
            data['value'] = host['mx']

        else:
            data['value'] = host['server']
            data['prio'] = None

        return data

    def _build_request(self) -> dict:
        data = {
            'enabled': to_digit(self.p['enabled']),
            'hostname': self.p['hostname'],
            'domain': self.p['domain'],
            'rr': self.p['record_type'],  # A/AAAA/MX
            'description': self.p['description'],
        }

        if self.p['record_type'] == 'MX':
            data['mxprio'] = self.p['prio']
            data['mx'] = self.p['value']

        else:
            data['server'] = self.p['value']

        return {
            self.API_KEY: data
        }

    def get_existing(self) -> list:
        return self.b.get_existing()

    def create(self):
        self.b.create()

    def update(self):
        self.b.update()

    def process(self):
        self.b.process()

    def delete(self):
        self.b.delete()

    def reload(self):
        self.b.reload()
