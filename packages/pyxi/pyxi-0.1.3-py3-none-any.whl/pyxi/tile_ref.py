from typing import Any, Dict


class TileReference:
    """
    Represents an individual tile reference used in a :class:`Layer`.

    Attributes
        :reference_id: Index of the reference.
        :index: Index of the tile; 1-based indexing is used here.
        :flipped: Whether the image is flipped on the X axis. Does not seem consistent?
        :rot: Unknown.
    """

    __slots__ = ('reference_id', 'index', 'flipped', 'rot')

    def __init__(self, n: int, data: Dict[str, Any]):
        self.reference_id = n
        self.index = data['index']
        self.flipped = data['flipX']
        self.rot = data['rot']

    def to_dict(self) -> Dict:
        """Returns a dictionary with original `.pyxel` docData.json keys."""
        return {'index': self.index, 'flipX': self.flipped, 'rot': self.rot}
