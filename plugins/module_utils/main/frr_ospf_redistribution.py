from ansible.module_utils.basic import AnsibleModule

from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.oxlorg.opnsense.plugins.module_utils.helper.main import is_unset
from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.module import BaseModule


class Redistribution(BaseModule):
    FIELD_ID = 'description'
    CMDS = {
        'add': 'addRedistribution',
        'del': 'delRedistribution',
        'set': 'setRedistribution',
        'search': 'get',
        'toggle': 'toggleRedistribution',
    }
    API_KEY_PATH = 'ospf.redistributions.redistribution'
    API_MOD = 'quagga'
    API_CONT = 'ospfsettings'
    API_CONT_REL = 'service'
    FIELDS_CHANGE = ['redistribute', 'route_map']
    FIELDS_ALL = ['enabled', 'description']
    FIELDS_ALL.extend(FIELDS_CHANGE)
    FIELDS_TRANSLATE = {
        'route_map': 'linkedRoutemap',
    }
    FIELDS_TYPING = {
        'select': ['redistribute', 'route_map',],
    }
    EXIST_ATTR = 'redistribute'
    SEARCH_ADDITIONAL = {
        'existing_maps': 'ospf.routemaps.routemap',
    }

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None, fail: dict = None):
        BaseModule.__init__(self=self, m=module, r=result, s=session, f=fail)
        self.redistribute = {}
        self.existing_maps = None

    def check(self) -> None:
        self._base_check()
        self._find_links()

    def _find_links(self) -> None:
        links = {
            'route-map': {
                'found': False,
                'existing': self.existing_maps,
                'match_fields': {'name': 'route_map'}
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
            if entry['route_map'] not in [None, ''] and \
                    entry['route_map'] in self.existing_maps:
                entry['route_map'] = self.existing_maps[entry['route_map']]['name']

            existing.append(entry)

        return existing
