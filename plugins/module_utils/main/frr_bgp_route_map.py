from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.main import \
    validate_int_fields, validate_str_fields
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.cls import BaseModule


class RouteMap(BaseModule):
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
        'community_list', 'set',
    ]
    FIELDS_ALL = [FIELD_ID, 'enabled']
    FIELDS_ALL.extend(FIELDS_CHANGE)
    FIELDS_TRANSLATE = {
        'as_path_list': 'match',
        'prefix_list': 'match2',
        'community_list': 'match3',
    }
    FIELDS_TYPING = {
        'bool': ['enabled'],
        'int': ['id'],
        'list': ['as_path_list', 'prefix_list', 'community_list'],
        'select': ['action'],
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
        BaseModule.__init__(self=self, m=module, r=result, s=session)
        self.route_map = {}
        self.existing_paths = None
        self.existing_prefixes = None
        self.existing_communities = None

    def check(self) -> None:
        if self.p['state'] == 'present':
            if self.p['id'] in ['', None] or self.p['action'] in ['', None]:
                self.m.fail_json(
                    'To create a BGP route-map you need to provide an ID and action!'
                )

            validate_str_fields(
                module=self.m, data=self.p,
                field_regex=self.STR_VALIDATIONS,
                field_minmax_length=self.STR_LEN_VALIDATIONS
            )
            validate_int_fields(module=self.m, data=self.p, field_minmax=self.INT_VALIDATIONS)

        self._base_check()
        self._find_links()

    def _search_call(self) -> dict:
        raw = self.s.get(cnf={
            **self.call_cnf, **{'command': self.CMDS['search']}
        })[self.API_KEY_1]

        self.existing_paths = raw['aspaths']['aspath']
        self.existing_prefixes = raw['prefixlists']['prefixlist']
        self.existing_communities = raw['communitylists']['communitylist']

        return raw[self.API_KEY_2][self.API_KEY]

    def _find_links(self) -> None:
        self.b.find_multiple_links(
            field='as_path_list',
            existing=self.existing_paths,
            existing_field_id='description',
        )
        self.b.find_multiple_links(
            field='community_list',
            existing=self.existing_communities,
            existing_field_id='description',
        )

        key = 'prefix_list'
        if len(self.p[key]) > 0:
            uuids = []
            provided_count = 0
            provided_prefixes = {}

            for k, v in self.p[key].items():
                if not isinstance(v, list):
                    v = [v]

                provided_count += len(v)
                provided_prefixes[k] = [int(_v) for _v in v]

            if len(self.existing_prefixes) > 0:
                for uuid, entry in self.existing_prefixes.items():
                    if entry['name'] in provided_prefixes and \
                            int(entry['seqnumber']) in provided_prefixes[entry['name']]:
                        uuids.append(uuid)

            if len(uuids) != provided_count:
                self.m.fail_json(
                    'At least one of the provided prefix-list entries was not found!'
                )

            self.p[key] = uuids

        else:
            self.p[key] = []

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
