from ansible.module_utils.basic import AnsibleModule

from ansible_collections.oxlorg.opnsense.plugins.module_utils.helper.main import \
    is_unset
from ansible_collections.oxlorg.opnsense.plugins.module_utils.helper.validate import \
    is_valid_domain
from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.module import BaseModule


class Host(BaseModule):
    FIELD_ID = 'description'
    CMDS = {
        'add': 'add_host',
        'del': 'del_host',
        'set': 'set_host',
        'search': 'get',
    }
    API_KEY_PATH = 'dnsmasq.hosts'
    API_KEY_PATH_REQ = 'host'
    API_MOD = 'dnsmasq'
    API_CONT = 'settings'
    API_CONT_REL = 'service'
    FIELDS_CHANGE = [
        'host', 'domain', 'local', 'ip', 'aliases', 'cnames', 'client_id', 'hardware_addr', 'lease_time', 'ignore',
        'set_tag', 'comments',
    ]
    FIELDS_TRANSLATE = {
        'description': 'descr',
        'hardware_addr': 'hwaddr',
    }
    FIELDS_TYPING = {
        'list': ['ip', 'aliases', 'cnames', 'hardware_addr'],
        'select': ['set_tag'],
        'bool': ['local', 'ignore'],
        'int': ['lease_time'],
    }
    FIELDS_ALL = [FIELD_ID]
    FIELDS_ALL.extend(FIELDS_CHANGE)
    EXIST_ATTR = 'host'
    SEARCH_ADDITIONAL = {
        'existing_tag': 'dnsmasq.dhcp_tags',
    }

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None):
        BaseModule.__init__(self=self, m=module, r=result, s=session)
        self.host = {}
        self.existing_tag = {}

    def check(self) -> None:
        if not is_unset(self.p['domain']) and not is_valid_domain(self.p['domain']):
            self.m.fail_json(
                f"Value of domain '{self.p['domain']}' is not a valid domain-name!"
            )

        self._base_check()

        if self.p['state'] == 'present':
            self.find_single_link(
                field='set_tag',
                existing=self.existing_tag,
                existing_field_id='tag',
            )
