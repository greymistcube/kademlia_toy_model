import random
from libs.address import KademliaAddress

class Bucket:
    BUCKET_SIZE = 10

    def __init__(self, address: KademliaAddress, distance: int):
        self._address = address
        self._distance = distance
        self._peers = []
        return

    def add_address(self, address: KademliaAddress):
        if self.address.get_distance(address) != self.distance:
            raise ValueError("invalid distance")

        if not address in self.peers:
            self._peers.append(address)
            if len(self.peers) > Bucket.BUCKET_SIZE:
                self._peers = self._peers[1:]
        return

    def select_random_address(self) -> KademliaAddress:
        if not self._peers:
            raise RuntimeError("invalid method call")

        return random.choice(self.peers)

    def generate_random_address(self) -> KademliaAddress:
        return KademliaAddress(
            self._address.array[
                :KademliaAddress.ADDRESS_LENGTH - self._distance
            ] + KademliaAddress.generate_random_address().array[
                KademliaAddress.ADDRESS_LENGTH - self._distance:
            ]
        )

    @property
    def address(self) -> KademliaAddress:
        """
        Address of the routing table owning this bucket
        """
        return self._address

    @property
    def distance(self) -> int:
        """
        The distance from `address` for all peers.
        """
        return self._distance

    @property
    def peers(self):
        return self._peers
