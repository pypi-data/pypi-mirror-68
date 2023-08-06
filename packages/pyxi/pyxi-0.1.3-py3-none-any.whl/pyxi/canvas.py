from typing import Any, Dict

from pyxi.layer import Layer


class Canvas:
    """
    Represents the canvas used in the :class:`PyxelImage`.

    Attributes
        :width: Number of columns in the image.
        :height: Number of rows in the image.
        :tile_width: Width in pixels of each tile.
        :tile_height: Height in pixels of each tile.
        :layer_count: Number of layers in the image.
        :layers: Individual :class:`Layer`'s in the image.
    """

    __slots__ = ('width', 'height', 'tile_width', 'tile_height', 'layer_count', 'layers')

    def __init__(self, data: Dict[str, Any]):
        self.width = data['width']
        self.height = data['height']
        self.tile_width = data['tileWidth']
        self.tile_height = data['tileHeight']
        self.layer_count = data['numLayers']
        self.layers = {n: Layer(n, data['layers'][str(n)]) for n in range(self.layer_count)}

    def to_dict(self) -> Dict:
        """Returns a dictionary with original `.pyxel` docData.json keys."""
        return {'width': self.width, 'height': self.height, 'tileWidth': self.tile_width,
                'tileHeight': self.tile_height, 'numLayers': self.layer_count,
                'layers': {k: v.to_dict() for k, v in self.layers.items()}}
