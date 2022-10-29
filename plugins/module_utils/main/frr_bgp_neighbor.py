from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.main import \
    is_true, validate_int_fields, get_selected, is_ip
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
    INT_VALIDATIONS = {
        'as_number': {'min': 1, 'max': 4294967295},
        'weight': {'min': 0, 'max': 65535},
        'keepalive': {'min': 1, 'max': 1000},
        'hold_down': {'min': 3, 'max': 3000},
        'connect_timer': {'min': 1, 'max': 65000},
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
        self.prefix_in_found = False
        self.prefix_out_found = False
        self.map_in_found = False
        self.map_out_found = False

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
        if self.exists:
            self.call_cnf['params'] = [self.neighbor['uuid']]

        self._find_prefix()
        self._find_map()

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

    @staticmethod
    def _simplify_existing(neighbor: dict) -> dict:
        # makes processing easier
        return {
            'ip': neighbor['address'],
            'as_number': neighbor['remoteas'],
            'password': neighbor['password'],
            'weight': neighbor['weight'],
            'local_ip': neighbor['localip'],
            'source_int': get_selected(neighbor['updatesource']),
            'ipv6_link_local_int': get_selected(neighbor['linklocalinterface']),
            'next_hop_self': is_true(neighbor['nexthopself']),
            'next_hop_self_all': is_true(neighbor['nexthopselfall']),
            'multi_hop': is_true(neighbor['multihop']),
            'multi_protocol': is_true(neighbor['multiprotocol']),
            'rrclient': is_true(neighbor['rrclient']),
            'bfd': is_true(neighbor['bfd']),
            'send_default_route': is_true(neighbor['defaultoriginate']),
            'as_override': is_true(neighbor['asoverride']),
            'disable_connected_check': is_true(neighbor['disable_connected_check']),
            'keepalive': neighbor['keepalive'],
            'hold_down': neighbor['holddown'],
            'connect_timer': neighbor['connecttimer'],
            'description': neighbor['description'],
            'prefix_list_in': get_selected(neighbor['linkedPrefixlistIn']),
            'prefix_list_out': get_selected(neighbor['linkedPrefixlistOut']),
            'route_map_in': get_selected(neighbor['linkedRoutemapIn']),
            'route_map_out': get_selected(neighbor['linkedRoutemapOut']),
            'enabled': is_true(neighbor['enabled']),
            'uuid': neighbor['uuid'],
        }

    def _find_prefix(self):
        pre_in_provided = self.p['prefix_list_in'] not in ['', None]
        pre_out_provided = self.p['prefix_list_out'] not in ['', None]

        if len(self.existing_prefixes) > 0 and (pre_in_provided or pre_out_provided):
            for uuid, prefix in self.existing_prefixes.items():
                if prefix['name'] == self.p['prefix_list_in']:
                    self.p['prefix_list_in'] = uuid
                    self.prefix_in_found = True

                if prefix['name'] == self.p['prefix_list_out']:
                    self.p['prefix_list_out'] = uuid
                    self.prefix_out_found = True

                if self.prefix_in_found and self.prefix_out_found:
                    break

        if pre_in_provided and not self.prefix_in_found:
            self.m.fail_json(
                f"Provided in-prefix-list '{self.p['prefix_list_in']}' was not found!"
            )

        if pre_out_provided and not self.prefix_out_found:
            self.m.fail_json(
                f"Provided out-prefix-list '{self.p['prefix_list_out']}' was not found!"
            )

    def _find_map(self):
        map_in_provided = self.p['route_map_in'] not in ['', None]
        map_out_provided = self.p['route_map_out'] not in ['', None]

        if len(self.existing_maps) > 0 and (map_in_provided or map_out_provided):
            for uuid, route_map in self.existing_prefixes.items():
                if route_map['name'] == self.p['route_map_in']:
                    self.p['route_map_in'] = uuid
                    self.map_in_found = True

                if route_map['name'] == self.p['route_map_out']:
                    self.p['route_map_out'] = uuid
                    self.map_out_found = True

                if self.map_in_found and self.map_out_found:
                    break

        if map_in_provided and not self.map_in_found:
            self.m.fail_json(
                f"Provided in-route-map '{self.p['route_map_in']}' was not found!"
            )

        if map_out_provided and not self.map_out_found:
            self.m.fail_json(
                f"Provided out-route-map '{self.p['route_map_out']}' was not found!"
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
