class Effect(object):

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

    def get_type(self):
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
    def get_type(self):
        return "keyboard"


class MouseEffect(Effect):
    def get_type(self):
        return "mouse"
