class Effect(object):
    """
    Effect interface.

    All Effects are subject to this interface.
    """

    def __init__(self, **kwargs):
        """
        Constructor must accepts kwargs.

        audio_device is passed in to connect with local audio devices.
        """
        pass

    def get_name(self):
        """
        The user-friendly name of this effect.
        """
        raise NotImplementedError()

    def get_description(self):
        """
        The user-friendly, one-line description of this effect.
        """
        return None

    def get_cli_name(self):
        """
        The cli-friendly slug of this effect.
        """
        raise NotImplementedError()

    def get_author(self):
        """
        The author of this effect.
        """
        raise NotImplementedError()

    def get_effect_type(self):
        """
        The type of this effect. Either "keyboard" or "mouse"
        """
        raise NotImplementedError()

    def start(self):
        """
        Begin this effect.
        """
        raise NotImplementedError()


class KeyboardEffect(Effect):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def get_effect_type(self):
        return "keyboard"


class MouseEffect(Effect):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def get_effect_type(self):
        return "mouse"
