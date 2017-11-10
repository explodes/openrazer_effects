import pytest
import six

from ore.registry.registry import get_registry


def test_registry_not_empty():
    reg = get_registry()
    assert len(reg) > 0


def is_str(s):
    return type(s) in six.string_types


@pytest.mark.parametrize("cli_name,effect", get_registry().items())
def test_effect_conforms_to_Effect(cli_name, effect):
    # cli_name
    assert is_str(cli_name)

    c = effect.get_cli_name(None)
    assert c == cli_name

    assert is_str(cli_name)

    # name
    assert is_str(effect.get_name(None))

    # author
    assert is_str(effect.get_author(None))

    # type
    assert effect.get_type(None) in ["keyboard", "mouse"]

    # description
    description = effect.get_description(None)
    if description is not None:
        assert is_str(description)

    # start
    assert hasattr(effect, "start")
    assert callable(effect.start)
