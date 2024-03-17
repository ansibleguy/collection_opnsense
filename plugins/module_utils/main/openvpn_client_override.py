from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.main import \
    is_unset, get_key_by_value_beg_from_selection
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.cls import BaseModule


class Override(BaseModule):
    FIELD_ID = 'name'
    CMDS = {
        'add': 'add',
        'del': 'del',
        'set': 'set',
        'toggle': 'toggle',
        'search': 'search',
        'detail': 'get',
    }
    API_KEY_PATH = 'cso'
    API_MOD = 'openvpn'
    API_CONT = 'client_overwrites'
    API_CONT_REL = 'service'
    API_CMD_REL = 'reconfigure'
    FIELDS_CHANGE = [
        'servers', 'description', 'block', 'push_reset', 'network_tunnel_ip4', 'network_tunnel_ip6',
        'network_local', 'network_remote', 'route_gateway', 'redirect_gateway', 'register_dns',
        'domain', 'domain_list', 'dns_servers', 'ntp_servers', 'wins_servers',
    ]
    FIELDS_ALL = ['enabled', FIELD_ID]
    FIELDS_ALL.extend(FIELDS_CHANGE)
    FIELDS_TRANSLATE = {
        'name': 'common_name',
        'network_tunnel_ip4': 'tunnel_network',
        'network_tunnel_ip6': 'tunnel_networkv6',
        'network_local': 'local_networks',
        'network_remote': 'remote_networks',
        'domain': 'dns_domain',
        'domain_list': 'dns_domain_search',
    }
    FIELDS_TYPING = {
        'bool': ['enabled', 'block', 'push_reset', 'register_dns'],
        'list': [
            'servers', 'redirect_gateway', 'network_local', 'network_remote', 'domain_list',
            'dns_servers', 'ntp_servers', 'wins_servers',
        ],
    }
    EXIST_ATTR = 'override'

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None):
        BaseModule.__init__(self=self, m=module, r=result, s=session)
        self.override = {}

    def check(self) -> None:
        if self.p['state'] == 'present':
            if is_unset(self.p['servers']):
                self.m.fail_json("You need to provide at least one 'servers' to create an Client-Overwrite!")

        self._base_check()

        if not is_unset(self.p['servers']):
            servers = []
            for server in self.p['servers']:
                servers.append(get_key_by_value_beg_from_selection(
                    selection=self.b.raw['servers'],
                    value=server,
                ))

            self.p['servers'] = servers

        if self.p['state'] == 'present':
            self.r['diff']['after'] = self.b.build_diff(data=self.p)
