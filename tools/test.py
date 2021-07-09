from libs.address import KademliaAddress
from libs.policy import KademliaBroadcastPolicy, KademliaDiscoveryPolicy
from libs.node import KademliaNode
from libs.message import Message
from libs.network import KademliaNetwork

def run_single_trial(
    network_size: int,
    broadcast_type: str,
    broadcast_size: int,
    discovery_type: str,
    discovery_depth: int,
    seed_start: bool,
):
    if not broadcast_type in KademliaBroadcastPolicy.POLICIES:
        raise ValueError("invalid broadcast type")
    if not discovery_type in KademliaDiscoveryPolicy.POLICIES:
        raise ValueError("invalid discovery type")

    print("running a single trial with")
    print(f"    network size: {network_size}")
    print(f"    broadcast type: {broadcast_type}")
    if broadcast_type == KademliaBroadcastPolicy.RANDOM:
        print(f"    broadcast size: {broadcast_size}")
    print(f"    discovery type: {discovery_type}")
    if discovery_type == KademliaDiscoveryPolicy.PARTIAL:
        print(f"    discovery depth: {discovery_depth}")

    broadcast_policy = KademliaBroadcastPolicy(
        broadcast_type=broadcast_type,
        broadcast_size=broadcast_size,
    )
    discovery_policy = KademliaDiscoveryPolicy(
        discovery_type=discovery_type,
        discovery_depth=discovery_depth,
    )
    kademlia_network = KademliaNetwork(discovery_policy)
    for _ in range(network_size):
        kademlia_network.add_node(
            KademliaNode(
                network=kademlia_network,
                address=KademliaAddress.generate_random_address(),
                broadcast_policy=broadcast_policy,
            )
        )

    message = Message("test", 0)
    if seed_start:
        start_node = kademlia_network.seed
    else:
        start_node = kademlia_network.get_random_node()
    kademlia_network.propagate_message(
        message, start_node.address
    )

    print(f"total number of peers: {sum(kademlia_network.peer_counts)}")
    print(
        f"total non-empty buckets: "
        f"{sum(kademlia_network.non_empty_bucket_counts)}"
    )
    print(f"success: {kademlia_network.propagation == kademlia_network.size}")
    print(f"send count: {kademlia_network.send_count}")
    print(f"propagation: {kademlia_network.propagation}")
    print(f"max hops: {kademlia_network.max_hops}")
    return

def run_multiple_trials(
    num_trials: int,
    network_fixed: bool,
    network_size: int,
    broadcast_type: str,
    broadcast_size: int,
    discovery_type: str,
    discovery_depth: int,
    seed_start: bool,
):
    if not broadcast_type in KademliaBroadcastPolicy.POLICIES:
        raise ValueError("invalid broadcast type")
    if not discovery_type in KademliaDiscoveryPolicy.POLICIES:
        raise ValueError("invalid discovery type")

    print("running trials with")
    print(f"    number of trials: {num_trials}")
    print(f"    network size: {network_size}")
    print(f"    broadcast type: {broadcast_type}")
    if broadcast_type == KademliaBroadcastPolicy.RANDOM:
        print(f"    broadcast size: {broadcast_size}")
    print(f"    discovery type: {discovery_type}")
    if discovery_type == KademliaDiscoveryPolicy.PARTIAL:
        print(f"    discovery depth: {discovery_depth}")

    broadcast_policy = KademliaBroadcastPolicy(
        broadcast_type=broadcast_type,
        broadcast_size=broadcast_size,
    )
    discovery_policy = KademliaDiscoveryPolicy(
        discovery_type=discovery_type,
        discovery_depth=discovery_depth,
    )

    success_results = []
    send_count_results = []
    max_hops_results = []
    propagation_results = []

    if network_fixed:
        kademlia_network = KademliaNetwork(discovery_policy)
        for _ in range(network_size):
            kademlia_network.add_node(
                KademliaNode(
                    network=kademlia_network,
                    address=KademliaAddress.generate_random_address(),
                    broadcast_policy=broadcast_policy,
                )
            )
        for _ in range(num_trials):
            kademlia_network.reset_messages()
            message = Message("test", 0)
            kademlia_network.propagate_message(
                message, kademlia_network.seed.address
            )
            success = kademlia_network.propagation == kademlia_network.size
            success_results.append(success)
            if success:
                send_count_results.append(kademlia_network.send_count)
                max_hops_results.append(kademlia_network.max_hops)
            propagation_results.append(kademlia_network.propagation)
    else:
        for _ in range(num_trials):
            kademlia_network = KademliaNetwork(discovery_policy)
            for _ in range(network_size):
                kademlia_network.add_node(
                    KademliaNode(
                        network=kademlia_network,
                        address=KademliaAddress.generate_random_address(),
                        broadcast_policy=broadcast_policy,
                    )
                )
            message = Message("test", 0)
            kademlia_network.propagate_message(
                message, kademlia_network.seed.address
            )
            success = kademlia_network.propagation == kademlia_network.size
            success_results.append(success)
            if success:
                send_count_results.append(kademlia_network.send_count)
                max_hops_results.append(kademlia_network.max_hops)
            propagation_results.append(kademlia_network.propagation)

    print(f"number of successes: {sum(success_results)}")
    print(
        f"average propagation: "
        f"{sum(propagation_results) / len(propagation_results):.2f}"
    )
    max_hops_results = [
        max_hops
            for success, max_hops in zip(success_results, max_hops_results)
            if success
    ]
    if send_count_results:
        print(
            f"average send count for successes: "
            f"{sum(send_count_results) / len(send_count_results):.2f}"
        )
    else:
        print(
            f"average send count for successes: invalid"
        )
    if max_hops_results:
        print(
            f"average max hops for successes: "
            f"{sum(max_hops_results) / len(max_hops_results):.2f}"
        )
    else:
        print(
            f"average max hops for successes: invalid"
        )
    return
