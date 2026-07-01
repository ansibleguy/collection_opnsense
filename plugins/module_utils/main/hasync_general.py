from ansible.module_utils.basic import AnsibleModule

from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.module import GeneralModule


class General(GeneralModule):
    CMDS = {
        'set': 'set',
        'search': 'get',
    }
    API_KEY_PATH = 'hasync'
    API_MOD = 'core'
    API_CONT = 'hasync'
    FIELDS_CHANGE = [
        'preempt', 'disconnect_ppps', 'pfsync_interface', 'pfsync_peer_ip', 'pfsync_version', 'synchronize_to_ip',
        'verify_peer', 'username', 'syncitems',
    ]
    FIELDS_ALL = ['password']
    FIELDS_ALL.extend(FIELDS_CHANGE)
    FIELDS_TRANSLATE = {
        'preempt': 'disablepreempt',
        'disconnect_ppps': 'disconnectppps',
        'pfsync_interface': 'pfsyncinterface',
        'pfsync_peer_ip': 'pfsyncpeerip',
        'pfsync_version': 'pfsyncversion',
        'synchronize_to_ip': 'synchronizetoip',
        'verify_peer': 'verifypeer',
    }
    FIELDS_BOOL_INVERT = ['preempt']
    FIELDS_TYPING = {
        'bool': ['preempt', 'disconnect_ppps', 'verify_peer'],
        'select': ['pfsync_interface', 'pfsync_version'],
        'list': ['syncitems'],
    }
    FIELDS_DIFF_NO_LOG = ['password']

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None):
        GeneralModule.__init__(self=self, m=module, r=result, s=session)

    def check(self) -> None:
        if self.p['update_password'] == 'always':
            self.FIELDS_CHANGE = self.FIELDS_CHANGE + ['password']

        self._base_check()
