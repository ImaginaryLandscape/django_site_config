


class ConfigBackend(object):

    def get(self, key, default, location=None):
        """
        Get the key from the backend store and return the value.
        Return None if not found.
        """
        raise NotImplementedError

    def set(self, key, value, location=None):
        """
        Add the value to the backend store given the key.
        """
        raise NotImplementedError