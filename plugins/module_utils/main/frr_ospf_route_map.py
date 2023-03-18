from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.main import \
    validate_int_fields
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
    FIELDS_TYPING = {
        'bool': ['enabled'],
        'list': ['prefix_list'],
        'select': ['action'],
        'int': ['id'],
    }
    INT_VALIDATIONS = {
        'id': {'min': 10, 'max': 99},
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
                    'To create a OSPF route-map you need to provide an ID and action!'
                )

            validate_int_fields(module=self.m, data=self.p, field_minmax=self.INT_VALIDATIONS)

        self._base_check()
        self.b.find_multiple_links(
            field='prefix_list',
            existing=self.existing_prefixes,
        )

    def _search_call(self) -> dict:
        raw = self.s.get(cnf={
            **self.call_cnf, **{'command': self.CMDS['search']}
        })[self.API_KEY_1]

        self.existing_prefixes = raw['prefixlists']['prefixlist']
        return raw[self.API_KEY_2][self.API_KEY]

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
