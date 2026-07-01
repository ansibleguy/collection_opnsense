from ansible.module_utils.basic import AnsibleModule

from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.oxlorg.opnsense.plugins.module_utils.helper.main import \
    is_unset
from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.module import BaseModule


class DhcRelayRelay(BaseModule):
    FIELD_ID = 'interface'
    CMDS = {
        'add': 'add_relay',
        'del': 'del_relay',
        'set': 'set_relay',
        'search': 'get',
        'toggle': 'toggle_relay',
    }
    API_KEY_PATH = 'dhcrelay.relays'
    API_KEY_PATH_REQ = 'relay'
    API_MOD = 'dhcrelay'
    API_CONT = 'settings'
    API_CONT_REL = 'service'
    FIELDS_CHANGE = ['destination', 'agent_info']
    FIELDS_ALL = [FIELD_ID, 'enabled']
    FIELDS_ALL.extend(FIELDS_CHANGE)
    FIELDS_TYPING = {
        'select': ['interface', 'destination'],
        'bool': ['enabled', 'agent_info']
    }
    EXIST_ATTR = 'relay'
    SEARCH_ADDITIONAL = {
        'existing_destinations': 'dhcrelay.destinations',
    }

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None, fail: dict = None):
        BaseModule.__init__(self=self, m=module, r=result, s=session, f=fail)
        self.relay = {}
        self.existing_destinations = None

    def check(self) -> None:
        if self.p['state'] == 'present':
            if is_unset(self.p['destination']):
                self.m.fail_json("You need to provide a 'destination' to create a dhcrelay_relay!")

        self._base_check()

        if not is_unset(self.p['destination']) and self.existing_destinations:
            for key, values in self.existing_destinations.items():
                if values['name'] == self.p['destination']:
                    self.p['destination'] = key
                    break

    def get_existing(self) -> list:
        existing = self._base_get_existing()
        for relay in existing:
            relay['destination'] = self.existing_destinations[relay['destination']]['name']
        return existing
