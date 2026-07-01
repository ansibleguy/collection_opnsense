from ansible.module_utils.basic import AnsibleModule

from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.oxlorg.opnsense.plugins.module_utils.helper.validate import \
    is_unset
from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.module import BaseModule


class PeerGroup(BaseModule):
    FIELD_ID = 'name'
    CMDS = {
        'add': 'addPeergroup',
        'del': 'delPeergroup',
        'set': 'setPeergroup',
        'search': 'get',
        'toggle': 'togglePeergroup',
    }
    API_KEY_PATH = 'bgp.peergroups.peergroup'
    API_MOD = 'quagga'
    API_CONT = 'bgp'
    API_CONT_REL = 'service'
    FIELDS_CHANGE = [
        'as_mode', 'as_number', 'source_int', 'next_hop_self', 'send_default_route',
        'prefix_list_in', 'prefix_list_out', 'route_map_in', 'route_map_out', 'listen_ranges',
    ]
    FIELDS_ALL = ['enabled', 'name']
    FIELDS_ALL.extend(FIELDS_CHANGE)
    FIELDS_TRANSLATE = {
        'as_mode': 'remote_as_mode',
        'as_number': 'remoteas',
        'source_int': 'updatesource',
        'next_hop_self': 'nexthopself',
        'send_default_route': 'defaultoriginate',
        'prefix_list_in': 'linkedPrefixlistIn',
        'prefix_list_out': 'linkedPrefixlistOut',
        'route_map_in': 'linkedRoutemapIn',
        'route_map_out': 'linkedRoutemapOut',
        'listen_ranges': 'listenranges',
    }
    FIELDS_TYPING = {
        'bool': [
            'next_hop_self', 'enabled', 'send_default_route',
        ],
        'select': [
            'as_mode', 'source_int', 'prefix_list_in', 'prefix_list_out',
            'route_map_in', 'route_map_out',
        ],
        'list': ['listen_ranges'],
    }
    INT_VALIDATIONS = {
        'as_number': {'min': 1, 'max': 4294967295},
    }
    EXIST_ATTR = 'peergroup'
    SEARCH_ADDITIONAL = {
        'existing_prefixes': 'bgp.prefixlists.prefixlist',
        'existing_maps': 'bgp.routemaps.routemap',
    }

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None):
        BaseModule.__init__(self=self, m=module, r=result, s=session)
        self.peergroup = {}
        self.existing_prefixes = None
        self.existing_maps = None

    def check(self) -> None:
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
            provided = not is_unset(self.p[value_name])
            seq_uuid_mapping = {}

            if not provided:
                continue

            if len(values['existing']) > 0:
                for uuid, entry in values['existing'].items():
                    matching = []

                    for api_field, ans_field in values['match_fields'].items():
                        if not is_unset(self.p[ans_field]):
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

        for entry in self._base_get_existing():
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
