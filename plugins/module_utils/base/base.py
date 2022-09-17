# could be implemented using inheritance in the future..

# pylint: disable=W0212

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.base.api import \
    single_get, single_post
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper.main import \
    get_simple_existing, to_digit


class Base:
    def __init__(self, instance):
        self.i = instance  # module-specific object
        self.e = {}  # existing entry

    def update(self) -> dict:
        if len(self.e) == 0:
            self.e = getattr(self.i, self.i.EXIST_ATTR)

        # checking if changed
        for field in self.i.FIELDS_CHANGE:
            if field in self.i.p:
                if str(self.e[field]) != str(self.i.p[field]):
                    self.i.r['changed'] = True
                    break

        # update if changed
        if self.i.r['changed']:
            if self.i.p['debug']:
                self.i.m.warn(f"{self.i.r['diff']}")

            if not self.i.m.check_mode:
                if hasattr(self.i, '_update_call'):
                    _ = self.i._update_call()

                elif hasattr(self.i, 's'):
                    _ = self.i.s.post(cnf={
                        **self.i.call_cnf, **{
                            'command': self.i.CMDS['set'],
                            'data': self._get_request_data(),
                        }
                    })

                else:
                    _ = single_post(
                        module=self.i.m,
                        cnf={
                            **self.i.call_cnf, **{
                                'command': self.i.CMDS['set'],
                                'data': self._get_request_data(),
                            }
                        }
                    )

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
            if hasattr(self.i, '_delete_call'):
                _ = self.i._delete_call()

            elif hasattr(self.i, 's'):
                _ = self.i.s.post(cnf={**self.i.call_cnf, **{'command': self.i.CMDS['del']}})

            else:
                _ = single_post(
                    module=self.i.m,
                    cnf={**self.i.call_cnf, **{'command': self.i.CMDS['del']}}
                )

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
        if len(self.e) == 0:
            self.e = getattr(self.i, self.i.EXIST_ATTR)

        diff = {
            'uuid': self.e['uuid'] if 'uuid' in self.e else None
        }

        for field in self.i.FIELDS_ALL:
            try:
                diff[field] = data[field]

            except KeyError:
                if field in self.i.p:
                    diff[field] = self.i.p[field]

            if isinstance(diff[field], list):
                diff[field].sort()

            elif isinstance(diff[field], str) and diff[field].isnumeric:
                try:
                    diff[field] = int(diff[field])

                except (TypeError, ValueError):
                    pass

        return diff

    def build_request(self) -> dict:
        request = {}
        translate = {}

        if len(self.e) == 0:
            self.e = getattr(self.i, self.i.EXIST_ATTR)

        if hasattr(self.i, 'FIELDS_TRANSLATE'):
            translate = self.i.FIELDS_TRANSLATE

        for field in self.i.FIELDS_ALL:
            opn_field = field
            if field in translate:
                opn_field = translate[field]

            if field in self.i.p:
                opn_data = self.i.p[field]

            else:
                opn_data = self.e[field]

            if isinstance(opn_data, bool):
                request[opn_field] = to_digit(opn_data)

            elif isinstance(opn_data, list):
                join_char = ','
                if hasattr(self, 'JOIN_CHAR'):
                    join_char = self.i.JOIN_CHAR

                request[opn_field] = join_char.join(opn_data)

            else:
                request[opn_field] = opn_data

        return {self.i.API_KEY: request}
