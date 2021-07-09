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
        return

    @property
    def broadcast_type(self) -> str:
        return self._broadcast_type

    @property
    def broadcast_size(self) -> int:
        return self._broadcast_size
