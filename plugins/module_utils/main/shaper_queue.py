from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.main import \
    get_matching, is_true, to_digit, get_simple_existing, get_selected, validate_int_fields


class Queue:
    CMDS = {
        'add': 'addQueue',
        'del': 'delQueue',
        'set': 'setQueue',
        'search': 'get',
        'toggle': 'toggleQueue',
    }
    API_KEY = 'queue'
    API_MOD = 'trafficshaper'
    API_CONT = 'settings'
    API_CONT_REL = 'service'
    API_CMD_REL = 'reconfigure'
    CHANGE_CHECK_FIELDS = [
        'codel_enable', 'codel_ecn_enable', 'pie_enable',  'mask', 'description',
        'pipe', 'buckets', 'codel_target', 'codel_interval', 'weight',
    ]
    INT_VALIDATIONS = {
        'weight': {'min': 1, 'max': 100},
        'buckets': {'min': 1, 'max': 65535},
        'codel_target': {'min': 1, 'max': 10000},
        'codel_interval': {'min': 1, 'max': 10000},
    }

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None):
        self.m = module
        self.p = module.params
        self.r = result
        self.s = Session(module=module) if session is None else session
        self.exists = False
        self.queue = {}
        self.pipe = None
        self.call_cnf = {  # config shared by all calls
            'module': self.API_MOD,
            'controller': self.API_CONT,
        }
        self.existing_queues = None
        self.existing_pipes = None

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
        validate_int_fields(module=self.m, data=self.p, field_minmax=self.INT_VALIDATIONS)

        # checking if item exists
        self._find_queue()
        if self.exists:
            self.call_cnf['params'] = [self.queue['uuid']]

        if self.p['state'] == 'present':
            if self.p['pipe'] in [None, '']:
                self.m.fail_json("You need to provide a 'pipe' to create a shaper queue!")

            if self.p['weight'] in [None, '']:
                if not self.exists:
                    self.m.fail_json("You need to provide 'weight' to create a shaper queue!")

                else:
                    self.p['weight'] = self.queue['weight']

        self._find_pipe()
        if self.pipe is None and self.p['state'] == 'present':
            self.m.fail_json(f"Provided pipe does not exist: '{self.p['pipe']}'")

        self.r['diff']['after'] = self._build_diff(self.p)

    def _find_queue(self):
        if self.existing_queues is None:
            self.existing_queues = self._search_call()

        match = get_matching(
            module=self.m, existing_items=self.existing_queues,
            compare_item=self.p, match_fields=['description'],
            simplify_func=self._simplify_existing,
        )

        if match is not None:
            self.queue = match
            self.r['diff']['before'] = self._build_diff(self.queue)
            self.exists = True

    def get_existing(self) -> list:
        return get_simple_existing(
            entries=self._search_call(),
            simplify_func=self._simplify_existing
        )

    def _search_call(self) -> dict:
        raw = self.s.get(cnf={
            **self.call_cnf, **{'command': self.CMDS['search']}
        })['ts']
        self.existing_pipes = raw['pipes']['pipe']
        return raw['queues'][self.API_KEY]

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
        for field in self.CHANGE_CHECK_FIELDS:
            if str(self.queue[field]) != str(self.p[field]):
                self.r['changed'] = True
                break

        if not self.r['changed']:
            if self.queue['enabled'] != self.p['enabled']:
                if self.p['enabled']:
                    self.enable()

                else:
                    self.disable()

        else:
            # update if changed
            if self.p['debug']:
                self.m.warn(f"{self.r['diff']}")

            if not self.m.check_mode:
                self.s.post(cnf={
                    **self.call_cnf, **{
                        'command': self.CMDS['set'],
                        'data': self._build_request(),
                    }
                })

    @staticmethod
    def _simplify_existing(queue: dict) -> dict:
        # makes processing easier
        pipe_uuid = get_selected(queue['pipe'])
        pipe_name = queue['pipe'][pipe_uuid]['value']
        return {
            'uuid': queue['uuid'],
            'enabled': is_true(queue['enabled']),
            'weight': queue['weight'],
            'mask': get_selected(queue['mask']),
            'buckets': queue['buckets'],
            'pie_enable': is_true(queue['pie_enable']),
            'codel_enable': is_true(queue['codel_enable']),
            'codel_ecn_enable': is_true(queue['codel_ecn_enable']),
            'codel_target': queue['codel_target'],
            'codel_interval': queue['codel_interval'],
            'description': queue['description'],
            'pipe': {
                'uuid': pipe_uuid,
                'description': pipe_name,
            }
        }

    def _find_pipe(self):
        if len(self.existing_pipes) > 0:
            for uuid, pipe in self.existing_pipes.items():
                if pipe['description'] == self.p['pipe']:
                    self.pipe = {
                        'uuid': uuid,
                        'description': pipe['description'],
                    }
                    self.p['pipe'] = self.pipe
                    break

    def _build_diff(self, data: dict) -> dict:
        relevant_int_fields = ['buckets', 'codel_target', 'codel_interval', 'weight']
        relevant_fields = [
            'codel_enable', 'codel_ecn_enable', 'pie_enable', 'enabled',
            'mask', 'description', 'pipe',
        ]
        diff = {}
        for field in relevant_int_fields:
            try:
                diff[field] = int(data[field])

            except (TypeError, ValueError):
                diff[field] = data[field]

        for field in relevant_fields:
            diff[field] = data[field]

        if self.queue is not None and 'uuid' in self.queue:
            diff['uuid'] = self.queue['uuid']

        else:
            diff['uuid'] = None

        return diff

    def _build_request(self) -> dict:
        return {
            self.API_KEY: {
                'enabled': to_digit(self.p['enabled']),
                'pipe': self.p['pipe']['uuid'],
                'mask': self.p['mask'],
                'weight': self.p['weight'],
                'buckets': self.p['buckets'],
                'pie_enable': to_digit(self.p['pie_enable']),
                'codel_enable': to_digit(self.p['codel_enable']),
                'codel_ecn_enable': to_digit(self.p['codel_enable']),
                'codel_target': self.p['codel_target'],
                'codel_interval': self.p['codel_interval'],
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

    def enable(self):
        if self.exists and not self.queue['enabled']:
            self.r['changed'] = True
            self.r['diff']['before'] = {'enabled': False}
            self.r['diff']['after'] = {'enabled': True}

            if not self.m.check_mode:
                self._change_enabled_state(1)

    def disable(self):
        if self.exists and self.queue['enabled']:
            self.r['changed'] = True
            self.r['diff']['before'] = {'enabled': True}
            self.r['diff']['after'] = {'enabled': False}

            if not self.m.check_mode:
                self._change_enabled_state(0)

    def _change_enabled_state(self, value: int):
        self.s.post(cnf={
            **self.call_cnf, **{
                'command': self.CMDS['toggle'],
                'params': [self.queue['uuid'], value],
            }
        })

    def reload(self):
        # reload the running config
        if not self.m.check_mode:
            self.s.post(cnf={
                'module': self.API_MOD,
                'controller': self.API_CONT_REL,
                'command': self.API_CMD_REL,
                'params': []
            })
