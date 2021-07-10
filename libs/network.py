import random
from libs.address import KademliaAddress
from libs.message import Message
from libs.node import KademliaNode
from libs.policy import KademliaBroadcastPolicy, KademliaDiscoveryPolicy

class KademliaNetwork:
    def __init__(
        self,
        discovery_policy: KademliaDiscoveryPolicy,
        broadcast_policy: KademliaBroadcastPolicy,
    ):
        self._seed = None
        self._nodes = {}
        self._queue = []
        self._discovery_policy = discovery_policy
        self._broadcast_policy = broadcast_policy

        self._send_count = 0
        return

    def set_seed(self, node: KademliaNode):
        self._seed = node
        self._nodes[node.address] = node
        return

    def add_node(self, node: KademliaNode):
        if node.address in self._nodes:
            raise ValueError("node already in network")

        if not self._nodes:
            # first node is set to seed
            self._nodes[node.address] = node
            self._seed = node
        else:
            self._nodes[node.address] = node
            self.discover_peers(node)
        return

    def discover_peers(self, node):
        self.discovery_policy.discover_peers(self, node)
        return

    def propagate_message(
        self,
        message: Message,
        start_address: KademliaAddress,
    ):
        if not message:
            raise ValueError("invalid message")

        self.send_message(start_address, message)
        while self._queue:
            broadcast = self._queue.pop(0)
            broadcast()
        return

    def queue_broadcast(self, broadcast):
        self._queue = self._queue + [broadcast]
        return

    def send_message(self, address: KademliaAddress, message):
        self._send_count = self._send_count + 1
        self.nodes[address].receive_message(message)
        return

    def get_random_node(self) -> KademliaNode:
        return random.choice(list(self.nodes.values()))

    def set_broadcast_policy(self, broadcast_policy: KademliaBroadcastPolicy):
        self._broadcast_policy = broadcast_policy
        return

    def reset(self):
        self._reset_send_count()
        self._reset_messages()
        return

    def _reset_send_count(self):
        self._send_count = 0
        return

    def _reset_messages(self):
        for address in self.nodes:
            self.nodes[address].reset_message()
        return

    @property
    def seed(self) -> KademliaNode:
        return self._seed

    @property
    def nodes(self) -> dict:
        return self._nodes

    @property
    def size(self) -> int:
        return len(self.nodes)

    @property
    def discovery_policy(self) -> KademliaDiscoveryPolicy:
        return self._discovery_policy

    @property
    def broadcast_policy(self) -> KademliaBroadcastPolicy:
        return self._broadcast_policy

    @property
    def send_count(self) -> int:
        return self._send_count

    @property
    def propagation(self) -> int:
        return len([
            True
                for node in self.nodes.values()
                if node.message
        ])

    @property
    def max_hops(self) -> int:
        return max([
            node.message.hops
                for node in self.nodes.values()
                if node.message
        ])

    @property
    def peer_counts(self) -> list:
        return [len(self.nodes[address].peers) for address in self.nodes]

    @property
    def non_empty_bucket_counts(self) -> list:
        return [
            len(self.nodes[address].routing_table.non_empty_buckets)
                for address in self.nodes
        ]
