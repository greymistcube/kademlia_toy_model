import random

class KademliaDiscoveryPolicy:
    NONE = "none"
    PARTIAL = "partial"
    COMPLETE = "complete"
    POLICIES = [NONE, PARTIAL, COMPLETE]

    def __init__(self, discovery_type: str, discovery_depth: int=1):
        if not discovery_type in KademliaDiscoveryPolicy.POLICIES:
            raise ValueError(f"invalid discovery type: {discovery_type}")

        self._discovery_type = discovery_type
        self._discovery_depth = discovery_depth

        if self.discovery_type == KademliaDiscoveryPolicy.NONE:
            self._discover_peers = self.discover_peers_none
        elif self.discovery_type == KademliaDiscoveryPolicy.PARTIAL:
            self._discover_peers = (
                lambda network, node:
                    self.discover_peers_partial(
                        network,
                        node,
                        self.discovery_depth,
                    )
            )
        elif self.discovery_type == KademliaDiscoveryPolicy.COMPLETE:
            self._discover_peers = self.discover_peers_complete
        else:
            raise ValueError("invalid peer discovery policy")
        return

    def discover_peers(self, network, node):
        self._discover_peers(network, node)
        return

    def discover_peers_none(self, network, node):
        self.discover_peers_partial(network, node, 0)
        return

    def discover_peers_partial(self, network, node, depth: int):
        network.seed.add_address(node.address)
        node.add_address(network.seed.address)

        visited = [network.seed.address]
        queue = network.seed.get_neighbors(node.address)
        while True:
            for address in queue:
                network.nodes[address].add_address(node.address)
                node.add_address(address)

            depth = depth - 1
            if not depth:
                break

            visited = visited + [
                address for address in queue if not address in visited
            ]
            queue = [
                neighbor
                    for address in queue
                    for neighbor
                        in network.nodes[address].get_neighbors(node.address)
                    if not neighbor in visited
            ]
        return

    def discover_peers_complete(self, network, node):
        for address in network.nodes:
            network.nodes[address].add_address(node.address)
            node.add_address(address)
        return

    @property
    def discovery_type(self) -> str:
        return self._discovery_type

    @property
    def discovery_depth(self) -> int:
        return self._discovery_depth

class KademliaBroadcastPolicy:
    FLOOD = "flood"
    SELECT = "select"
    RANDOM = "random"
    POLICIES = [FLOOD, SELECT, RANDOM]

    def __init__(self, broadcast_type: str, broadcast_size: int):
        if broadcast_type not in KademliaBroadcastPolicy.POLICIES:
            raise ValueError(f"invalid broadcast type: {broadcast_type}")

        self._broadcast_type = broadcast_type
        self._broadcast_size = broadcast_size

        if self.broadcast_type == KademliaBroadcastPolicy.FLOOD:
            self._broadcast_message = self.flood_broadcast_message
        elif self.broadcast_type == KademliaBroadcastPolicy.SELECT:
            self._broadcast_message = self.select_broadcast_message
        elif self.broadcast_type == KademliaBroadcastPolicy.RANDOM:
            self._broadcast_message = (
                lambda node, message: self.random_broadcast_message(
                    node,
                    message,
                    self.broadcast_size,
                )
            )
        return

    def broadcast_message(self, node, message):
        self._broadcast_message(node, message)
        return

    def flood_broadcast_message(self, node, message):
        for peer in node.peers:
            node.send_message(peer, message)
        return

    def select_broadcast_message(self, node, message):
        for peer in node.routing_table.select_random_peers():
            node.send_message(peer, message)
        return

    def random_broadcast_message(self, node, message, size):
        try:
            peers = random.sample(
                node.peers,
                size,
            )
        except:
            # if not enough peers, send to every peer
            peers = node.peers
        for peer in peers:
            node.send_message(peer, message)
        return

    @property
    def broadcast_type(self) -> str:
        return self._broadcast_type

    @property
    def broadcast_size(self) -> int:
        return self._broadcast_size
