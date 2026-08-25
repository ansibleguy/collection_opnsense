from ipaddress import ip_network

from ansible.module_utils.basic import AnsibleModule

from ansible_collections.oxlorg.opnsense.plugins.module_utils.helper.main import \
    is_true, to_digit
from ansible_collections.oxlorg.opnsense.plugins.module_utils.helper.translate import \
    simplify_translate
from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.module import BaseModule


class Route(BaseModule):
    FIELD_ID = 'uuid'
    CMDS = {
        'add': 'addroute',
        'del': 'delroute',
        'set': 'setroute',
        'search': 'get',
        'toggle': 'toggleroute',
    }
    API_KEY_PATH = 'route.route'
    API_MOD = 'routes'
    API_CONT = 'routes'
    FIELDS_CHANGE = ['network', 'gateway', 'description']
    FIELDS_ALL = ['enabled']
    FIELDS_ALL.extend(FIELDS_CHANGE)
    FIELDS_TRANSLATE = {
        'description': 'descr',
    }
    FIELDS_TYPING = {
        'bool': ['enabled'],
        'select': ['gateway'],
    }
    EXIST_ATTR = 'route'

    # OPNsense 26.1.10 renamed the static-route model's inverted 'disabled'
    # boolean to a plain 'enabled' one - opnsense/core#10027, which bumped the
    # Routes model from 1.0.0 to 1.0.1 and migrated existing entries. Both
    # serialisations are in the field, so this module can hardcode neither:
    #   * reading  - whichever of the two the API returned is normalised to the
    #                module's 'enabled' semantics, inverting only for 'disabled'.
    #   * writing  - both keys are sent. OPNsense's BaseField::setNodes() walks
    #                its *own* model items and picks the matching keys out of the
    #                payload, so the key the running model does not define is
    #                ignored rather than rejected.
    API_FIELD_ENABLED = 'enabled'
    API_FIELD_DISABLED = 'disabled'

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None, fail: dict = None):
        BaseModule.__init__(self=self, m=module, r=result, s=session, f=fail)
        self.route = {}

    def check(self) -> None:
        try:
            ip_network(self.p['network'])

        except ValueError:
            self.m.fail_json(f"Value '{self.p['network']}' is not a valid network!")

        self._base_check()

    def simplify_existing(self, route: dict) -> dict:
        route = dict(route)

        if self.API_FIELD_ENABLED not in route and self.API_FIELD_DISABLED in route:
            # OPNsense < 26.1.10
            route[self.API_FIELD_ENABLED] = not is_true(route.pop(self.API_FIELD_DISABLED))

        simple = simplify_translate(
            existing=route,
            typing=self.FIELDS_TYPING,
            translate=self.FIELDS_TRANSLATE,
        )
        if simple['gateway'].find(' - ') != -1:
            simple['gateway'] = simple['gateway'].rsplit('-', 1)[0].strip()

        return simple

    def build_request(self) -> dict:
        request = self._base_build_request()
        entry = request[self.API_KEY_PATH.rsplit('.', 1)[1]]
        entry[self.API_FIELD_DISABLED] = to_digit(
            not is_true(entry[self.API_FIELD_ENABLED])
        )
        return request
