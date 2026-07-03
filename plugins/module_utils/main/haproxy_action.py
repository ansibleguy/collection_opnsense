from ansible.module_utils.basic import AnsibleModule

from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.api import Session
from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.module import BaseModule


class HaproxyAction(BaseModule):
    FIELD_ID = 'name'

    CMDS = {
        'add': 'addAction',
        'del': 'delAction',
        'set': 'setAction',
        'search': 'get',
        'toggle': 'toggleAction',
    }
    API_KEY_PATH = 'haproxy.actions.action'
    API_MOD = 'haproxy'
    API_CONT = 'settings'
    API_CONT_REL = 'service'
    API_CMD_REL = 'reconfigure'

    FIELDS_TRANSLATE = {
        'test_type': 'testType',
        'linked_acls': 'linkedAcls',
        'custom_rule': 'custom',
    }

    FIELDS_CHANGE = list(FIELDS_TRANSLATE.keys()) + [
        'name', 'description', 'operator', 'kind',
        'use_backend', 'use_server', 'fcgi_pass_header', 'fcgi_set_param',
        'http_request_auth', 'http_request_redirect', 'http_request_lua',
        'http_request_use_service', 'http_request_add_header_name',
        'http_request_add_header_content', 'http_request_set_header_name',
        'http_request_set_header_content', 'http_request_del_header_name',
        'http_request_replace_header_name', 'http_request_replace_header_regex',
        'http_request_replace_value_name', 'http_request_replace_value_regex',
        'http_request_set_path', 'http_request_set_var_scope',
        'http_request_set_var_name', 'http_request_set_var_expr',
        'http_response_lua', 'http_response_add_header_name',
        'http_response_add_header_content', 'http_response_set_header_name',
        'http_response_set_header_content', 'http_response_del_header_name',
        'http_response_replace_header_name', 'http_response_replace_header_regex',
        'http_response_replace_value_name', 'http_response_replace_value_regex',
        'http_response_set_status_code', 'http_response_set_status_reason',
        'http_response_set_var_scope', 'http_response_set_var_name',
        'http_response_set_var_expr', 'monitor_fail_uri',
        'tcp_request_content_lua', 'tcp_request_content_use_service',
        'tcp_request_inspect_delay', 'tcp_response_content_lua',
        'tcp_response_inspect_delay',
        'map_use_backend_file', 'map_use_backend_default'
    ]
    FIELDS_ALL = FIELDS_CHANGE

    FIELDS_TYPING = {
        "str": [
            "name",
            "description",
            "fcgi_pass_header",
            "fcgi_set_param",
            "http_request_auth",
            "http_request_redirect",
            "http_request_use_service",
            "http_request_add_header_name",
            "http_request_add_header_content",
            "http_request_set_header_name",
            "http_request_set_header_content",
            "http_request_del_header_name",
            "http_request_replace_header_name",
            "http_request_replace_header_regex",
            "http_request_replace_value_name",
            "http_request_replace_value_regex",
            "http_request_set_path",
            "http_request_set_var_name",
            "http_request_set_var_expr",
            "http_response_add_header_name",
            "http_response_add_header_content",
            "http_response_set_header_name",
            "http_response_set_header_content",
            "http_response_del_header_name",
            "http_response_replace_header_name",
            "http_response_replace_header_regex",
            "http_response_replace_value_name",
            "http_response_replace_value_regex",
            "http_response_set_status_reason",
            "http_response_set_var_name",
            "http_response_set_var_expr",
            "monitor_fail_uri",
            "tcp_request_content_use_service",
            "tcp_request_inspect_delay",
            "tcp_response_inspect_delay",
            "custom_rule",
        ],
        "int": ["http_response_set_status_code"],
        "list": ["linked_acls"],
        "select": [
            "test_type",
            "operator",
            "kind",
            "http_request_set_var_scope",
            "http_response_set_var_scope",
            "use_backend",
            "use_server",
            "http_request_lua",
            "http_response_lua",
            "tcp_request_content_lua",
            "tcp_response_content_lua",
            "map_use_backend_file",
            "map_use_backend_default",
        ],
    }
    FIELDS_TRANSLATE = {
        'kind': 'type',
    }
    FIELDS_OPTIONAL = ['linked_acls', 'test_type']

    EXIST_ATTR = 'haproxy_action'

    STR_VALIDATIONS = {
        'name': r'^[^\t^,^;^\.^\[^\]^\{^\}]{1,255}$',
    }

    SEARCH_ADDITIONAL = {
        'existing_acls': 'haproxy.acls.acl',
        'existing_backends': 'haproxy.backends.backend',
        'existing_servers': 'haproxy.servers.server',
        'existing_luas': 'haproxy.luas.lua',
        'existing_mapfiles': 'haproxy.mapfiles.mapfile',
    }

    TIMEOUT = 60.0

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None):
        BaseModule.__init__(self=self, m=module, r=result, s=session)
        self.haproxy_action = {}
        self.existing_acls = {}
        self.existing_backends = {}
        self.existing_servers = {}
        self.existing_luas = {}
        self.existing_mapfiles = {}

    def check(self) -> None:
        self._base_check()
        if self.p['state'] == 'present':
            if self.p.get('linked_acls'):
                self.find_multiple_links(
                    field='linked_acls',
                    existing=self.existing_acls,
                )
            if self.p.get('use_backend'):
                self.find_single_link(
                    field='use_backend',
                    existing=self.existing_backends,
                )
            if self.p.get('use_server'):
                self.find_single_link(
                    field='use_server',
                    existing=self.existing_servers,
                )
            if self.p.get('http_request_lua'):
                self.find_single_link(
                    field='http_request_lua',
                    existing=self.existing_luas,
                )
            if self.p.get('http_response_lua'):
                self.find_single_link(
                    field='http_response_lua',
                    existing=self.existing_luas,
                )
            if self.p.get('tcp_request_content_lua'):
                self.find_single_link(
                    field='tcp_request_content_lua',
                    existing=self.existing_luas,
                )
            if self.p.get('tcp_response_content_lua'):
                self.find_single_link(
                    field='tcp_response_content_lua',
                    existing=self.existing_luas,
                )
            if self.p.get('map_use_backend_file'):
                self.find_single_link(
                    field='map_use_backend_file',
                    existing=self.existing_mapfiles,
                )
            if self.p.get('map_use_backend_default'):
                self.find_single_link(
                    field='map_use_backend_default',
                    existing=self.existing_backends,
                )
