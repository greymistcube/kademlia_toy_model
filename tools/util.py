from libs.address import KademliaAddress
from libs.network import KademliaNetwork
from libs.node import KademliaNode
from libs.policy import KademliaBroadcastPolicy, KademliaDiscoveryPolicy

def get_start_node(kademlia_network: KademliaNetwork, seed_start: bool):
    if seed_start:
        return kademlia_network.seed
    else:
        return kademlia_network.get_random_node()

def generate_kademlia_network(
    network_size: int,
    broadcast_type: str,
    broadcast_size: int,
    discovery_type: str,
    discovery_depth: int,
):
    if not broadcast_type in KademliaBroadcastPolicy.POLICIES:
        raise ValueError("invalid broadcast type")
    if not discovery_type in KademliaDiscoveryPolicy.POLICIES:
        raise ValueError("invalid discovery type")
    broadcast_policy = KademliaBroadcastPolicy(
        broadcast_type=broadcast_type,
        broadcast_size=broadcast_size,
    )
    discovery_policy = KademliaDiscoveryPolicy(
        discovery_type=discovery_type,
        discovery_depth=discovery_depth,
    )
    kademlia_network = KademliaNetwork(discovery_policy, broadcast_policy)
    for _ in range(network_size):
        kademlia_network.add_node(
            KademliaNode(
                network=kademlia_network,
                address=KademliaAddress.generate_random_address(),
            )
        )
    return kademlia_network
