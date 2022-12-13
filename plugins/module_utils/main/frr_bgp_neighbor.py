from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.main import \
    validate_int_fields, is_ip, simplify_translate
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.base import Base


class Neighbor:
    CMDS = {
        'add': 'addNeighbor',
        'del': 'delNeighbor',
        'set': 'setNeighbor',
        'search': 'get',
        'toggle': 'toggleNeighbor',
    }
    API_KEY = 'neighbor'
    API_KEY_1 = 'bgp'
    API_KEY_2 = 'neighbors'
    API_MOD = 'quagga'
    API_CONT = 'bgp'
    API_CONT_REL = 'service'
    API_CMD_REL = 'reconfigure'
    FIELDS_CHANGE = [
        'ip', 'as_number', 'password', 'weight', 'local_ip', 'source_int',
        'ipv6_link_local_int', 'next_hop_self', 'next_hop_self_all',
        'multi_hop', 'multi_protocol', 'rrclient', 'bfd', 'send_default_route',
        'as_override', 'disable_connected_check', 'keepalive', 'hold_down',
        'connect_timer', 'description', 'prefix_list_in', 'prefix_list_out',
        'route_map_in', 'route_map_out', 'enabled',
    ]
    FIELDS_DIFF_EXCLUDE = ['password']
    FIELDS_ALL = FIELDS_CHANGE
    FIELDS_TRANSLATE = {
        'as_number': 'remoteas',
        'ip': 'address',
        'local_ip': 'localip',
        'source_int': 'updatesource',
        'ipv6_link_local_int': 'linklocalinterface',
        'next_hop_self': 'nexthopself',
        'next_hop_self_all': 'nexthopselfall',
        'multi_hop': 'multihop',
        'multi_protocol': 'multiprotocol',
        'hold_down': 'holddown',
        'connect_timer': 'connecttimer',
        'send_default_route': 'defaultoriginate',
        'as_override': 'asoverride',
        'prefix_list_in': 'linkedPrefixlistIn',
        'prefix_list_out': 'linkedPrefixlistOut',
        'route_map_in': 'linkedRoutemapIn',
        'route_map_out': 'linkedRoutemapOut',
    }
    FIELDS_TYPING = {
        'bool': [
            'next_hop_self', 'next_hop_self_all', 'multi_hop', 'multi_protocol', 'enabled',
            'rrclient', 'bfd', 'send_default_route', 'as_override', 'disable_connected_check',
        ],
        'select': [
            'source_int', 'ipv6_link_local_int', 'prefix_list_in', 'prefix_list_out',
            'route_map_in', 'route_map_out',
        ],
    }
    INT_VALIDATIONS = {
        'as_number': {'min': 1, 'max': 4294967295},
        'weight': {'min': 0, 'max': 65535},
        'keepalive': {'min': 1, 'max': 1000},
        'hold_down': {'min': 3, 'max': 3000},
        'connect_timer': {'min': 1, 'max': 65000},
        'prefix_list_in_seq': {'min': 1, 'max': 4294967294},
        'prefix_list_out_seq': {'min': 1, 'max': 4294967294},
    }
    EXIST_ATTR = 'neighbor'

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None):
        self.m = module
        self.p = module.params
        self.r = result
        self.s = Session(module=module) if session is None else session
        self.exists = False
        self.neighbor = {}
        self.call_cnf = {  # config shared by all calls
            'module': self.API_MOD,
            'controller': self.API_CONT,
        }
        self.b = Base(instance=self)
        self.existing_entries = None
        self.existing_prefixes = None
        self.existing_maps = None

    def check(self):
        if self.p['state'] == 'present':
            if self.p['ip'] in ['', None] or self.p['as_number'] in ['', None]:
                self.m.fail_json(
                    'To create a BGP neighbor you need to provide its AS-number and peer-ip!'
                )

            if not is_ip(self.p['ip']):
                self.m.fail_json(f"Provided peer IP '{self.p['ip']}' is not a valid IP-Address!")

            if self.p['local_ip'] not in ['', None] and not is_ip(self.p['local_ip']):
                self.m.fail_json(f"Provided source IP '{self.p['local_ip']}' is not a valid IP-Address!")

            validate_int_fields(module=self.m, data=self.p, field_minmax=self.INT_VALIDATIONS)

        self.b.find(match_fields=self.p['match_fields'])
        self._find_links()
        if self.exists:
            self.call_cnf['params'] = [self.neighbor['uuid']]

        if self.p['state'] == 'present':
            self.r['diff']['after'] = self.b.build_diff(data=self.p)

    def process(self):
        self.b.process()

    def _search_call(self) -> dict:
        raw = self.s.get(cnf={
            **self.call_cnf, **{'command': self.CMDS['search']}
        })[self.API_KEY_1]

        self.existing_prefixes = raw['prefixlists']['prefixlist']
        self.existing_maps = raw['routemaps']['routemap']

        return raw[self.API_KEY_2][self.API_KEY]

    def _simplify_existing(self, neighbor: dict) -> dict:
        # makes processing easier
        return simplify_translate(
            existing=neighbor,
            typing=self.FIELDS_TYPING,
            translate=self.FIELDS_TRANSLATE,
        )

    def _find_links(self):
        links = {
            'prefix-list-in': {
                'found': False,
                'existing': self.existing_prefixes,
                'match_fields': {'name': 'prefix_list_in'}
            },
            'prefix-list-out': {
                'found': False,
                'existing': self.existing_prefixes,
                'match_fields': {'name': 'prefix_list_out'}
            },
            'route-map-in': {
                'found': False,
                'existing': self.existing_maps,
                'match_fields': {'name': 'route_map_in'}
            },
            'route-map-out': {
                'found': False,
                'existing': self.existing_maps,
                'match_fields': {'name': 'route_map_out'}
            },
        }

        for key, values in links.items():
            value_name = values['match_fields']['name']
            provided = self.p[value_name] not in ['', None]
            seq_uuid_mapping = {}

            if len(values['existing']) > 0 and provided:
                for uuid, entry in values['existing'].items():
                    matching = []

                    for api_field, ans_field in values['match_fields'].items():
                        if self.p[ans_field] not in ['', None]:
                            matching.append(str(entry[api_field]) == str(self.p[ans_field]))

                    if all(matching):
                        self.p[value_name] = uuid
                        values['found'] = True

                        if 'seqnumber' in entry:
                            seq_uuid_mapping[int(entry['seqnumber'])] = uuid

            if provided and not values['found']:
                self.m.fail_json(
                    f"Provided {key} '{value_name}' was not found!"
                )

            if len(seq_uuid_mapping) > 0:
                # only the lowest prefix-list uuid is linkable - all others are just extensions of the first one
                self.p[value_name] = seq_uuid_mapping[min(seq_uuid_mapping.keys())]

    def get_existing(self) -> list:
        existing = []

        for entry in self.b.get_existing():
            if entry['prefix_list_in'] not in [None, ''] and \
                    entry['prefix_list_in'] in self.existing_prefixes:
                entry['prefix_list_in'] = self.existing_prefixes[entry['prefix_list_in']]['name']

            if entry['prefix_list_out'] not in [None, ''] and \
                    entry['prefix_list_out'] in self.existing_prefixes:
                entry['prefix_list_out'] = self.existing_prefixes[entry['prefix_list_out']]['name']

            if entry['route_map_in'] not in [None, ''] and \
                    entry['route_map_in'] in self.existing_maps:
                entry['route_map_in'] = self.existing_maps[entry['route_map_in']]['name']

            if entry['route_map_out'] not in [None, ''] and \
                    entry['route_map_out'] in self.existing_maps:
                entry['route_map_out'] = self.existing_maps[entry['route_map_out']]['name']

            existing.append(entry)

        return existing

    def create(self):
        self.b.create()

    def update(self):
        self.b.update()

    def delete(self):
        self.b.delete()

    def enable(self):
        self.b.enable()

    def disable(self):
        self.b.disable()

    def reload(self):
        self.b.reload()
