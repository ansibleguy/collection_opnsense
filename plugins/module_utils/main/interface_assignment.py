from ansible.module_utils.basic import AnsibleModule

from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.oxlorg.opnsense.plugins.module_utils.helper.validate import \
    is_unset
from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.module import BaseModule


class Assignment(BaseModule):
    FIELD_ID = 'identifier'
    CMDS = {
        'add': 'add_item',
        'del': 'del_item',
        'set': 'set_item',
        'search': 'search_item',
        'detail': 'get_item',
    }
    API_KEY_PATH = 'interface'
    API_MOD = 'interfaces'
    API_CONT = 'assignment'
    FIELDS_CHANGE = ['description', 'device', 'lock']
    FIELDS_ALL = [FIELD_ID]
    FIELDS_ALL.extend(FIELDS_CHANGE)
    FIELDS_TRANSLATE = {
        'device': 'if',
        'description': 'descr',
    }
    FIELDS_TYPING = {
       'str': ['device', 'description', 'identifier'],
       'bool': ['lock'],
    }
    EXIST_ATTR = 'assignment'

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None, fail: dict = None):
        BaseModule.__init__(self=self, m=module, r=result, s=session, f=fail)
        self.assignment = {}

    @staticmethod
    def get_selected_device(assignment) -> str:
        for device, details in assignment.get('device', {}).items():
            if details.get('selected') == 1:
                return device
        return None

    def check(self) -> None:
        if self.p['state'] == 'present':
            # We dont provide an identifier on creation, so we
            # need to first check if the device is already in use
            # and if it is we use the previous defined identifier
            if is_unset(self.p['identifier']):

                # If we dont have the identifier set, we need the device
                if is_unset(self.p['device']):
                    self.m.fail_json("You need to provide a 'device' to assign the interface!")

                # Get the exisiting assignments, loop through and
                # find the if there is a matching device if there
                # is then we aquire thats identitier
                existing = self.get_existing()
                for assignment in existing:
                    device = self.get_selected_device(assignment)
                    if device == self.p['device']:
                        self.p['identifier'] = assignment['identifier']
                        break

                # If there isnt and exisiting assignment
                # and the lock is not set then set it to
                # a default
                if is_unset(self.p['identifier']) and is_unset(self.p['lock']):
                    self.p['lock'] = 1

        elif self.p['state'] == 'absent':

            # we need to have the identifier set to remove
            if is_unset(self.p['identifier']):
                self.m.fail_json("You need to provide a 'identifier' to delete an assigned interface!")

            # Get the exisiting assignments, loop through and
            # find the identitier if check if the device is not
            # locked
            existing = self.get_existing()
            for assignment in existing:
                if assignment['identifier'] != self.p['identifier']:
                    continue
                if assignment['lock']:
                    self.m.fail_json("You need to unlock the interface before you delete an assigned interface!")

        self._base_check()

    def update(self) -> None:

        # check if any of the parameters have not been provided
        # and if not use the exisiting parameters
        if is_unset(self.p['description']):
            self.p['description'] = self.e['description']

        if is_unset(self.p['device']):
            self.p['device'] = self.get_selected_device(self.e)

        if is_unset(self.p['lock']):
            self.p['lock'] = self.e['lock']

        # parse the selected device, so it can be compared
        self.e['device'] = self.get_selected_device(self.e)
        self._base_update(enable_switch=False)
