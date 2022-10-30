from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.main import \
    is_true, validate_int_fields, get_selected, get_selected_list, validate_str_fields
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.base import Base


class RouteMap:
    FIELD_ID = 'name'
    CMDS = {
        'add': 'addRoutemap',
        'del': 'delRoutemap',
        'set': 'setRoutemap',
        'search': 'get',
        'toggle': 'toggleRoutemap',
    }
    API_KEY = 'routemap'
    API_KEY_1 = 'bgp'
    API_KEY_2 = 'routemaps'
    API_MOD = 'quagga'
    API_CONT = 'bgp'
    API_CONT_REL = 'service'
    API_CMD_REL = 'reconfigure'
    FIELDS_CHANGE = [
        'action', 'description', 'id', 'as_path_list', 'prefix_list',
        'community_list', 'enabled', 'set',
    ]
    FIELDS_ALL = [FIELD_ID]
    FIELDS_ALL.extend(FIELDS_CHANGE)
    FIELDS_TRANSLATE = {
        'as_path_list': 'match',
        'prefix_list': 'match2',
        'community_list': 'match3',
    }
    INT_VALIDATIONS = {
        'id': {'min': 10, 'max': 99},
    }
    STR_VALIDATIONS = {
        'name': r'^[a-zA-Z0-9._-]{1,64}$'
    }
    STR_LEN_VALIDATIONS = {
        'name': {'min': 1, 'max': 64}
    }
    EXIST_ATTR = 'route_map'

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None):
        self.m = module
        self.p = module.params
        self.r = result
        self.s = Session(module=module) if session is None else session
        self.exists = False
        self.route_map = {}
        self.call_cnf = {  # config shared by all calls
            'module': self.API_MOD,
            'controller': self.API_CONT,
        }
        self.b = Base(instance=self)
        self.existing_entries = None
        self.existing_paths = None
        self.existing_prefixes = None
        self.existing_communities = None

    def check(self):
        if self.p['state'] == 'present':
            if self.p['id'] in ['', None] or self.p['action'] in ['', None]:
                self.m.fail_json(
                    'To create a BGP route_map you need to provide a ID and action!'
                )

            validate_str_fields(
                module=self.m, data=self.p,
                field_regex=self.STR_VALIDATIONS,
                field_minmax_length=self.STR_LEN_VALIDATIONS
            )
            validate_int_fields(module=self.m, data=self.p, field_minmax=self.INT_VALIDATIONS)

        self.b.find(match_fields=[self.FIELD_ID])
        self._find_links()
        if self.exists:
            self.call_cnf['params'] = [self.route_map['uuid']]

        if self.p['state'] == 'present':
            self.r['diff']['after'] = self.b.build_diff(data=self.p)

    def process(self):
        self.b.process()

    def _search_call(self) -> dict:
        raw = self.s.get(cnf={
            **self.call_cnf, **{'command': self.CMDS['search']}
        })[self.API_KEY_1]

        self.existing_paths = raw['aspaths']['aspath']
        self.existing_prefixes = raw['prefixlists']['prefixlist']
        self.existing_communities = raw['communitylists']['communitylist']

        return raw[self.API_KEY_2][self.API_KEY]

    @staticmethod
    def _simplify_existing(route_map: dict) -> dict:
        # makes processing easier
        return {
            'name': route_map['name'],
            'id': int(route_map['id']),
            'description': route_map['description'],
            'set': route_map['set'],
            'as_path_list': get_selected_list(route_map['match']),
            'prefix_list': get_selected_list(route_map['match2']),
            'community_list': get_selected_list(route_map['match3']),
            'action': get_selected(route_map['action']),
            'enabled': is_true(route_map['enabled']),
            'uuid': route_map['uuid'],
        }

    def _find_links(self):
        links = {
            'as_path_list': {
                'key': 'description',
                'existing': self.existing_paths,
            },
            'prefix_list': {
                'key': 'name',
                'existing': self.existing_prefixes,
            },
            'community_list': {
                'key': 'description',
                'existing': self.existing_communities,
            },
        }

        for key, values in links.items():
            provided = len(self.p[key]) > 0
            uuids = []

            if len(self.existing_prefixes) > 0 and provided:
                for uuid, entry in values['existing'].items():
                    if entry[values['key']] in self.p[key]:
                        uuids.append(uuid)

                    if len(uuids) == len(self.p[key]):
                        break

            if provided and len(uuids) != len(self.p[key]):
                self.m.fail_json(
                    f"At least one of the provided {key} entries was not found!"
                )

            self.p[key] = uuids

    def get_existing(self) -> list:
        existing = []

        for entry in self.b.get_existing():
            if len(entry['as_path_list']) > 0:
                _list = []
                for path in entry['as_path_list']:
                    if path in self.existing_paths:
                        _list.append(
                            self.existing_paths[path]['description']
                        )

                entry['as_path_list'] = _list

            if len(entry['prefix_list']) > 0:
                _list = []
                for pre in entry['prefix_list']:
                    if pre in self.existing_prefixes:
                        _list.append(
                            self.existing_prefixes[pre]['name']
                        )

                entry['prefix_list'] = _list

            if len(entry['community_list']) > 0:
                _list = []
                for comm in entry['community_list']:
                    if comm in self.existing_communities:
                        _list.append(
                            self.existing_communities[comm]['description']
                        )

                entry['community_list'] = _list

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
