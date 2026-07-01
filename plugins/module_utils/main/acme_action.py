from ansible.module_utils.basic import AnsibleModule

from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.oxlorg.opnsense.plugins.module_utils.helper.validate import \
    is_unset
from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.module import BaseModule


class Action(BaseModule):
    FIELD_ID = 'name'
    CMDS = {
        'add': 'add',
        'del': 'del',
        'set': 'update',
        'search': 'get',
        'toggle': 'toggle',
    }
    API_KEY_PATH = 'acmeclient.actions.action'
    API_MOD = 'acmeclient'
    API_CONT = 'actions'
    API_CONT_GET = 'settings'
    FIELDS_CHANGE = ['type']
    FIELDS_ALL = [
        'enabled', 'name', 'description',
        # SFTP
        'sftp_host', 'sftp_host_key', 'sftp_port', 'sftp_user', 'sftp_identity_type',
        'sftp_remote_path', 'sftp_chgrp', 'sftp_chmod', 'sftp_chmod_key',
        'sftp_filename_cert', 'sftp_filename_key', 'sftp_filename_ca',
        'sftp_filename_fullchain',
        # Remote SSH
        'remote_ssh_host', 'remote_ssh_host_key', 'remote_ssh_port', 'remote_ssh_user',
        'remote_ssh_identity_type', 'remote_ssh_command',
        # ACME FRITZ!Box
        'acme_fritzbox_url', 'acme_fritzbox_username', 'acme_fritzbox_password',
        # ACME PANOS
        'acme_panos_username', 'acme_panos_password', 'acme_panos_host',
        # ACME promox VE
        'acme_proxmoxve_user', 'acme_proxmoxve_server', 'acme_proxmoxve_port',
        'acme_proxmoxve_nodename', 'acme_proxmoxve_realm', 'acme_proxmoxve_tokenid',
        'acme_proxmoxve_tokenkey',
        # ACME Vault
        'acme_vault_url', 'acme_vault_prefix', 'acme_vault_token', 'acme_vault_kvv2',
        # ACME Synology DSM
        'acme_synology_dsm_hostname', 'acme_synology_dsm_port', 'acme_synology_dsm_scheme',
        'acme_synology_dsm_username', 'acme_synology_dsm_password', 'acme_synology_dsm_create',
        'acme_synology_dsm_deviceid', 'acme_synology_dsm_devicename',
        # ACME TrueNAS
        'acme_truenas_apikey', 'acme_truenas_hostname', 'acme_truenas_scheme',
        # ACME unifi
        'acme_unifi_keystore',
    ]
    FIELDS_ALL.extend(FIELDS_CHANGE)
    FIELDS_TYPING = {
        'bool': ['enabled', 'acme_vault_kvv2', 'acme_synology_dsm_create'],
        'select': [
            'type', 'remote_ssh_identity_type', 'acme_synology_dsm_scheme', 'acme_truenas_scheme',
            'sftp_identity_type',
        ],
        'int': ['sftp_port', 'remote_ssh_port', 'acme_proxmoxve_port', 'acme_synology_dsm_port'],
    }
    INT_VALIDATIONS = {
        'sftp_port': {'min': 1, 'max': 65535},
    }
    EXIST_ATTR = 'action'

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None, fail: dict = None):
        BaseModule.__init__(self=self, m=module, r=result, s=session, f=fail)
        self.action = {}

    def check(self) -> None:
        if self.p['state'] == 'present':
            if is_unset(self.p['type']):
                self.m.fail_json('You need to provide type to create/update actions!')

            if self.p['type'].startswith('acme_'):
                for field in self.FIELDS_ALL:
                    if field.startswith(self.p['type']) and is_unset(self.p[field]):
                        self.m.fail_json(f"You need to provide {field} to create/update {self.p['type']} actions!")

        self._base_check()

    def reload(self):
        # no reload required
        pass
