from ansible.module_utils.basic import AnsibleModule

from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.api import Session
from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.module import BaseModule
from ansible_collections.oxlorg.opnsense.plugins.module_utils.helper.validate import is_unset


class HaproxyAcl(BaseModule):
    FIELD_ID = 'name'

    CMDS = {
        'add': 'addAcl',
        'del': 'delAcl',
        'set': 'setAcl',
        'search': 'get',
        'toggle': 'toggleAcl',
    }
    API_KEY_PATH = 'haproxy.acls.acl'
    API_MOD = 'haproxy'
    API_CONT = 'settings'
    API_CONT_REL = 'service'
    API_CMD_REL = 'reconfigure'

    FIELDS_TRANSLATE = {
        'case_sensitive': 'caseSensitive',
        'allowed_users': 'allowedUsers',
        'allowed_groups': 'allowedGroups',
    }

    FIELDS_CHANGE = list(FIELDS_TRANSLATE.keys()) + [
        'name', 'description', 'expression', 'negate',
        'hdr_beg', 'hdr_end', 'hdr', 'hdr_reg', 'hdr_sub',
        'path_beg', 'path_end', 'path', 'path_reg', 'path_dir', 'path_sub',
        'cust_hdr_beg_name', 'cust_hdr_beg', 'cust_hdr_end_name', 'cust_hdr_end',
        'cust_hdr_name', 'cust_hdr', 'cust_hdr_reg_name', 'cust_hdr_reg',
        'cust_hdr_sub_name', 'cust_hdr_sub', 'url_param', 'url_param_value',
        'ssl_c_verify_code', 'ssl_c_ca_commonname', 'ssl_hello_type',
        'src', 'src_port', 'src_port_comparison', 'nbsrv', 'nbsrv_backend',
        'ssl_fc_sni', 'ssl_sni', 'ssl_sni_sub', 'ssl_sni_beg',
        'ssl_sni_end', 'ssl_sni_reg', 'custom_acl',
        'src_bytes_in_rate_comparison', 'src_bytes_in_rate',
        'src_bytes_out_rate_comparison', 'src_bytes_out_rate',
        'src_conn_cnt_comparison', 'src_conn_cnt',
        'src_conn_cur_comparison', 'src_conn_cur',
        'src_conn_rate_comparison', 'src_conn_rate',
        'src_http_err_cnt_comparison', 'src_http_err_cnt',
        'src_http_err_rate_comparison', 'src_http_err_rate',
        'src_http_req_cnt_comparison', 'src_http_req_cnt',
        'src_http_req_rate_comparison', 'src_http_req_rate',
        'src_kbytes_in_comparison', 'src_kbytes_in',
        'src_kbytes_out_comparison', 'src_kbytes_out',
        'src_sess_cnt_comparison', 'src_sess_cnt',
        'src_sess_rate_comparison', 'src_sess_rate'
    ]
    FIELDS_ALL = FIELDS_CHANGE

    FIELDS_TYPING = {
        'str': ['name', 'description', 'hdr_beg', 'hdr_end', 'hdr', 'hdr_reg', 'hdr_sub',
                'path_beg', 'path_end', 'path', 'path_reg', 'path_dir', 'path_sub',
                'cust_hdr_beg_name', 'cust_hdr_beg', 'cust_hdr_end_name', 'cust_hdr_end',
                'cust_hdr_name', 'cust_hdr', 'cust_hdr_reg_name', 'cust_hdr_reg',
                'cust_hdr_sub_name', 'cust_hdr_sub', 'url_param', 'url_param_value',
                'ssl_c_ca_commonname', 'src', 'ssl_fc_sni', 'ssl_sni', 'ssl_sni_sub',
                'ssl_sni_beg', 'ssl_sni_end', 'ssl_sni_reg', 'custom_acl'],
        'bool': ['negate', 'case_sensitive'],
        'int': ['ssl_c_verify_code', 'src_port', 'nbsrv', 'src_bytes_in_rate', 'src_bytes_out_rate',
                'src_conn_cnt', 'src_conn_cur', 'src_conn_rate', 'src_http_err_cnt', 'src_http_err_rate',
                'src_http_req_cnt', 'src_http_req_rate', 'src_kbytes_in', 'src_kbytes_out',
                'src_sess_cnt', 'src_sess_rate'],
        'list': ['allowed_users', 'allowed_groups'],
        'select': ['expression', 'ssl_hello_type', 'nbsrv_backend', 'src_port_comparison',
                   'src_bytes_in_rate_comparison', 'src_bytes_out_rate_comparison', 'src_conn_cnt_comparison',
                   'src_conn_cur_comparison', 'src_conn_rate_comparison', 'src_http_err_cnt_comparison',
                   'src_http_err_rate_comparison', 'src_http_req_cnt_comparison', 'src_http_req_rate_comparison',
                   'src_kbytes_in_comparison', 'src_kbytes_out_comparison', 'src_sess_cnt_comparison',
                   'src_sess_rate_comparison']
    }

    EXIST_ATTR = 'haproxy_acl'

    STR_VALIDATIONS = {
        'name': r'^[^\t^,^;^\.^\[^\]^\{^\}]{1,255}$',
    }

    SEARCH_ADDITIONAL = {
        'existing_users': 'haproxy.users.user',
        'existing_groups': 'haproxy.groups.group',
        'existing_backends': 'haproxy.backends.backend',
    }

    TIMEOUT = 60.0

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None):
        BaseModule.__init__(self=self, m=module, r=result, s=session)
        self.haproxy_acl = {}
        self.existing_users = {}
        self.existing_groups = {}
        self.existing_backends = {}

    def check(self) -> None:
        self._base_check()

        if self.p['state'] == 'present':
            if is_unset(self.p['expression']):
                self.m.fail_json("You need to provide an 'expression' to create an ACL!")

            if self.p.get('allowed_users'):
                self.find_multiple_links(
                    field='allowed_users',
                    existing=self.existing_users,
                    existing_field_id='name',
                )
            if self.p.get('allowed_groups'):
                self.find_multiple_links(
                    field='allowed_groups',
                    existing=self.existing_groups,
                    existing_field_id='name',
                )
            if self.p.get('nbsrv_backend'):
                self.find_single_link(
                    field='nbsrv_backend',
                    existing=self.existing_backends,
                    existing_field_id='name',
                )
