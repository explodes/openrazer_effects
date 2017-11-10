import pytest
import six

from ore.registry.registry import get_registry


def test_registry_not_empty():
    reg = get_registry()
    assert len(reg) > 0


def is_str(s):
    return type(s) in six.string_types


@pytest.mark.parametrize("cli_name,effect_class", get_registry().items())
def test_effect_conforms_to_Effect(cli_name, effect_class):
    # cli_name
    assert is_str(cli_name)

    effect = effect_class(audio_device="default")

    c = effect.get_cli_name()
    assert c == cli_name

    assert is_str(cli_name)

    # name
    assert is_str(effect.get_name())

    # author
    assert is_str(effect.get_author())

    # type
    assert effect.get_effect_type() in ["keyboard", "mouse"]

    # description
    description = effect.get_description()
    if description is not None:
        assert is_str(description)

    # start
    assert hasattr(effect, "start")
    assert callable(effect.start)
