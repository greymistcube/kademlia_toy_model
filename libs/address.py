import abc
import random
import numpy as np

class Address(abc.ABC):
    ADDRESS_LENGTH = 80

    @abc.abstractmethod
    def __init__(self, array: np.ndarray):
        if not isinstance(array, np.ndarray):
            raise TypeError("invalid type for array")
        if len(array) != Address.ADDRESS_LENGTH:
            raise ValueError("invalid array length")

        self._array = array
        return

    @abc.abstractmethod
    def get_distance(self, address) -> int:
        pass

    @property
    def array(self) -> np.ndarray:
        return self._array

    def __eq__(self, address):
        return np.array_equal(self.array, address.array)

    def __repr__(self):
        return "".join([str(c) for c in self.array])

    def __hash__(self):
        return hash(self.__repr__)

    @staticmethod
    def generate_random_address():
        array = np.random.randint(2, size=Address.ADDRESS_LENGTH)
        return Address(array)

    @staticmethod
    def generate_default_address():
        array = np.zeros(shape=Address.ADDRESS_LENGTH, dtype="int")
        return Address(array)

class KademliaAddress(Address):
    def __init__(self, array: np.ndarray):
        self._array = array
        return

    def get_distance(self, address) -> int:
        distance = Address.ADDRESS_LENGTH
        xor = self.array ^ address.array
        argmax = np.argmax(xor)
        first = xor[0]

        if argmax or first:
            return distance - argmax
        else:
            return 0

    @staticmethod
    def generate_random_address():
        array = np.random.randint(2, size=Address.ADDRESS_LENGTH)
        return KademliaAddress(array)

    @staticmethod
    def generate_default_address():
        array = np.zeros(shape=Address.ADDRESS_LENGTH, dtype="int")
        return KademliaAddress(array)
