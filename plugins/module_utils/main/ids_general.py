from ansible.module_utils.basic import AnsibleModule

from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.module import GeneralModule
from ansible_collections.oxlorg.opnsense.plugins.module_utils.helper.translate import \
    get_selected, get_key_by_value_from_selection
from ansible_collections.oxlorg.opnsense.plugins.module_utils.helper.validate import \
    is_ip_or_network, is_unset


class General(GeneralModule):
    CMDS = {
        'set': 'set',
        'search': 'get',
    }
    API_KEY = 'general'
    API_KEY_1 = 'ids'
    API_KEY_PATH = f'{API_KEY_1}.{API_KEY}'
    API_MOD = 'ids'
    API_CONT = 'settings'
    API_CONT_REL = 'service'
    FIELDS_CHANGE = [
        'mode', 'promiscuous', 'enabled', 'interfaces', 'pattern_matcher', 'local_networks', 'default_packet_size',
        'syslog_alerts', 'syslog_output', 'log_level', 'log_rotate', 'log_retention', 'log_payload',
        'profile', 'profile_toclient_groups', 'profile_toserver_groups', 'schedule', 'divert_listeners',
    ]
    FIELDS_ALL = FIELDS_CHANGE
    FIELDS_TRANSLATE = {
        'promiscuous': 'promisc',
        'syslog_alerts': 'syslog',
        'syslog_output': 'syslog_eve',
        'log_level': 'verbosity',
        'pattern_matcher': 'MPMAlgo',
        'local_networks': 'homenet',
        'default_packet_size': 'defaultPacketSize',
        'log_rotate': 'AlertLogrotate',
        'log_retention': 'AlertSaveLogs',
        'log_payload': 'LogPayload',
        'schedule': 'UpdateCron',
    }
    FIELDS_TRANSLATE_SPECIAL = {
        'profile': 'Profile',
        'profile_toclient_groups': 'toclient_groups',
        'profile_toserver_groups': 'toserver_groups',
    }
    FIELDS_TYPING = {
        'bool': ['enabled', 'promiscuous', 'syslog_alerts', 'syslog_output', 'log_payload'],
        'int': ['default_packet_size', 'log_retention', 'divert_listeners'],
        'list': ['local_networks', 'interfaces'],
        'select': ['log_level', 'pattern_matcher', 'log_rotate', 'schedule', 'mode'],
    }
    FIELDS_IGNORE = ['detect']
    INT_VALIDATIONS = {
        'log_retention': {'min': 1, 'max': 1000},
        'profile_toclient_groups': {'min': 1, 'max': 65535},
        'profile_toserver_groups': {'min': 1, 'max': 65535},
        'default_packet_size': {'min': 82, 'max': 65535},
        'divert_listeners': {'min': 1, 'max': 255},
    }
    FIELDS_VALUE_MAPPING = {
        'log_rotate': {
            'weekly': 'W0D23',
            'daily': 'D0',
        },
        'log_level': {
            'info': 'v',
            'perf': 'vv',
            'config': 'vvv',
            'debug': 'vvvv',
        },
    }

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None):
        GeneralModule.__init__(self=self, m=module, r=result, s=session)

    def check(self) -> None:
        if len(self.p['interfaces']) == 0:
            self.m.fail_json("You need to supply 'interfaces'!")

        if self.p['profile'] == 'custom' and (
                is_unset(self.p['profile_toclient_groups']) or is_unset(self.p['profile_toserver_groups'])
        ):
            self.m.fail_json(
                "You need to supply 'profile_toclient_groups' and 'profile_toserver_groups' "
                "when using the profile 'custom'!"
            )

        for net in self.p['local_networks']:
            if not is_ip_or_network(net):
                self.m.fail_json(
                    f"It seems you provided an invalid network in 'local_networks': '{net}'"
                )

        self._base_check()

    def search_call(self) -> dict:
        settings = self.s.get(cnf={
            **self.call_cnf, **{'command': self.CMDS['search']}
        })[self.API_KEY_1][self.API_KEY]

        simple = self.simplify_existing(settings)

        try:
            # resolve schedule/cron name to uuid
            self.p['schedule'] = get_key_by_value_from_selection(
                selection=settings[self.FIELDS_TRANSLATE['schedule']],
                value=self.p['schedule'],
            )

        except KeyError:
            # list module not supplying params
            pass

        simple['profile'] = get_selected(
            settings['detect'][self.FIELDS_TRANSLATE_SPECIAL['profile']]
        )
        simple['profile_toclient_groups'] = settings['detect'][self.FIELDS_TRANSLATE_SPECIAL['profile_toclient_groups']]
        simple['profile_toserver_groups'] = settings['detect'][self.FIELDS_TRANSLATE_SPECIAL['profile_toserver_groups']]

        for field in self.FIELDS_IGNORE:
            if field in simple:
                simple.pop(field)

        return simple

    def build_request(self) -> dict:
        raw_request = self._base_build_request(
            ignore_fields=['profile', 'profile_toclient_groups', 'profile_toserver_groups']
        )
        raw_request[self.API_KEY]['detect'] = {
            self.FIELDS_TRANSLATE_SPECIAL['profile']: self.p['profile'],
            self.FIELDS_TRANSLATE_SPECIAL['profile_toclient_groups']: self.p['profile_toclient_groups'],
            self.FIELDS_TRANSLATE_SPECIAL['profile_toserver_groups']: self.p['profile_toserver_groups'],
        }

        return {self.API_KEY_1: raw_request}
