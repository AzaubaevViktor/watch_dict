import abc


class AbstractWatcher(metaclass=abc.ABCMeta):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._callbacks = dict()

    def _run_callback(self, key, old_value, **kwargs):
        new_value = kwargs['new_value'] \
            if "new_value" in kwargs \
            else super().__getitem__(key)

        callback = self._callbacks.get(key, None)
        if callable(callback):
            callback(key, old_value, new_value)

    def set_callback(self, key: int, callback):
        """

        :param key: Ключ, при изменении значения которого будет вызываться функция
        :param callback: func(key, old_value, new_value)
        :return: None
        """
        self._callbacks[key] = callback

    def clear_callbacks(self):
        self._callbacks = dict()


class WatchList(AbstractWatcher, list):
    def __setitem__(self, index, value):
        # for simple types
        old_value = super().__getitem__(index)
        super().__setitem__(index, value)
        self._run_callback(index, old_value)

    def pop(self, index=None):
        if not index:
            index = len(self) - 1

        old_value = super().__getitem__(index)
        super().pop(index)
        self._run_callback(index, old_value, new_value=None)

