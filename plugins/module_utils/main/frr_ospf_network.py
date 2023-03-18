from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.main import \
    validate_int_fields, is_ip_or_network
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.cls import BaseModule


class Network(BaseModule):
    CMDS = {
        'add': 'addNetwork',
        'del': 'delNetwork',
        'set': 'setNetwork',
        'search': 'get',
        'toggle': 'toggleNetwork',
    }
    API_KEY = 'network'
    API_KEY_1 = 'ospf'
    API_KEY_2 = 'networks'
    API_MOD = 'quagga'
    API_CONT = 'ospfsettings'
    API_CONT_REL = 'service'
    API_CMD_REL = 'reconfigure'
    FIELDS_CHANGE = ['ip', 'mask', 'area', 'area_range', 'prefix_list_in', 'prefix_list_out']
    FIELDS_ALL = ['enabled']
    FIELDS_ALL.extend(FIELDS_CHANGE)
    FIELDS_TRANSLATE = {
        'ip': 'ipaddr',
        'mask': 'netmask',
        'area_range': 'arearange',
        'prefix_list_in': 'linkedPrefixlistIn',
        'prefix_list_out': 'linkedPrefixlistOut',
    }
    FIELDS_TYPING = {
        'bool': ['enabled'],
        'select': ['prefix_list_in', 'prefix_list_out'],
    }
    INT_VALIDATIONS = {
        'mask': {'min': 0, 'max': 32},
    }
    EXIST_ATTR = 'net'

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None):
        BaseModule.__init__(self=self, m=module, r=result, s=session)
        self.net = {}
        self.existing_paths = None
        self.existing_prefixes = None
        self.existing_communities = None

    def check(self) -> None:
        if self.p['state'] == 'present':
            if self.p['area'] in ['', None]:
                self.m.fail_json(
                    'To create a OSPF network you need to provide an area!'
                )

            if not is_ip_or_network(f"{self.p['ip']}/{self.p['mask']}", strict=True):
                self.m.fail_json(
                    'The combination of the provided ip and network mask is invalid: '
                    f"'{self.p['ip']}/{self.p['mask']}'!"
                )

            validate_int_fields(module=self.m, data=self.p, field_minmax=self.INT_VALIDATIONS)

        self._base_check()
        self.b.find_single_link(
            field='prefix_list_in',
            existing=self.existing_prefixes,
        )
        self.b.find_single_link(
            field='prefix_list_out',
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
            if entry['prefix_list_in'] not in [None, ''] and \
                    entry['prefix_list_in'] in self.existing_prefixes:
                entry['prefix_list_in'] = self.existing_prefixes[entry['prefix_list_in']]['name']

            if entry['prefix_list_out'] not in [None, ''] and \
                    entry['prefix_list_out'] in self.existing_prefixes:
                entry['prefix_list_out'] = self.existing_prefixes[entry['prefix_list_out']]['name']

            existing.append(entry)

        return existing
