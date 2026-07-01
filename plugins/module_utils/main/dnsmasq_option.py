from ansible.module_utils.basic import AnsibleModule

from ansible_collections.oxlorg.opnsense.plugins.module_utils.helper.main import \
    is_unset
from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.module import BaseModule


class Option(BaseModule):
    FIELD_ID = 'description'
    CMDS = {
        'add': 'add_option',
        'del': 'del_option',
        'set': 'set_option',
        'search': 'get',
    }
    API_KEY_PATH = 'dnsmasq.dhcp_options'
    API_KEY_PATH_REQ = 'option'
    API_MOD = 'dnsmasq'
    API_CONT = 'settings'
    API_CONT_REL = 'service'
    FIELDS_CHANGE = ['type', 'option', 'option6', 'interface', 'tag', 'set_tag', 'value', 'force']
    FIELDS_TYPING = {
        'select': ['type', 'option', 'option6', 'interface', 'set_tag'],
        'list': ['tag'],
        'bool': ['force'],
    }
    FIELDS_ALL = [FIELD_ID]
    FIELDS_ALL.extend(FIELDS_CHANGE)
    EXIST_ATTR = 'option'
    SEARCH_ADDITIONAL = {
        'existing_tag': 'dnsmasq.dhcp_tags',
        'existing_interface': 'dnsmasq.interface',
    }

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None):
        BaseModule.__init__(self=self, m=module, r=result, s=session)
        self.option = {}
        self.existing_tag = {}
        self.existing_interface = {}

    def check(self) -> None:
        if self.p['state'] == 'present' and self.p['type'] == 'match':
            if is_unset(self.p['set_tag']):
                self.m.fail_json("When type is 'match', a set_tag must be set.")
            if not is_unset(self.p['interface']):
                self.m.fail_json("When type is 'match', no internet can be set.")
            if not is_unset(self.p['tag']):
                self.m.fail_json("When type is 'match', no tag can be set.")

        self._base_check()

        if self.p['state'] == 'present':
            self.find_single_link(
                field='interface',
                existing=self.existing_interface,
                existing_field_id='value',
            )
            self.find_single_link(
                field='set_tag',
                existing=self.existing_tag,
                existing_field_id='tag',
            )
            self.find_multiple_links(
                field='tag',
                existing_field_id='tag',
                existing=self.existing_tag,
                fail_soft=True, fail=False,
            )
