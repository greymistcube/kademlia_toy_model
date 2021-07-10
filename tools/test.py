from libs.address import KademliaAddress
from libs.policy import KademliaBroadcastPolicy, KademliaDiscoveryPolicy
from libs.node import KademliaNode
from libs.message import Message
from libs.network import KademliaNetwork
from tools import util

def run_single_trial(
    kademlia_network: KademliaNetwork,
    seed_start: bool,
):
    network_size = kademlia_network.size
    discovery_type = kademlia_network.discovery_policy.discovery_type
    discovery_depth = kademlia_network.discovery_policy.discovery_depth
    broadcast_type = kademlia_network.broadcast_policy.broadcast_type
    broadcast_size = kademlia_network.broadcast_policy.broadcast_size

    print("running a single trial with")
    print(f"    network size: {network_size}")
    print(f"    discovery type: {discovery_type}")
    if discovery_type == KademliaDiscoveryPolicy.PARTIAL:
        print(f"    discovery depth: {discovery_depth}")
    print(f"    broadcast type: {broadcast_type}")
    if broadcast_type == KademliaBroadcastPolicy.RANDOM:
        print(f"    broadcast size: {broadcast_size}")

    kademlia_network.reset()
    start_node = util.get_start_node(kademlia_network, seed_start)
    message = Message("test", 0)
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
    kademlia_network: KademliaNetwork,
    num_trials: int,
    seed_start: bool,
):
    network_size = kademlia_network.size
    discovery_type = kademlia_network.discovery_policy.discovery_type
    discovery_depth = kademlia_network.discovery_policy.discovery_depth
    broadcast_type = kademlia_network.broadcast_policy.broadcast_type
    broadcast_size = kademlia_network.broadcast_policy.broadcast_size

    print("running multiple trials with")
    print(f"    number of trials: {num_trials}")
    print(f"    network size: {network_size}")
    print(f"    broadcast type: {broadcast_type}")
    if broadcast_type == KademliaBroadcastPolicy.RANDOM:
        print(f"    broadcast size: {broadcast_size}")
    print(f"    discovery type: {discovery_type}")
    if discovery_type == KademliaDiscoveryPolicy.PARTIAL:
        print(f"    discovery depth: {discovery_depth}")

    success_results = []
    send_count_results = []
    max_hops_results = []
    propagation_results = []

    for _ in range(num_trials):
        kademlia_network.reset()
        start_node = util.get_start_node(kademlia_network, seed_start)
        message = Message("test", 0)
        kademlia_network.propagate_message(
            message, start_node.address
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
