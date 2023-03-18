from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.main import \
    is_true, is_unset
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
                self.m.fail_json(f"Got unsupported command! Available ones are: {', '.join(self.available_commands)}")

    def _simplify_existing(self, job: dict) -> dict:
        simple = job
        simple.pop('origin')
        job['enabled'] = is_true(job['enabled'])

        # to get full list of commands
        init_cmds = False
        if len(self.available_commands) == 0:
            init_cmds = True

        for cmd, cmd_values in job['command'].items():
            if cmd not in self.available_commands:
                self.available_commands.append(cmd)

            if is_true(cmd_values['selected']):
                job['command'] = cmd
                if not init_cmds:
                    break

        return simple
