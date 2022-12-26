from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.cls import BaseModule
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.main import is_unset


class Acl(BaseModule):
    FIELD_ID = 'file'
    CMDS = {
        'add': 'addRemoteBlacklist',
        'set': 'setRemoteBlacklist',
        'del': 'delRemoteBlacklist',
        'search': 'get',
        'toggle': 'toggleRemoteBlacklist',
    }
    API_KEY = 'blacklist'
    API_KEY_PATH = 'proxy.forward.acl.remoteACLs.blacklists'
    REQUEST_NO_API_KEY = True
    API_MOD = 'proxy'
    API_CONT = 'settings'
    API_CONT_REL = 'service'
    API_CMD_REL = 'reconfigure'
    FIELDS_CHANGE = [
        'url', 'username', 'password', 'categories', 'verify_ssl',
        'description',
    ]
    FIELDS_ALL = FIELDS_CHANGE
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
    EXIST_ATTR = 'acl'

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None):
        BaseModule.__init__(self=self, m=module, r=result, s=session)
        self.acl = {}

    def check(self):
        if self.p['state'] == 'present':
            if is_unset(self.p['url']):
                self.m.fail_json('You need to provide an URL to create a remote ACL!')

            if is_unset(self.p['description']):
                self.m.fail_json('You need to provide a description to create a remote ACL!')

        creds = [self.p['username'] != '', self.p['password'] != '']

        if not all(creds) and any(creds):
            self.m.fail_json(
                "You need to provide both 'username' and 'password' for "
                "authentication to work!"
            )

        self.b.find(match_fields=[self.FIELD_ID])
        if self.exists:
            self.call_cnf['params'] = [self.acl['uuid']]

        if self.p['state'] == 'present':
            self.r['diff']['after'] = self.b.build_diff(data=self.p)

    def _build_request(self) -> dict:
        return {self.API_KEY: self.b.build_request()}
