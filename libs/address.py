import abc
import numpy as np

class Address(abc.ABC):
    ADDRESS_LENGTH = 40

    @abc.abstractmethod
    def __init__(self, array: "np.ndarray"):
        if not isinstance(array, np.ndarray):
            raise TypeError("invalid type for array")
        if len(array) != Address.ADDRESS_LENGTH:
            raise ValueError("invalid array length")

        self._array = array
        return

    @abc.abstractmethod
    def get_distance(self, address: "Address") -> "int":
        pass

    @property
    def array(self) -> "np.ndarray":
        return self._array

    def __eq__(self, address) -> "bool":
        return np.array_equal(self.array, address.array)

    def __repr__(self) -> "str":
        return "".join([str(c) for c in self.array])

    def __hash__(self) -> "int":
        return hash(self.__repr__)

    @staticmethod
    def generate_random_address() -> "Address":
        array = np.random.randint(2, size=Address.ADDRESS_LENGTH)
        return Address(array)

    @staticmethod
    def generate_default_address() -> "Address":
        array = np.zeros(shape=Address.ADDRESS_LENGTH, dtype="int")
        return Address(array)

class KademliaAddress(Address):
    def __init__(self, array: np.ndarray):
        super().__init__(array)
        self._distances = {}
        return

    def get_distance(self, address: "KademliaAddress") -> "int":
        try:
            return self._distances[address]
        except:
            distance = Address.ADDRESS_LENGTH
            xor = self.array ^ address.array
            argmax = np.argmax(xor)
            first = xor[0]

            if argmax or first:
                distance = distance - argmax
            else:
                distance = 0
            self._distances[address] = distance
            return self._distances[address]

    @staticmethod
    def generate_random_address() -> "KademliaAddress":
        array = np.random.randint(2, size=Address.ADDRESS_LENGTH)
        return KademliaAddress(array)

    @staticmethod
    def generate_default_address() -> "KademliaAddress":
        array = np.zeros(shape=Address.ADDRESS_LENGTH, dtype="int")
        return KademliaAddress(array)
