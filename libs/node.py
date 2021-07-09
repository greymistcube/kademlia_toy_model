import random
from .address import KademliaAddress
from .policy import KademliaBroadcastPolicy
from .message import Message
from .routingtable import KademliaRoutingTable

class KademliaNode:
    def __init__(
        self,
        network,
        address: KademliaAddress,
        broadcast_policy: KademliaBroadcastPolicy,
    ):
        self._network = network
        self._address = address
        self._routing_table = KademliaRoutingTable(address)
        self._message = None
        self._broadcast_policy = broadcast_policy

        if broadcast_policy.broadcast_type == KademliaBroadcastPolicy.FLOOD:
            self.broadcast_message = self.flood_broadcast_message
        elif broadcast_policy.broadcast_type == KademliaBroadcastPolicy.SELECT:
            self.broadcast_message = self.select_broadcast_message
        elif broadcast_policy.broadcast_type == KademliaBroadcastPolicy.RANDOM:
            self.broadcast_message = self.random_broadcast_message
        else:
            raise ValueError("invalid broadcast policy")
        return

    def add_address(self, address: KademliaAddress):
        self._routing_table.add_address(address)
        return

    def get_neighbors(self, address: KademliaAddress) -> list:
        return self._routing_table.get_neighbors(address)

    def select_random_peers(self) -> list:
        return self._routing_table.select_random_peers()

    def generate_random_addresses(self) -> list:
        return self._routing_table.generate_random_addresses()

    def receive_message(self, message: Message):
        if not self._message:
            self._message = message
            self._network.queue_broadcast(
                lambda: self.broadcast_message(
                    Message(self.message.content, self.message.hops + 1)
                )
            )
        return

    def flood_broadcast_message(self, message: str):
        for peer in self.peers:
            self.send_message(peer, message)
        return

    def select_broadcast_message(self, message: str):
        for peer in self._routing_table.select_random_peers():
            self.send_message(peer, message)
        return

    def random_broadcast_message(self, message: str):
        try:
            peers = random.sample(
                self.peers,
                self._broadcast_policy.broadcast_size,
            )
        except:
            # if not enough peers, send to every peer
            peers = self.peers
        for peer in peers:
            self.send_message(peer, message)
        return

    def send_message(self, address: KademliaAddress, message: Message):
        self._network.send_message(address, message)
        return

    def reset_message(self):
        self._message = None
        return

    @property
    def address(self) -> KademliaAddress:
        return self._address

    @property
    def routing_table(self) -> KademliaRoutingTable:
        return self._routing_table

    @property
    def peers(self) -> list:
        return self._routing_table.peers

    @property
    def message(self):
        return self._message
