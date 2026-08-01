from ansible_collections.oxlorg.opnsense.plugins.module_utils.main.ipsec_psk import PreSharedKey


def test_ipsec_psk_supports_description():
    assert 'description' in PreSharedKey.FIELDS_CHANGE
    assert PreSharedKey.FIELDS_TRANSLATE['description'] == 'description'
