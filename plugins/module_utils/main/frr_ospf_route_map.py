from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.main import \
    is_true, validate_int_fields, get_selected, get_selected_list
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
    API_KEY_1 = 'ospf'
    API_KEY_2 = 'routemaps'
    API_MOD = 'quagga'
    API_CONT = 'ospfsettings'
    API_CONT_REL = 'service'
    API_CMD_REL = 'reconfigure'
    FIELDS_CHANGE = ['action', 'id', 'prefix_list', 'set']
    FIELDS_ALL = [FIELD_ID, 'enabled']
    FIELDS_ALL.extend(FIELDS_CHANGE)
    FIELDS_TRANSLATE = {
        'prefix_list': 'match2',
    }
    INT_VALIDATIONS = {
        'id': {'min': 10, 'max': 99},
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
                    'To create a OSPF route-map you need to provide an ID and action!'
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

        self.existing_prefixes = raw['prefixlists']['prefixlist']
        return raw[self.API_KEY_2][self.API_KEY]

    @staticmethod
    def _simplify_existing(route_map: dict) -> dict:
        # makes processing easier
        return {
            'name': route_map['name'],
            'id': int(route_map['id']),
            'set': route_map['set'],
            'prefix_list': get_selected_list(route_map['match2'], remove_empty=True),
            'action': get_selected(route_map['action']),
            'enabled': is_true(route_map['enabled']),
            'uuid': route_map['uuid'],
        }

    def _find_links(self):
        links = {
            'prefix_list': {
                'key': 'name',
                'existing': self.existing_prefixes,
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
            if len(entry['prefix_list']) > 0:
                _list = []
                for pre in entry['prefix_list']:
                    if pre in self.existing_prefixes:
                        _list.append(
                            self.existing_prefixes[pre]['name']
                        )

                entry['prefix_list'] = _list

            existing.append(entry)

        return existing

    def create(self):
        self.b.create()

    def update(self):
        self.b.update()

    def delete(self):
        self.b.delete()

    def reload(self):
        self.b.reload()
