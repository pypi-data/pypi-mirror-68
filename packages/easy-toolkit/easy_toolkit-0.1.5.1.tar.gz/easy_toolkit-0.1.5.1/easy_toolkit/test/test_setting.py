from easy_toolkit.default_settings import SettingsHandler


def test_setting_get_none():
    assert SettingsHandler.read_property("a.c") is None
    assert SettingsHandler.read_property("github_token") is not None
