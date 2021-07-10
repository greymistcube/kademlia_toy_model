import abc
from libs.address import Address, KademliaAddress
from libs.bucket import Bucket

class RoutingTable(abc.ABC):
    def __init__(self, address: Address):
        if not isinstance(address, Address):
            raise TypeError(f"invalid type for address")

        self._address = address
        return

    @abc.abstractmethod
    def get_neighbors(self, address: Address):
        pass

    @abc.abstractmethod
    def add_address(self, address: Address):
        pass

    @abc.abstractmethod
    def get_distance(self, address: Address):
        pass

    @property
    def address(self):
        return self._address

    @property
    @abc.abstractmethod
    def peers(self):
        pass

class KademliaRoutingTable(RoutingTable):
    def __init__(self, address: KademliaAddress):
        super().__init__(address)
        self._buckets = [
            Bucket(address, d)
                for d in range(KademliaAddress.ADDRESS_LENGTH + 1)
        ]
        return

    def get_neighbors(
        self,
        address: KademliaAddress,
        n=Bucket.BUCKET_SIZE
    ):
        return sorted(
            self.peers,
            key=lambda peer: peer.get_distance(address)
        )[:n]

    def add_address(self, address: KademliaAddress):
        d = self.get_distance(address)
        self._buckets[d].add_address(address)
        return

    def get_distance(self, address: KademliaAddress):
        return self.address.get_distance(address)

    def select_random_peers(self) -> list:
        """
        Selects a random peer from each bucket.
        """
        return [
            bucket.select_random_address() for bucket in self.non_empty_buckets
        ]

    def generate_random_addresses(self) -> list:
        """
        Generate a random address from each bucket.
        """
        return [
            bucket.generate_random_address() for bucket in self.buckets[1:]
        ]

    @property
    def buckets(self):
        return self._buckets

    @property
    def non_empty_buckets(self) -> list:
        return [bucket for bucket in self.buckets[1:] if bucket.peers]

    @property
    def peers(self) -> list:
        return [address for bucket in self.buckets for address in bucket.peers]
