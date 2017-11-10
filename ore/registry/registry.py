import glob
from os.path import dirname, basename, isfile

from ore.core.effects import Effect

_REGISTRY = {}


def register_effect(effect: Effect):
    """
    Registers an effect.

    An effect be of type openrazer_effects.core.effects.Effect to be valid.
    """
    cli_name = effect.get_cli_name(None)
    if cli_name in _REGISTRY:
        raise ValueError("effect {} already registered.".format(cli_name))
    _REGISTRY[cli_name] = effect


def get_registry():
    _load_all_submodules()
    return _REGISTRY


def _load_all_submodules():
    import ore.effects
    modules = glob.glob(dirname(ore.effects.__file__) + "/*.py")
    files = ["ore.effects.{}".format(basename(f)[:-3]) for f in modules if isfile(f) and not f.endswith('__init__.py')]
    f = list(map(__import__, files))
    return f
