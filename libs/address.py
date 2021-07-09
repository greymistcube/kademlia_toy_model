import abc
import random

class Address(abc.ABC):
    ADDRESS_LENGTH = 80

    @abc.abstractmethod
    def __init__(self, array: list):
        self._array = array
        return

    @abc.abstractmethod
    def get_distance(self, address) -> int:
        pass

    @property
    def array(self) -> list:
        return self._array

    def __eq__(self, address):
        return all([x == y for x, y in zip(self.array, address.array)])

    def __repr__(self):
        return "".join([str(c) for c in self.array])

    def __hash__(self):
        return hash(self.__repr__)

    @staticmethod
    def generate_random_address():
        array = [random.randint(0, 1) for _ in range(Address.ADDRESS_LENGTH)]
        return Address(array)

    @staticmethod
    def generate_default_address():
        array = [0 for _ in range(Address.ADDRESS_LENGTH)]
        return Address(array)

class KademliaAddress(Address):
    def __init__(self, array: list):
        if len(array) != Address.ADDRESS_LENGTH:
            raise ValueError("invalid array length")

        self._array = array
        return

    def get_distance(self, address) -> int:
        distance = Address.ADDRESS_LENGTH
        for x, y in zip(self.array, address.array):
            if x == y:
                distance = distance - 1
            else:
                break
        return distance

    @staticmethod
    def generate_random_address():
        array = [random.randint(0, 1) for _ in range(Address.ADDRESS_LENGTH)]
        return KademliaAddress(array)

    @staticmethod
    def generate_default_address():
        array = [0 for _ in range(Address.ADDRESS_LENGTH)]
        return KademliaAddress(array)
