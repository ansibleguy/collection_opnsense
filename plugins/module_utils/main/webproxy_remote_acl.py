from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.cls import BaseModule
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.main import is_unset
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.validate import \
    is_valid_url


class Acl(BaseModule):
    FIELD_ID = 'file'
    CMDS = {
        'add': 'addRemoteBlacklist',
        'set': 'setRemoteBlacklist',
        'del': 'delRemoteBlacklist',
        'search': 'get',
        'toggle': 'toggleRemoteBlacklist',
    }
    API_KEY_PATH = 'proxy.forward.acl.remoteACLs.blacklists.blacklist'
    API_MOD = 'proxy'
    API_CONT = 'settings'
    API_CONT_REL = 'service'
    API_CMD_REL = 'reconfigure'
    FIELDS_CHANGE = [
        'url', 'username', 'password', 'categories', 'verify_ssl',
        'description',
    ]
    FIELDS_ALL = [FIELD_ID]
    FIELDS_ALL.extend(FIELDS_CHANGE)
    FIELDS_TRANSLATE = {
        'file': 'filename',
        'categories': 'filter',
        'verify_ssl': 'sslNoVerify',
    }
    FIELDS_BOOL_INVERT = ['verify_ssl']
    FIELDS_TYPING = {
        'list': ['categories'],
        'bool': ['enabled', 'verify_ssl'],
    }
    STR_VALIDATIONS = {
        'file': r'^[a-zA-Z0-9]{1,245}\.?[a-zA-z0-9]{1,10}$'
    }
    EXIST_ATTR = 'acl'

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None):
        BaseModule.__init__(self=self, m=module, r=result, s=session)
        self.acl = {}

    def check(self) -> None:
        if self.p['state'] == 'present':
            if is_unset(self.p['url']):
                self.m.fail_json('You need to provide an URL to create a remote ACL!')

            if not is_valid_url(self.p['url']):
                self.m.fail_json(f"The provided URL seems to be invalid: '{self.p['url']}'")

            if is_unset(self.p['description']):
                self.m.fail_json('You need to provide a description to create a remote ACL!')

        creds = [self.p['username'] != '', self.p['password'] != '']

        if not all(creds) and any(creds):
            self.m.fail_json(
                "You need to provide both 'username' and 'password' for "
                "authentication to work!"
            )

        self._base_check()
