from ansible.module_utils.basic import AnsibleModule

from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.module import BaseModule


class Boot(BaseModule):
    FIELD_ID = 'description'
    CMDS = {
        'add': 'add_boot',
        'del': 'del_boot',
        'set': 'set_boot',
        'search': 'get',
    }
    API_KEY_PATH = 'dnsmasq.dhcp_boot'
    API_KEY_PATH_REQ = 'boot'
    API_MOD = 'dnsmasq'
    API_CONT = 'settings'
    API_CONT_REL = 'service'
    FIELDS_CHANGE = ['address', 'filename', 'interface', 'servername', 'tag']
    FIELDS_TYPING = {
        'select': ['interface'],
        'list': ['tag'],
    }
    FIELDS_ALL = [FIELD_ID]
    FIELDS_ALL.extend(FIELDS_CHANGE)
    EXIST_ATTR = 'boot'
    SEARCH_ADDITIONAL = {
        'existing_tag': 'dnsmasq.dhcp_tags',
        'existing_interface': 'dnsmasq.interface',
    }

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None):
        BaseModule.__init__(self=self, m=module, r=result, s=session)
        self.boot = {}
        self.existing_tag = {}
        self.existing_interface = {}

    def check(self) -> None:
        self._base_check()

        if self.p['state'] == 'present':
            self.find_single_link(
                field='interface',
                existing=self.existing_interface,
                existing_field_id='value',
            )
            self.find_multiple_links(
                field='tag',
                existing_field_id='tag',
                existing=self.existing_tag,
                fail_soft=True, fail=False,
            )
