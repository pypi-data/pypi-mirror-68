from typing import Any, Dict

from pyxi.tile_ref import TileReference


class Layer:
    """
    Represents an individual layer used in the image :class:`Canvas`.

    Attributes
        :layer_id: Index of the layer.
        :name: Name of the layer.
        :blend_mode: Which blend mode us being used on the layer. Can be `normal`.
        :alpha: Transparency of the layer `(0-255)`.
        :muted: Unknown.
        :soloed: Unknown.
        :tile_references: Individual references to each :class:`TileReference` used by the layer.
    """

    __slots__ = ('layer_id', 'blend_mode', 'alpha', 'hidden', 'name', 'muted', 'tile_references', 'soloed')

    def __init__(self, n: int, data: Dict[str, Any]):
        self.layer_id = n
        self.name = data['name']
        self.blend_mode = data['blendMode']
        self.alpha = data['alpha']
        self.hidden = data['hidden']
        self.muted = data['muted']
        self.soloed = data['soloed']
        self.tile_references = {n: TileReference(n, data['tileRefs'][str(n)]) for n in range(len((data['tileRefs'])))}

    def to_dict(self) -> Dict:
        """Returns a dictionary with original `.pyxel` docData.json keys."""
        return {'name': self.name, 'blendMode': self.blend_mode, 'alpha': self.alpha,
                'hidden': self.hidden, 'muted': self.muted, 'soloed': self.soloed,
                'tileRefs': {k: v.to_dict() for k, v in self.tile_references.items()}}
