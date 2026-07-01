from ansible.module_utils.basic import AnsibleModule

from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.api import \
    Session
from ansible_collections.oxlorg.opnsense.plugins.module_utils.helper.main import is_unset
from ansible_collections.oxlorg.opnsense.plugins.module_utils.base.module import BaseModule


class Validation(BaseModule):
    FIELD_ID = 'name'
    CMDS = {
        'add': 'add',
        'del': 'del',
        'set': 'update',
        'search': 'get',
        'toggle': 'toggle',
    }
    API_KEY_PATH = 'acmeclient.validations.validation'
    API_MOD = 'acmeclient'
    API_CONT = 'validations'
    API_CONT_GET = 'settings'
    FIELDS_CHANGE = ['description', 'method']
    FIELDS_ALL = [
        'name',
        'http_service', 'http_opn_autodiscovery', 'http_opn_interface', 'http_opn_ipaddresses', 'http_haproxy_inject',
        'http_haproxy_frontends', 'tlsalpn_acme_autodiscovery', 'tlsalpn_acme_ipaddresses', 'tlsalpn_acme_interface',
        'dns_service', 'dns_sleep', 'dns_active24_token', 'dns_ad_key', 'dns_ali_key', 'dns_ali_secret',
        'dns_autodns_user', 'dns_autodns_password', 'dns_autodns_context', 'dns_aws_id', 'dns_aws_secret',
        'dns_azuredns_subscriptionid', 'dns_azuredns_tenantid', 'dns_azuredns_appid', 'dns_azuredns_clientsecret',
        'dns_bunny_api_key', 'dns_cf_email', 'dns_cf_key', 'dns_cf_token', 'dns_cf_account_id', 'dns_cf_zone_id',
        'dns_cloudns_auth_id', 'dns_cloudns_sub_auth_id', 'dns_cloudns_auth_password', 'dns_cx_key', 'dns_cx_secret',
        'dns_cyon_user', 'dns_cyon_password', 'dns_ddnss_token', 'dns_dgon_key', 'dns_dnsexit_auth_user',
        'dns_dnsexit_auth_pass', 'dns_dnsexit_api', 'dns_dnshome_password', 'dns_dnshome_subdomain',
        'dns_dnsimple_token', 'dns_dnsservices_user', 'dns_dnsservices_password', 'dns_doapi_token', 'dns_do_pid',
        'dns_do_password', 'dns_domeneshop_token', 'dns_domeneshop_secret', 'dns_dp_id', 'dns_dp_key',
        'dns_duckdns_token', 'dns_dyn_customer', 'dns_dyn_user', 'dns_dyn_password', 'dns_dynu_clientid',
        'dns_dynu_secret', 'dns_freedns_user', 'dns_freedns_password', 'dns_fornex_api_key', 'dns_gandi_livedns_key',
        'dns_gandi_livedns_token', 'dns_gcloud_key', 'dns_googledomains_access_token', 'dns_googledomains_zone',
        'dns_gd_key', 'dns_gd_secret', 'dns_hostingde_server', 'dns_hostingde_apiKey', 'dns_he_user',
        'dns_he_password', 'dns_infoblox_credentials', 'dns_infoblox_server', 'dns_inwx_user', 'dns_inwx_password',
        'dns_inwx_shared_secret', 'dns_ionos_prefix', 'dns_ionos_secret', 'dns_ipv64_token', 'dns_ispconfig_user',
        'dns_ispconfig_password', 'dns_ispconfig_api', 'dns_ispconfig_insecure','dns_jd_id', 'dns_jd_region',
        'dns_jd_secret', 'dns_joker_username', 'dns_joker_password', 'dns_kinghost_username', 'dns_kinghost_password',
        'dns_knot_server', 'dns_knot_key', 'dns_limacity_apikey', 'dns_linode_v4_key', 'dns_loopia_api',
        'dns_loopia_user', 'dns_loopia_password', 'dns_lua_email', 'dns_lua_key', 'dns_miab_user', 'dns_miab_password',
        'dns_miab_server', 'dns_me_key', 'dns_me_secret', 'dns_mydnsjp_masterid', 'dns_mydnsjp_password',
        'dns_mythic_beasts_key', 'dns_mythic_beasts_secret', 'dns_namecheap_user', 'dns_namecheap_api',
        'dns_namecheap_sourceip', 'dns_namecom_user', 'dns_namecom_token', 'dns_namesilo_key', 'dns_nederhost_key',
        'dns_netcup_cid', 'dns_netcup_key', 'dns_netcup_pw', 'dns_njalla_token', 'dns_nsone_key',
        'dns_nsupdate_server', 'dns_nsupdate_zone', 'dns_nsupdate_key', 'dns_oci_cli_user', 'dns_oci_cli_tenancy',
        'dns_oci_cli_region', 'dns_oci_cli_key', 'dns_online_key', 'dns_opnsense_host', 'dns_opnsense_port',
        'dns_opnsense_key', 'dns_opnsense_token', 'dns_opnsense_insecure', 'dns_ovh_app_key', 'dns_ovh_app_secret',
        'dns_ovh_consumer_key', 'dns_ovh_endpoint', 'dns_pleskxml_user', 'dns_pleskxml_pass', 'dns_pleskxml_uri',
        'dns_pdns_url', 'dns_pdns_serverid', 'dns_pdns_token', 'dns_porkbun_key', 'dns_porkbun_secret', 'dns_sl_key',
        'dns_selfhost_user', 'dns_selfhost_password', 'dns_selfhost_map', 'dns_servercow_username',
        'dns_servercow_password', 'dns_simply_api_key', 'dns_simply_account_name', 'dns_transip_username',
        'dns_transip_key', 'dns_udr_user', 'dns_udr_password', 'dns_uno_key', 'dns_uno_user', 'dns_vscale_key',
        'dns_vultr_key', 'dns_yandex_token', 'dns_zilore_key', 'dns_zm_key', 'dns_gdnsdk_user', 'dns_gdnsdk_password',
        'dns_acmedns_user', 'dns_acmedns_password', 'dns_acmedns_subdomain', 'dns_acmedns_updateurl',
        'dns_acmedns_baseurl', 'dns_acmeproxy_endpoint', 'dns_acmeproxy_username', 'dns_acmeproxy_password',
        'dns_variomedia_key', 'dns_schlundtech_user', 'dns_schlundtech_password', 'dns_easydns_apitoken',
        'dns_easydns_apikey', 'dns_euserv_user', 'dns_euserv_password', 'dns_leaseweb_key', 'dns_cn_user',
        'dns_cn_password', 'dns_arvan_token', 'dns_artfiles_username', 'dns_artfiles_password', 'dns_hetzner_token',
        'dns_hetznercloud_token',
        'dns_hexonet_login', 'dns_hexonet_password', 'dns_1984hosting_user', 'dns_1984hosting_password',
        'dns_kas_login', 'dns_kas_authdata', 'dns_kas_authtype', 'dns_desec_token', 'dns_desec_name',
        'dns_infomaniak_token', 'dns_zone_username', 'dns_zone_key', 'dns_dynv6_token', 'dns_cpanel_user',
        'dns_cpanel_token', 'dns_cpanel_hostname', 'dns_regru_username', 'dns_regru_password', 'dns_nic_username',
        'dns_nic_password', 'dns_nic_client', 'dns_nic_secret', 'dns_world4you_username', 'dns_world4you_password',
        'dns_aurora_key', 'dns_aurora_secret', 'dns_conoha_user', 'dns_conoha_password', 'dns_conoha_tenantid',
        'dns_conoha_idapi', 'dns_constellix_key', 'dns_constellix_secret', 'dns_exoscale_key', 'dns_exoscale_secret',
        'dns_internetbs_key', 'dns_internetbs_password', 'dns_pointhq_key', 'dns_pointhq_email', 'dns_rackspace_user',
        'dns_rackspace_key', 'dns_rage4_token', 'dns_rage4_user',
    ]
    FIELDS_ALL.extend(FIELDS_CHANGE)
    FIELDS_TRANSLATE = {
        'http_haproxy_inject': 'http_haproxyInject',
        'http_haproxy_frontends': 'http_haproxyFrontends',
    }
    FIELDS_TYPING = {
        'bool': [
            'enabled', 'http_opn_autodiscovery', 'http_haproxy_inject', 'tlsalpn_acme_autodiscovery',
            'dns_opnsense_insecure', 'dns_ispconfig_insecure',
        ],
        'list': ['http_opn_ipaddresses', 'http_haproxy_frontends', 'tlsalpn_acme_ipaddresses'],
        'select': [
            'method', 'http_service', 'http_opn_interface', 'tlsalpn_acme_interface', 'dns_service',
            'dns_kas_authtype',
        ],
    }
    EXIST_ATTR = 'validation'

    def __init__(self, module: AnsibleModule, result: dict, session: Session = None, fail: dict = None):
        BaseModule.__init__(self=self, m=module, r=result, s=session, f=fail)
        self.validation = {}

    def check(self) -> None:
        if self.p['state'] == 'present':
            if is_unset(self.p['method']):
                self.m.fail_json('You need to provide method to create/update validations!')

            if self.p['method'] == 'http01':
                self.FIELDS_CHANGE = self.FIELDS_CHANGE + ['http_service']
                if self.p['http_service'] == 'opnsense':
                    self.FIELDS_CHANGE = self.FIELDS_CHANGE + [
                        field
                        for field in self.FIELDS_ALL
                        if field.startswith('http_opn')
                    ]

                else:
                    self.FIELDS_CHANGE = self.FIELDS_CHANGE + [
                        field
                        for field in self.FIELDS_ALL
                        if field.startswith('http_haproxy')
                    ]

            elif self.p['method'] == 'tlsalpn01':
                self.FIELDS_CHANGE = self.FIELDS_CHANGE + [
                    field
                    for field in self.FIELDS_ALL
                    if field.startswith('tlsalpn_')
                ]

            elif self.p['method'] == 'dns01':
                # OPNsense API does not seem to return the access-tokens anymore - no way to compare it
                self.r['changed'] = True

        self._base_check()

    def reload(self):
        # no reload required
        pass
