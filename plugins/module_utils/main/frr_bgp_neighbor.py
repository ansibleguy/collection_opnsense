from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.main import \
    validate_int_fields, is_ip
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.cls import BaseModule


class Neighbor(BaseModule):
    CMDS = {
        'add': 'addNeighbor',
        'del': 'delNeighbor',
        'set': 'setNeighbor',
        'search': 'get',
        'toggle': 'toggleNeighbor',
    }
    API_KEY_PATH = 'bgp.neighbors.neighbor'
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
        'route_map_in', 'route_map_out',
    ]
    FIELDS_DIFF_EXCLUDE = ['password']
    FIELDS_ALL = ['enabled']
    FIELDS_ALL.extend(FIELDS_CHANGE)
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
    }
    EXIST_ATTR = 'neighbor'
    SEARCH_ADDITIONAL = {
        'existing_prefixes': 'bgp.prefixlists.prefixlist',
        'existing_maps': 'bgp.routemaps.routemap',
    }

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None):
        BaseModule.__init__(self=self, m=module, r=result, s=session)
        self.neighbor = {}
        self.existing_prefixes = None
        self.existing_maps = None

    def check(self) -> None:
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

        self._base_check()
        self._find_links()

    def _find_links(self) -> None:
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

            if not provided:
                continue

            if len(values['existing']) > 0:
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

            if not values['found']:
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
