from ansible.module_utils.basic import AnsibleModule

from ansible_collections.ansibleguy.opnsense.plugins.module_utils.helper import \
    is_true
from ansible_collections.ansibleguy.opnsense.plugins.module_utils.api import \
    Session


class Package:
    UPGRADE_MSG = 'Installation out of date'
    API_MOD = 'core'
    API_CONT = 'firmware'

    def __init__(self, module: AnsibleModule, name: str, session: Session = None):
        self.m = module
        self.p = module.params
        self.s = Session(module=module) if session is None else session
        self.n = name
        self.r = {
            'changed': False, 'version': None,
            'diff': {}
        }
        self.package_stati = None
        self.call_cnf = {
            'module': self.API_MOD,
            'controller': self.API_CONT,
        }

    def check(self):
        if self.package_stati is None:
            self.package_stati = self.search_call()

        self.r['diff']['before'] = {'installed': False, 'locked': False}

        for pkg_status in self.package_stati:
            if pkg_status['name'] == self.n:
                if self.p['debug']:
                    self.m.warn(f"Package status: '{pkg_status}'")

                self.r['diff']['before'] = {
                    'version': pkg_status['version'],
                    'installed': is_true(pkg_status['installed']),
                    'locked': is_true(pkg_status['locked']),
                }
                break

        self.r['diff']['after'] = self.r['diff']['before'].copy()

        if self.p['action'] in ['install', 'reinstall']:
            self.check_system_up_to_date()

        self.check_lock()
        self.call_cnf['params'] = [self.n]

    def check_lock(self):
        if self.p['action'] in ['reinstall', 'remove', 'install'] and \
                self.r['diff']['before']['locked']:
            self.m.fail_json(
                f"Unable to execute action '{self.p['action']}' - "
                f"package is locked!"
            )

    def check_system_up_to_date(self) -> bool:
        status = self.s.get(cnf={
            'command': 'upgradestatus',
            **self.call_cnf
        })

        if str(status).find(self.UPGRADE_MSG) != -1:
            self.m.fail_json(
                f"Unable to execute action '{self.p['action']}' - "
                f"system needs to be upgraded beforehand!"
            )

        return False

    def get_existing(self) -> list:
        entries = []

        for entry in self.search_call():
            if is_true(entry['installed']):
                entries.append({
                    'name': entry['name'],
                    'version': entry['version'],
                    'locked': is_true(entry['locked']),
                })

        return entries

    def search_call(self) -> dict:
        return self.s.get(cnf={'command': 'info', **self.call_cnf})['package']

    def change_state(self):
        run = False

        if self.p['action'] == 'lock':
            if not self.r['diff']['before']['locked']:
                run = True
                self.r['diff']['after']['locked'] = True

        elif self.p['action'] == 'unlock':
            if self.r['diff']['before']['locked']:
                run = True
                self.r['diff']['after']['locked'] = False

        elif self.p['action'] == 'remove':
            self.r['diff']['after']['installed'] = False
            run = True

        else:
            run = True

        self.r['changed'] = True
        if run:
            self.execute()

    def execute(self):
        if not self.m.check_mode:
            self.s.post(cnf={
                'command': self.p['action'],
                **self.call_cnf
            })

    def install(self):
        self.r['changed'] = True
        self.r['diff']['after']['installed'] = True
        self.execute()
