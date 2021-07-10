from libs.address import KademliaAddress
from libs.message import Message
from libs.routingtable import KademliaRoutingTable

class KademliaNode:
    def __init__(
        self,
        network,
        address: KademliaAddress,
    ):
        self._network = network
        self._address = address
        self._routing_table = KademliaRoutingTable(address)
        self._message = None
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

    def broadcast_message(self, message: str):
        self._network.broadcast_policy.broadcast_message(self, message)
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
