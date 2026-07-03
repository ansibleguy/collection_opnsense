from ipaddress import ip_network

from ansible.module_utils.basic import AnsibleModule

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
        simple = simplify_translate(
            existing=route,
            typing=self.FIELDS_TYPING,
            translate=self.FIELDS_TRANSLATE,
        )
        if simple['gateway'].find(' - ') != -1:
            simple['gateway'] = simple['gateway'].rsplit('-', 1)[0].strip()

        return simple
