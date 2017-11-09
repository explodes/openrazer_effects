def test_dbus_import():
    """
    Make sure that dbus is import-able.
    """
    import dbus
    assert dbus is not None
