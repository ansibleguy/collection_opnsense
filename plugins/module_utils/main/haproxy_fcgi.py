from ansible.module_utils.basic import AnsibleModule

from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.api import Session
from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.module import BaseModule


class HaproxyFcgi(BaseModule):
    FIELD_ID = 'name'

    CMDS = {
        'add': 'addFcgi',
        'del': 'delFcgi',
        'set': 'setFcgi',
        'search': 'get',
        'toggle': 'toggleFcgi',
    }
    API_KEY_PATH = 'haproxy.fcgis.fcgi'
    API_MOD = 'haproxy'
    API_CONT = 'settings'
    API_CONT_REL = 'service'
    API_CMD_REL = 'reconfigure'

    FIELDS_TRANSLATE = {
        'linked_actions': 'linkedActions'
    }

    FIELDS_CHANGE = ['enabled', 'name', 'description', 'docroot', 'index', 'path_info',
                     'log_stderr', 'keep_conn', 'get_values', 'mpxs_conns', 'max_reqs', 'linked_actions']
    FIELDS_ALL = FIELDS_CHANGE

    EXIST_ATTR = 'haproxy_fcgi'

    FIELDS_TYPING = {
        'bool': ['enabled', 'log_stderr', 'keep_conn', 'get_values', 'mpxs_conns'],
        'int': ['max_reqs'],
        'list': ['linked_actions']
    }

    STR_VALIDATIONS = {
        'name': r'^[^\t^,^;^\.^\[^\]^\{^\}]{1,255}$',
    }

    INT_VALIDATIONS = {
        'max_reqs': {'min': 1, 'max': 100000},
    }

    SEARCH_ADDITIONAL = {
        'existing_actions': 'haproxy.actions.action',
    }

    TIMEOUT = 20.0

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None):
        BaseModule.__init__(self=self, m=module, r=result, s=session)
        self.haproxy_fcgi = {}
        self.existing_actions = {}

    def check(self) -> None:
        self._base_check()

        if self.p['state'] == 'present':
            self.find_multiple_links(
                field='linked_actions',
                existing=self.existing_actions,
            )
