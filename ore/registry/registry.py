from ore.core.effects import Effect


REGISTRY = {}


def register_effect(effect: Effect):
    """
    Registers an effect.

    An effect be of type openrazer_effects.core.effects.Effect to be valid.
    """
    cli_name = effect.get_cli_name(None)
    if cli_name in REGISTRY:
        raise ValueError("effect {} already registered.".format(cli_name))
    REGISTRY[cli_name] = effect
