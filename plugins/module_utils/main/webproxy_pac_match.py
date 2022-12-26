from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.cls import BaseModule
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.main import is_unset


class Match(BaseModule):
    FIELD_ID = 'name'
    CMDS = {
        'add': 'addPACMatch',
        'set': 'setPACMatch',
        'del': 'delPACMatch',
        'search': 'get',
    }
    API_KEY_PATH = 'proxy.pac.match'
    API_MOD = 'proxy'
    API_CONT = 'settings'
    API_CONT_REL = 'service'
    API_CMD_REL = 'reconfigure'
    FIELDS_CHANGE = [
        'negate', 'url', 'description', 'type', 'hostname', 'network',
        'domain_level_from', 'domain_level_to', 'hour_from', 'hour_to',
        'month_from', 'month_to', 'weekday_from', 'weekday_to',
    ]
    FIELDS_ALL = [FIELD_ID]
    FIELDS_ALL.extend(FIELDS_CHANGE)
    FIELDS_TRANSLATE = {
        'type': 'match_type',
        'hour_from': 'time_from',
        'hour_to': 'time_to',
        'month_from': 'date_from',
        'month_to': 'date_to',
    }
    FIELDS_TYPING = {
        'select': ['type', 'month_from', 'month_to', 'weekday_from', 'weekday_to'],
        'bool': ['negate'],
        'int': [
            'domain_level_from', 'domain_level_to', 'hour_from', 'hour_to', 'month_from',
            'month_to', 'weekday_from', 'weekday_to',
        ],
    }
    INT_VALIDATIONS = {
        'hour_from': {'min': 0, 'max': 23},
        'hour_to': {'min': 0, 'max': 23},
    }
    EXIST_ATTR = 'proxy'

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None):
        BaseModule.__init__(self=self, m=module, r=result, s=session)
        self.proxy = {}

    def check(self):
        if self.p['state'] == 'present':
            if self.p['type'] == 'url_matches':
                if is_unset(self.p['url']):
                    self.m.fail_json('You need to provide an URL to match!')

            if self.p['type'] in [
                'hostname_matches', 'plain_hostname', 'is_resolvable', 'dns_domain_is',
            ] and is_unset(self.p['hostname']):
                self.m.fail_json('You need to provide a hostname to match!')

            if self.p['type'] in ['my_ip_in_net', 'destination_in_net'] and \
                    is_unset(self.p['network']):
                self.m.fail_json('You need to provide a network to match!')

            from_to_fields = {
                'date_range': {'from': 'month_from', 'to': 'month_to'},
                'time_range': {'from': 'hour_from', 'to': 'hour_to'},
                'weekday_range': {'from': 'weekday_from', 'to': 'weekday_to'},
                'dns_domain_levels': {'from': 'domain_level_from', 'to': 'domain_level_to'},
            }

            for match_type, from_to in from_to_fields.items():
                if self.p['type'] == match_type and (
                        is_unset(self.p[from_to['from']]) or is_unset(from_to['to'])
                ):
                    self.m.fail_json(
                        f"You need to provide a '{from_to['from']}' and '{from_to['to']}' "
                        'to match!'
                    )

        self.b.find(match_fields=[self.FIELD_ID])
        if self.exists:
            self.call_cnf['params'] = [self.proxy['uuid']]

        if self.p['state'] == 'present':
            self.r['diff']['after'] = self.b.build_diff(data=self.p)
