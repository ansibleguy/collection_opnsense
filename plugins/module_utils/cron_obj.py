from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper import \
    is_true, to_digit, get_matching, get_simple_existing
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.api import \
    Session


class CronJob:
    FIELD_ID = 'description'
    CMDS = {
        'add': 'addJob',
        'del': 'delJob',
        'set': 'setJob',
        'search': 'get',
        'toggle': 'toggleJob',
    }
    API_KEY = 'job'
    API_MOD = 'cron'
    API_CONT = 'settings'
    API_CONT_REL = 'service'

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None):
        self.m = module
        self.p = module.params
        self.r = result
        self.s = Session(module=module) if session is None else session
        self.exists = False
        self.cron = {}
        self.call_cnf = {  # config shared by all calls
            'module': self.API_MOD,
            'controller': self.API_CONT,
        }
        self.existing_jobs = None
        self.available_commands = []

    def process(self):
        if self.p['state'] == 'absent':
            if self.exists:
                self.delete()

        else:
            if self.exists:
                self.update()

            else:
                self.create()

    def check(self):
        # basic validation of conditional parameters
        if self.p['state'] == 'present' and self.p['command'] is None:
            self.m.fail_json("You need to provide a 'command' if you want to create a cron-job!")

        # checking if item exists
        self._find_cron()
        if self.exists:
            self.call_cnf['params'] = [self.cron['uuid']]
            self.r['diff']['after'] = self._build_diff_after()

        if self.p['command'] is not None and len(self.available_commands) > 0 and \
                self.p['command'] not in self.available_commands:
            self.m.fail_json(f"Got unsupported command! Available ones are: {', '.join(self.available_commands)}")

    def _find_cron(self):
        if self.existing_jobs is None:
            self.existing_jobs = self._search_call()

        match = get_matching(
            module=self.m, existing_items=self.existing_jobs,
            compare_item=self.p, match_fields=[self.FIELD_ID],
            simplify_func=self._simplify_existing,
        )

        if match is not None:
            self.cron = match
            self.r['diff']['before'] = self.cron
            self.exists = True

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

    def get_existing(self) -> list:
        return get_simple_existing(
            entries=self._search_call(),
            simplify_func=self._simplify_existing
        )

    def _search_call(self) -> dict:
        return self.s.get(cnf={
            **self.call_cnf, **{'command': self.CMDS['search']}
        })['job']['jobs']['job']

    def create(self):
        self.r['changed'] = True

        if not self.m.check_mode:
            self.s.post(cnf={
                **self.call_cnf, **{
                    'command': self.CMDS['add'],
                    'data': self._build_request(),
                }
            })

    def update(self):
        # checking if changed
        for field in ['enabled', 'minutes', 'hours', 'days', 'months',
                      'weekdays', 'command', 'who', 'parameters']:
            if str(self.cron[field]) != str(self.p[field]):
                self.r['changed'] = True
                break

        # update if changed
        if self.r['changed'] and not self.m.check_mode:
            self.s.post(cnf={
                **self.call_cnf, **{
                    'command': self.CMDS['set'],
                    'data': self._build_request(),
                }
            })

            if self.p['debug']:
                self.m.warn(f"{self.r['diff']}")

    def _build_diff_after(self) -> dict:
        return {
            'enabled': self.p['enabled'],
            'minutes': self.p['minutes'],
            'hours': self.p['hours'],
            'days': self.p['days'],
            'months': self.p['months'],
            'weekdays': self.p['weekdays'],
            'command': self.p['command'],
            'parameters': self.p['parameters'],
            'who': self.p['who'],
            'description': self.p['description'],
            'uuid': self.cron['uuid'] if self.cron is not None else None,
        }

    def _build_request(self) -> dict:
        return {
            self.API_KEY: {
                'enabled': to_digit(self.p['enabled']),
                'minutes': self.p['minutes'],
                'hours': self.p['hours'],
                'days': self.p['days'],
                'months': self.p['months'],
                'weekdays': self.p['weekdays'],
                'command': self.p['command'],
                'parameters': self.p['parameters'],
                'who': self.p['who'],
                'description': self.p['description'],
            }
        }

    def delete(self):
        self.r['changed'] = True
        self.r['diff']['after'] = {}

        if not self.m.check_mode:
            self._delete_call()

            if self.p['debug']:
                self.m.warn(f"{self.r['diff']}")

    def _delete_call(self) -> dict:
        return self.s.post(cnf={**self.call_cnf, **{'command': self.CMDS['del']}})

    def reconfigure(self):
        # reload the active jobs
        if not self.m.check_mode:
            self.s.post(cnf={
                'module': self.call_cnf['module'],
                'controller': self.API_CONT_REL,
                'command': 'reconfigure',
                'params': []
            })
