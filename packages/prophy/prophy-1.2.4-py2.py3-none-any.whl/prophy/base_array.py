from prophy.scalar import prophy_data_object


class base_array(prophy_data_object):
    __slots__ = ['_values']

    def __init__(self):
        self._values = []

    def __getitem__(self, idx):
        return self._values[idx]

    def __getslice__(self, start, stop):
        return self._values[start:stop]

    def __len__(self):
        return len(self._values)

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        raise TypeError('unhashable object')

    def __repr__(self):
        return repr(self._values)

    def sort(self, key_function=lambda x: x):
        self._values.sort(key=key_function)
