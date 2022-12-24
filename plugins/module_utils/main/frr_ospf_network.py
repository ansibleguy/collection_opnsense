from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.main import \
    validate_int_fields, is_ip_or_network
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.cls import BaseModule


class Network(BaseModule):
    CMDS = {
        'add': 'addNetwork',
        'del': 'delNetwork',
        'set': 'setNetwork',
        'search': 'get',
        'toggle': 'toggleNetwork',
    }
    API_KEY = 'network'
    API_KEY_1 = 'ospf'
    API_KEY_2 = 'networks'
    API_MOD = 'quagga'
    API_CONT = 'ospfsettings'
    API_CONT_REL = 'service'
    API_CMD_REL = 'reconfigure'
    FIELDS_CHANGE = ['ip', 'mask', 'area', 'area_range', 'prefix_list_in', 'prefix_list_out']
    FIELDS_ALL = ['enabled']
    FIELDS_ALL.extend(FIELDS_CHANGE)
    FIELDS_TRANSLATE = {
        'ip': 'ipaddr',
        'mask': 'netmask',
        'area_range': 'arearange',
        'prefix_list_in': 'linkedPrefixlistIn',
        'prefix_list_out': 'linkedPrefixlistOut',
    }
    FIELDS_TYPING = {
        'bool': ['enabled'],
        'select': ['prefix_list_in', 'prefix_list_out'],
    }
    INT_VALIDATIONS = {
        'mask': {'min': 0, 'max': 32},
    }
    EXIST_ATTR = 'net'

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None):
        BaseModule.__init__(self=self, m=module, r=result, s=session)
        self.net = {}
        self.existing_paths = None
        self.existing_prefixes = None
        self.existing_communities = None

    def check(self):
        if self.p['state'] == 'present':
            if self.p['area'] in ['', None]:
                self.m.fail_json(
                    'To create a OSPF network you need to provide an area!'
                )

            if not is_ip_or_network(f"{self.p['ip']}/{self.p['mask']}", strict=True):
                self.m.fail_json(
                    'The combination of the provided ip and network mask is invalid: '
                    f"'{self.p['ip']}/{self.p['mask']}'!"
                )

            validate_int_fields(module=self.m, data=self.p, field_minmax=self.INT_VALIDATIONS)

        self.b.find(match_fields=self.p['match_fields'])
        self._find_links()
        if self.exists:
            self.call_cnf['params'] = [self.net['uuid']]

        if self.p['state'] == 'present':
            self.r['diff']['after'] = self.b.build_diff(data=self.p)

    def _search_call(self) -> dict:
        raw = self.s.get(cnf={
            **self.call_cnf, **{'command': self.CMDS['search']}
        })[self.API_KEY_1]

        self.existing_prefixes = raw['prefixlists']['prefixlist']
        return raw[self.API_KEY_2][self.API_KEY]

    def _find_links(self):
        links = {
            'prefix-list': {
                'in': 'prefix_list_in',
                'out': 'prefix_list_out',
                'in_found': False,
                'out_found': False,
                'existing': self.existing_prefixes,
            }
        }

        for key, values in links.items():
            in_provided = self.p[values['in']] not in ['', None]
            out_provided = self.p[values['out']] not in ['', None]

            if len(values['existing']) > 0 and (in_provided or out_provided):
                for uuid, prefix in values['existing'].items():
                    if prefix['name'] == self.p[values['in']]:
                        self.p[values['in']] = uuid
                        values['in_found'] = True

                    if prefix['name'] == self.p[values['out']]:
                        self.p[values['out']] = uuid
                        values['out_found'] = True

                    if values['in_found'] and values['out_found']:
                        break

            if in_provided and not values['in_found']:
                self.m.fail_json(
                    f"Provided in-{key} '{self.p[values['in']]}' was not found!"
                )

            if out_provided and not values['out_found']:
                self.m.fail_json(
                    f"Provided out-{key} '{self.p[values['out']]}' was not found!"
                )

    def get_existing(self) -> list:
        existing = []

        for entry in self.b.get_existing():
            if entry['prefix_list_in'] not in [None, ''] and \
                    entry['prefix_list_in'] in self.existing_prefixes:
                entry['prefix_list_in'] = self.existing_prefixes[entry['prefix_list_in']]['name']

            if entry['prefix_list_out'] not in [None, ''] and \
                    entry['prefix_list_out'] in self.existing_prefixes:
                entry['prefix_list_out'] = self.existing_prefixes[entry['prefix_list_out']]['name']

            existing.append(entry)

        return existing
