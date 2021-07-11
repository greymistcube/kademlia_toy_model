class Message:
    def __init__(self, content: "str", hops: "int"):
        self._content = content
        self._hops = hops
        return

    @property
    def content(self) -> "str":
        return self._content

    @property
    def hops(self) -> "int":
        return self._hops
