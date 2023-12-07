from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.cls import GeneralModule
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.main import \
    get_selected, is_ip_or_network, is_unset, validate_int_fields, get_key_by_value_from_selection


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
    API_CMD_REL = 'reconfigure'
    FIELDS_CHANGE = [
        'block', 'promiscuous', 'enabled', 'interfaces', 'pattern_matcher', 'local_networks', 'default_packet_size',
        'syslog_alerts', 'syslog_output', 'log_level', 'log_rotate', 'log_retention', 'log_payload',
        'profile', 'profile_toclient_groups', 'profile_toserver_groups', 'schedule',
    ]
    FIELDS_ALL = FIELDS_CHANGE
    FIELDS_TRANSLATE = {
        'block': 'ips',
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
        'bool': ['enabled', 'block', 'promiscuous', 'syslog_alerts', 'syslog_output', 'log_payload'],
        'int': ['default_packet_size', 'log_retention'],
        'list': ['local_networks', 'interfaces'],
        'select': ['log_level', 'pattern_matcher', 'log_rotate', 'schedule'],
    }
    FIELDS_IGNORE = ['detect']
    INT_VALIDATIONS = {
        'log_retention': {'min': 1, 'max': 1000},
        'profile_toclient_groups': {'min': 1, 'max': 65535},
        'profile_toserver_groups': {'min': 1, 'max': 65535},
        'default_packet_size': {'min': 82, 'max': 65535},
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
        # pylint: disable=W0201
        validate_int_fields(module=self.m, data=self.p, field_minmax=self.INT_VALIDATIONS)

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

        self.settings = self._search_call()
        self._build_diff()

    def _search_call(self) -> dict:
        settings = self.s.get(cnf={
            **self.call_cnf, **{'command': self.CMDS['search']}
        })[self.API_KEY_1][self.API_KEY]

        simple = self.b._simplify_existing(settings)

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

    def _build_request(self) -> dict:
        raw_request = self.b.build_request(
            ignore_fields=['profile', 'profile_toclient_groups', 'profile_toserver_groups']
        )
        raw_request[self.API_KEY]['detect'] = {
            self.FIELDS_TRANSLATE_SPECIAL['profile']: self.p['profile'],
            self.FIELDS_TRANSLATE_SPECIAL['profile_toclient_groups']: self.p['profile_toclient_groups'],
            self.FIELDS_TRANSLATE_SPECIAL['profile_toserver_groups']: self.p['profile_toserver_groups'],
        }

        return {self.API_KEY_1: raw_request}

