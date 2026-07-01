from ansible.module_utils.basic import AnsibleModule

from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.oxlorg.opnsense.plugins.module_utils.helper.validate import \
    is_unset
from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.module import BaseModule


class RouteMap(BaseModule):
    CMDS = {
        'add': 'addRoutemap',
        'del': 'delRoutemap',
        'set': 'setRoutemap',
        'search': 'get',
        'toggle': 'toggleRoutemap',
    }
    API_KEY_PATH = 'bgp.routemaps.routemap'
    API_MOD = 'quagga'
    API_CONT = 'bgp'
    API_CONT_REL = 'service'
    FIELDS_CHANGE = [
        'action', 'description', 'id', 'as_path_list', 'prefix_list',
        'community_list', 'set',
    ]
    FIELDS_ALL = ['name', 'enabled']
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
    EXIST_ATTR = 'route_map'
    SEARCH_ADDITIONAL = {
        'existing_paths': 'bgp.aspaths.aspath',
        'existing_prefixes': 'bgp.prefixlists.prefixlist',
        'existing_communities': 'bgp.communitylists.communitylist',
    }

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None, fail: dict = None):
        BaseModule.__init__(self=self, m=module, r=result, s=session, f=fail)
        self.route_map = {}
        self.existing_paths = None
        self.existing_prefixes = None
        self.existing_communities = None

    def check(self) -> None:
        if self.p['state'] == 'present':
            if is_unset(self.p['id']) or is_unset(self.p['action']):
                self.m.fail_json(
                    'To create a BGP route-map you need to provide an ID and action!'
                )

        self._base_check()

        if self.p['state'] == 'present':
            self._find_links()

    def _find_links(self) -> None:
        self.find_multiple_links(
            field='as_path_list',
            existing=self.existing_paths,
            existing_field_id='description',
        )
        self.find_multiple_links(
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
        self.r['diff']['after'][key] = self.p[key]

    def get_existing(self) -> list:
        existing = []

        for entry in self._base_get_existing():
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
