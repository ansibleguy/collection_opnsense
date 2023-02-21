from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.main import \
    is_ip, valid_hostname, to_digit, simplify_translate, is_unset
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.unbound import \
    validate_domain
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.cls import BaseModule


class Host(BaseModule):
    CMDS = {
        'add': 'addHostOverride',
        'del': 'delHostOverride',
        'set': 'setHostOverride',
        'search': 'get',
        'toggle': 'toggleHostOverride',
    }
    API_KEY = 'host'
    API_KEY_PATH = f'unbound.hosts.{API_KEY}'
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
    FIELDS_TYPING = {
        'bool': ['enabled'],
        'select': ['record_type'],
    }
    FIELDS_TRANSLATE = {
        'record_type': 'rr',
        # 'prio': 'mxprio',
        # 'value': 'mx',  # mx or server
    }

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None):
        BaseModule.__init__(self=self, m=module, r=result, s=session)
        self.host = {}

    def check(self) -> None:
        if self.p['state'] == 'present':
            if is_unset(self.p['value']):
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

        self._base_check()

    def _simplify_existing(self, host: dict) -> dict:
        simple = simplify_translate(
            existing=host,
            typing=self.FIELDS_TYPING,
            translate=self.FIELDS_TRANSLATE,
        )

        if simple['record_type'] == 'MX':
            simple['prio'] = host['mxprio']
            simple['value'] = host['mx']

        else:
            simple['value'] = host['server']
            simple['prio'] = None

        return simple

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
