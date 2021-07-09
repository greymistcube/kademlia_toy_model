import random
from libs.address import KademliaAddress
from libs.message import Message
from libs.node import KademliaNode
from libs.policy import KademliaDiscoveryPolicy

class KademliaNetwork:
    def __init__(self, discovery_policy: KademliaDiscoveryPolicy):
        self._seed = None
        self._nodes = {}
        self._queue = []
        self._discovery_policy = discovery_policy

        self._send_count = 0

        if (
            self._discovery_policy.discovery_type
                == KademliaDiscoveryPolicy.NONE
        ):
            self._discover_peers = self.discover_peers_none
        elif (
            self._discovery_policy.discovery_type
                == KademliaDiscoveryPolicy.PARTIAL
        ):
            self._discover_peers = (
                lambda node:
                    self.discover_peers_partial(
                        node,
                        self._discovery_policy._discovery_depth,
                    )
            )
        elif (
            self._discovery_policy.discovery_type
                == KademliaDiscoveryPolicy.COMPLETE
        ):
            self._discover_peers = self.discover_peers_complete
        else:
            raise ValueError("invalid peer discovery policy")
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
            self._discover_peers(node)
        return

    def discover_peers_none(self, node: KademliaNode):
        self.discover_peers_partial(node, 1)
        return

    def discover_peers_partial(self, node: KademliaNode, depth: int):
        visited = []
        queue = [self.seed.address]
        while depth:
            queue = [address for address in queue if not address in visited]
            next_queue = []

            for neighbor in queue:
                next_queue = (
                    next_queue
                        + self.nodes[neighbor].get_neighbors(node.address)
                )
                self.nodes[neighbor].add_address(node.address)
                node.add_address(neighbor)
                visited.append(neighbor)

            queue = next_queue
            depth = depth - 1
        return

    def discover_peers_complete(self, node: KademliaNode):
        for address in self._nodes:
            self._nodes[address].add_address(node.address)
            node.add_address(address)
        return

    def propagate_message(
        self,
        message: Message,
        start_address: KademliaAddress,
    ):
        if not message:
            raise ValueError("invalid message")
        self.reset_messages()

        self._send_count = 0
        self.send_message(start_address, message)
        while self._queue:
            broadcast = self._queue.pop(0)
            broadcast()
        return

    def reset_messages(self):
        for address in self.nodes:
            self.nodes[address].reset_message()
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
