from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.main import \
    validate_int_fields, is_ip, is_unset
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.cls import GeneralModule


class Parent(GeneralModule):
    CMDS = {
        'set': 'set',
        'search': 'get',
    }
    API_KEY_PATH = 'proxy.general.parentproxy'
    API_KEY_PATH_REQ = API_KEY_PATH
    API_MOD = 'proxy'
    API_CONT = 'settings'
    API_CONT_REL = 'service'
    API_CMD_REL = 'reconfigure'
    FIELDS_CHANGE = [
        'host', 'auth', 'user', 'password', 'port', 'local_domains', 'local_ips',
        'enabled',
    ]
    FIELDS_ALL = FIELDS_CHANGE
    FIELDS_TRANSLATE = {
        'auth': 'enableauth',
        'local_domains': 'localdomains',
        'local_ips': 'localips',
    }
    FIELDS_TYPING = {
        'bool': ['enabled', 'auth'],
        'list': ['local_domains', 'local_ips'],
        'int': ['port'],
    }
    INT_VALIDATIONS = {
        'port': {'min': 1, 'max': 65535},
    }
    STR_VALIDATIONS = {
        'user': r'^([0-9a-zA-Z\._\-]){1,32}$',
        'password': r'^([0-9a-zA-Z\._\-]){1,32}$',
    }
    FIELDS_DIFF_NO_LOG = ['password']

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None):
        GeneralModule.__init__(self=self, m=module, r=result, s=session)

    def check(self) -> None:
        # pylint: disable=W0201
        if self.p['enabled']:
            if is_unset(self.p['host']) or is_unset(self.p['port']):
                self.m.fail_json('To enable a parent proxy, a host and port must be provided!')

            if not is_ip(self.p['host']):
                self.m.fail_json(f"Provided host '{self.p['host']}' is not a valid IP-Address!")

        validate_int_fields(module=self.m, data=self.p, field_minmax=self.INT_VALIDATIONS)

        self.settings = self._search_call()
        self._build_diff()
