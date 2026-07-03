from ansible.module_utils.basic import AnsibleModule

from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.oxlorg.opnsense.plugins.module_utils.helper.translate import \
    get_selected_list, simplify_translate
from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.module import BaseModule


class SubnetV4(BaseModule):
    CMDS = {
        'add': 'add_subnet',
        'del': 'del_subnet',
        'set': 'set_subnet',
        'search': 'search_subnet',
        'detail': 'get_subnet',
    }
    API_KEY = 'subnet4'
    API_KEY_PATH = 'subnet4'
    API_MOD = 'kea'
    API_CONT = 'dhcpv4'
    API_CONT_REL = 'service'
    FIELDS_ALL = [
        'subnet', 'description', 'pools', 'auto_options', 'next_server',
    ]
    FIELDS_CHANGE = FIELDS_ALL.copy()
    FIELDS_CHANGE.extend([
        'gateway', 'dns', 'domain_search', 'ntp_servers', 'time_servers', 'auto_options', 'v6_only_preferred',
        'routes', 'domain', 'tftp_server', 'tftp_file',
    ])
    FIELDS_TYPING = {
        'list': ['gateway', 'dns', 'domain_search', 'ntp_servers', 'time_servers'],  # 'pools',
        'bool': ['auto_options'],
        'int': ['v6_only_preferred'],
    }
    FIELDS_TRANSLATE = {
        'auto_options': 'option_data_autocollect',
    }
    API_ATTR_OPTIONS = 'option_data'
    API_FIELDS_OPTIONS = [
        'gateway', 'routes', 'dns', 'domain', 'domain_search', 'ntp_servers', 'time_servers',
        'tftp_server', 'tftp_file', 'v6_only_preferred',
    ]
    API_FIELDS_IGNORE = [
        'option_data',
        'option_data.boot_file_name',
        'option_data.classless_static_route',
        'option_data.domain_name',
        'option_data.domain_name_servers',
        'option_data.domain_search',
        'option_data.ntp_servers',
        'option_data.routers',
        'option_data.static_routes',
        'option_data.tftp_server_name',
        'option_data.time_servers',
        'option_data.v4_dnr',
        'option_data.v6_only_preferred',
        'option_data_autocollect',
    ]
    API_FIELDS_IGNORE.extend(API_FIELDS_OPTIONS)
    POOL_JOIN_CHAR = '\n'
    FIELDS_TRANSLATE_SPECIAL = {
        'dns': 'domain_name_servers',
        'domain': 'domain_name',
        'gateway': 'routers',
        'routes': 'static_routes',
        'tftp_server': 'tftp_server_name',
        'tftp_file': 'boot_file_name',
    }
    EXIST_ATTR = 'subnet'

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None, fail: dict = None):
        BaseModule.__init__(self=self, m=module, r=result, s=session, f=fail)
        self.subnet = {}
        self.existing_subnets = None

    def simplify_existing(self, entry: dict) -> dict:
        simple = simplify_translate(
            existing=entry,
            typing=self.FIELDS_TYPING,
            translate=self.FIELDS_TRANSLATE,
            ignore=self.API_FIELDS_IGNORE,
        )

        simple['pools'] = simple['pools'].split(self.POOL_JOIN_CHAR)
        if self.API_ATTR_OPTIONS in entry:
            # get/details call
            opts = entry[self.API_ATTR_OPTIONS]
            return {
                **simple,
                'dns': get_selected_list(opts[self.FIELDS_TRANSLATE_SPECIAL['dns']], remove_empty=True),
                'domain_search': get_selected_list(opts['domain_search'], remove_empty=True),
                'gateway': get_selected_list(opts[self.FIELDS_TRANSLATE_SPECIAL['gateway']], remove_empty=True),
                'routes': opts[self.FIELDS_TRANSLATE_SPECIAL['routes']],
                'domain': opts[self.FIELDS_TRANSLATE_SPECIAL['domain']],
                'ntp_servers': get_selected_list(opts['ntp_servers'], remove_empty=True),
                'time_servers': get_selected_list(opts['time_servers'], remove_empty=True),
                'tftp_server': opts[self.FIELDS_TRANSLATE_SPECIAL['tftp_server']],
                'tftp_file': opts[self.FIELDS_TRANSLATE_SPECIAL['tftp_file']],
                'v6_only_preferred': opts['v6_only_preferred'],
            }

        # search-call :'(
        return {
            **simple,
            'dns': entry[f"option_data.{self.FIELDS_TRANSLATE_SPECIAL['dns']}"],
            'domain_search': entry['option_data.domain_search'],
            'gateway': entry[f"option_data.{self.FIELDS_TRANSLATE_SPECIAL['gateway']}"],
            'routes': entry[f"option_data.{self.FIELDS_TRANSLATE_SPECIAL['routes']}"],
            'domain': entry[f"option_data.{self.FIELDS_TRANSLATE_SPECIAL['domain']}"],
            'ntp_servers': entry['option_data.ntp_servers'],
            'time_servers': entry['option_data.time_servers'],
            'tftp_server': entry[f"option_data.{self.FIELDS_TRANSLATE_SPECIAL['tftp_server']}"],
            'tftp_file': entry[f"option_data.{self.FIELDS_TRANSLATE_SPECIAL['tftp_file']}"],
            'v6_only_preferred': entry['option_data.v6_only_preferred'],
        }

    def build_request(self) -> dict:
        raw_request = self._base_build_request(ignore_fields=self.API_FIELDS_OPTIONS)

        raw_request[self.API_KEY]['pools'] = self.POOL_JOIN_CHAR.join(self.p['pools'])
        raw_request[self.API_KEY][self.API_ATTR_OPTIONS] = {
            self.FIELDS_TRANSLATE_SPECIAL['dns']: self.RESP_JOIN_CHAR.join(self.p['dns']),
            self.FIELDS_TRANSLATE_SPECIAL['gateway']: self.RESP_JOIN_CHAR.join(self.p['gateway']),
            self.FIELDS_TRANSLATE_SPECIAL['routes']: self.p['routes'],
            self.FIELDS_TRANSLATE_SPECIAL['domain']: self.p['domain'],
            self.FIELDS_TRANSLATE_SPECIAL['tftp_server']: self.p['tftp_server'],
            self.FIELDS_TRANSLATE_SPECIAL['tftp_file']: self.p['tftp_file'],
            'ntp_servers': self.RESP_JOIN_CHAR.join(self.p['ntp_servers']),
            'time_servers': self.RESP_JOIN_CHAR.join(self.p['time_servers']),
            'domain_search': self.RESP_JOIN_CHAR.join(self.p['domain_search']),
            'v6_only_preferred': self.p['v6_only_preferred'],
        }

        return raw_request
