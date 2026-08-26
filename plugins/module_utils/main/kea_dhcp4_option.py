from ansible.module_utils.basic import AnsibleModule

from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.module import BaseModule
from ansible_collections.oxlorg.opnsense.plugins.module_utils.helper.validate import \
    is_unset


class Dhcpv4Option(BaseModule):
    CMDS = {
        'add': 'add_option',
        'del': 'del_option',
        'set': 'set_option',
        'search': 'search_option',
        'detail': 'get_option',
    }
    API_KEY_PATH = 'option'
    API_MOD = 'kea'
    API_CONT = 'dhcpv4'
    API_CONT_REL = 'service'
    FIELDS_CHANGE = [
        'code', 'encoding', 'data', 'force', 'match_code', 'match_encoding',
        'match_data', 'description',
    ]
    FIELDS_ALL = FIELDS_CHANGE
    FIELDS_TYPING = {
        'bool': ['force'],
        # the API returns these four as select-lists, not as plain values
        'select': ['code', 'encoding', 'match_code', 'match_encoding'],
    }
    EXIST_ATTR = 'option'

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None, fail: dict = None):
        BaseModule.__init__(self=self, m=module, r=result, s=session, f=fail)
        self.option = {}
        self.existing_options = None

    def check(self) -> None:
        if self.p['state'] == 'present':
            if is_unset(self.p['code']):
                self.m.fail_json("You need to provide a 'code' if you want to create a DHCPv4 option!")

            if is_unset(self.p['data']):
                self.m.fail_json("You need to provide 'data' if you want to create a DHCPv4 option!")

            if is_unset(self.p['description']):
                self.m.fail_json("You need to provide a 'description' if you want to create a DHCPv4 option!")

            match_code_set = not is_unset(self.p['match_code'])
            match_data_set = not is_unset(self.p['match_data'])
            if match_code_set != match_data_set:
                self.m.fail_json("'match_code' and 'match_data' must either both be set or both be empty!")

            if match_data_set and is_unset(self.p['match_encoding']):
                self.m.fail_json("You need to provide 'match_encoding' when 'match_data' is set!")

        self._base_check()
