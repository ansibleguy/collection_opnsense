# could be implemented using inheritance in the future..

# pylint: disable=W0212

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.main import \
    get_simple_existing, to_digit


class Base:
    def __init__(self, instance):
        self.i = instance  # module-specific object
        self.e = getattr(self.i, self.i.EXIST_ATTR)  # existing entry

    def update(self) -> dict:
        # checking if changed
        for field in self.i.FIELDS_CHANGE:
            if str(self.e[field]) != str(self.i.p[field]):
                self.i.r['changed'] = True
                break

        # update if changed
        if self.i.r['changed']:
            if self.i.p['debug']:
                self.i.m.warn(f"{self.i.r['diff']}")

            if not self.i.m.check_mode:
                return self.i.s.post(cnf={
                    **self.i.call_cnf, **{
                        'command': self.i.CMDS['set'],
                        'data': self._get_request_data(),
                    }
                })

    def delete(self) -> dict:
        self.i.r['changed'] = True
        self.i.r['diff']['after'] = {}

        if not self.i.m.check_mode:
            _ = self.i.s.post(cnf={**self.i.call_cnf, **{'command': self.i.CMDS['del']}})

            if self.i.p['debug']:
                self.i.m.warn(f"{self.i.r['diff']}")

            return _

    def process(self) -> None:
        if self.i.p['state'] == 'absent':
            if self.i.exists:
                self.i.delete()

        else:
            if self.i.exists:
                self.i.update()

            else:
                self.i.create()

    def search(self) -> (dict, list):
        return self.i.s.get(cnf={
            **self.i.call_cnf, **{'command': self.i.CMDS['search']}
        })[self.i.API_MAIN_KEY][self.i.API_KEY]

    def detail(self) -> (dict, list):
        return self.i.s.get(cnf={
            **self.i.call_cnf, **{'command': self.i.CMDS['detail']}
        })[self.i.API_KEY]

    def reload(self) -> dict:
        # reload the running config
        if not self.i.m.check_mode:
            return self.i.s.post(cnf={
                'module': self.i.API_MOD,
                'controller': self.i.API_CONT_REL,
                'command': self.i.API_CMD_REL,
                'params': []
            })

    def create(self) -> dict:
        self.i.r['changed'] = True

        if not self.i.m.check_mode:
            return self.i.s.post(cnf={
                **self.i.call_cnf, **{
                    'command': self.i.CMDS['add'],
                    'data': self._get_request_data(),
                }
            })

    def _get_request_data(self):
        if hasattr(self.i, '_build_request'):
            return self.i._build_request()

        else:
            return self.build_request()

    def _change_enabled_state(self, value: int) -> dict:
        return self.i.s.post(cnf={
            **self.i.call_cnf, **{
                'command': self.i.CMDS['toggle'],
                'params': [self.i.stuff['uuid'], value],
            }
        })

    def enable(self) -> dict:
        if self.i.exists and not self.i.stuff['enabled']:
            self.i.r['changed'] = True
            self.i.r['diff']['before'] = {'enabled': False}
            self.i.r['diff']['after'] = {'enabled': True}

            if not self.i.m.check_mode:
                return self._change_enabled_state(1)

    def disable(self) -> dict:
        if self.i.exists and self.i.stuff['enabled']:
            self.i.r['changed'] = True
            self.i.r['diff']['before'] = {'enabled': True}
            self.i.r['diff']['after'] = {'enabled': False}

            if not self.i.m.check_mode:
                return self._change_enabled_state(0)

    def get_existing(self) -> list:
        return get_simple_existing(
            entries=self.i._search_call(),
            simplify_func=self.i._simplify_existing
        )

    def build_diff(self, data: dict) -> dict:
        diff = {
            'uuid': self.e['uuid'] if 'uuid' in self.e else None
        }

        for field in self.i.FIELDS_ALL:
            diff[field] = data[field]

            if isinstance(data[field], list):
                diff[field].sort()

            elif isinstance(data[field], str) and data[field].isnumeric:
                try:
                    diff[field] = int(data[field])

                except (TypeError, ValueError):
                    pass

        return diff

    def build_request(self) -> dict:
        request = {}

        for field in self.i.FIELDS_ALL:
            if isinstance(self.i.p[field], bool):
                request[field] = to_digit(self.i.p[field])

            elif isinstance(self.i.p[field], list):
                join_char = ','
                if hasattr(self, 'JOIN_CHAR'):
                    join_char = self.i.JOIN_CHAR

                request[field] = join_char.join(self.i.p[field])

            else:
                request[field] = self.i.p[field]

        return request
