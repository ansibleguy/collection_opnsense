from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.main import \
    is_unset
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.cls import BaseModule


class CronJob(BaseModule):
    FIELD_ID = 'description'
    CMDS = {
        'add': 'addJob',
        'del': 'delJob',
        'set': 'setJob',
        'search': 'get',
        'toggle': 'toggleJob',
    }
    API_KEY_PATH = 'job.jobs.job'
    API_MOD = 'cron'
    API_CONT = 'settings'
    API_CONT_REL = 'service'
    API_CMD_REL = 'reconfigure'
    FIELDS_CHANGE = [
        'minutes', 'hours', 'days', 'months',
        'weekdays', 'command', 'who', 'parameters'
    ]
    FIELDS_TYPING = {
        'bool': ['enabled'],
        'select': ['command'],
        'int': ['minutes', 'hours', 'days', 'months', 'weekdays'],
    }
    FIELDS_ALL = ['description', 'enabled']
    FIELDS_ALL.extend(FIELDS_CHANGE)
    EXIST_ATTR = 'cron'

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None):
        BaseModule.__init__(self=self, m=module, r=result, s=session)
        self.cron = {}
        self.available_commands = []

    def check(self) -> None:
        if self.p['state'] == 'present' and is_unset(self.p['command']):
            self.m.fail_json("You need to provide a 'command' if you want to create a cron-job!")

        self.b.find(match_fields=[self.FIELD_ID])

        if self.p['state'] == 'present':
            self.r['diff']['after'] = self.b.build_diff(data=self.p)

            if self.p['command'] is not None and len(self.available_commands) > 0 and \
                    self.p['command'] not in self.available_commands:
                self.m.fail_json(
                    'Got unsupported command! '
                    f"Available ones are: {', '.join(self.available_commands)}"
                )

    def _build_all_available_cmds(self, raw_cmds: dict):
        if len(self.available_commands) == 0:
            for cmd in raw_cmds.keys():
                if cmd not in self.available_commands:
                    self.available_commands.append(cmd)

    def _simplify_existing(self, existing: dict) -> dict:
        # pylint: disable=W0212
        simple = self.b._simplify_existing(existing)
        simple.pop('origin')
        self._build_all_available_cmds(existing['command'])
        return simple
