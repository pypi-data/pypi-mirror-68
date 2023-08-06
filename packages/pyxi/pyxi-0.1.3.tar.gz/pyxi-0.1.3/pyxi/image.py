import json
import zipfile
from pathlib import Path
from typing import Any, Dict, List, Union

import PIL
from PIL import Image

from pyxi.animation import Animation
from pyxi.canvas import Canvas
from pyxi.palette import Palette
from pyxi.tileset import Tileset


class PyxelImage:
    """
    Represents a `.pyxel` file.

    :param str file: Path to the file that you are opening.

    Attributes
        :version: Version of PyxelEdit that was used to create the image file.
        :name: The name of the file.
        :settings: Local settings related to PyxelEdit configuration and the image file.
        :canvas: Settings related to the image canvas.
        :palette: The color palette (in hexadecimal values) used in the image file.
        :tileset: Settings related to the tile set.
        :animations: The individual animations built in the image file.
    """

    __slots__ = ('_path', 'version', 'name', 'settings', 'canvas', 'palette', 'tileset', 'animations')

    def __init__(self, file: str):
        super().__init__()
        data = self._get_data_ref(file)
        self._path = file
        self.version = data['version']
        self.name = data['name']
        self.settings = data['settings']
        self.canvas = Canvas(data['canvas'])
        self.palette = Palette(data['palette'])
        self.tileset = Tileset(data['tileset'])
        self.animations = {n: Animation(n, data['animations'][str(n)]) for n in range(len(data['animations']))}

    def to_dict(self) -> Dict:
        """Returns a dictionary with original `.pyxel` docData.json keys."""
        return {'version': self.version, 'name': self.name, 'settings': self.settings,
                'canvas': self.canvas.to_dict(), 'palette': self.palette.to_dict(),
                'tileset': self.tileset.to_dict(), 'animations': {k: v.to_dict() for k, v in self.animations.items()}}

    def save(self):
        """Packs the object into a `.pyxel` file and places it in the `/exported` directory."""
        export_path = Path(__file__).parents[1] / 'exported'
        repacked_files = {}

        # we need to load all the original .pyxel documents into memory, mapped with their filenames as keys
        with zipfile.ZipFile(self._path, 'r') as f:
            for file in f.filelist:
                if file.filename != 'docData.json':
                    repacked_files.update({file.filename: f.read(file.filename)})

        # create a new file in the '/exported' directory and write out all the buffer bytes
        with zipfile.ZipFile(Path(export_path) / f'{self.name}.pyxel', 'x') as zf:
            self.settings.update({'PyxiExport': True})
            zf.writestr('docData.json', data=json.dumps(self.to_dict(), indent=4))

            for k, v in repacked_files.items():
                zf.writestr(k, data=v)

    def get_tile(self) -> PIL.Image.Image:
        """Merges layers and returns the image.

        :returns: New :py:class:`PIL.Image.Image` object."""
        img = self.merge_layers()
        return img

    def merge_layers(self, skip_layers: List[Union[str, int]] = None, base_layer: int = 0) -> PIL.Image.Image:
        """Merges layer images onto the defined base layer and returns the new Image object.

        :param skip_layers: Not implemented.
        :param int base_layer: Changes the base layer to merge on.
        :returns: New :py:class:`PIL.Image.Image` object.
        """

        if skip_layers is None:
            skip_layers = []

        with zipfile.ZipFile(self._path, 'r') as f:
            base = Image.open(f.open(f'layer{base_layer}.png'))

            if base_layer != 0:
                remaining_layers = [layer.layer_id for layer in self.canvas.layers if layer != base_layer]

            for layer_id in remaining_layers:
                if layer_id not in skip_layers:
                    next_layer = Image.open(f.open(f'layer{layer_id}.png'))
                    base.paste(next_layer, (0, 0), next_layer.convert('RGBA'))

            return base

    def extract(self):
        """Extracts all the individual files from a .pyxel file and
        places them in a `converted/<file_name>` directory."""
        with zipfile.ZipFile(self._path, 'r') as f:
            f.extractall(Path(__file__).parents[1] / f'converted/{self.name}')

    @staticmethod
    def _get_data_ref(file: str) -> Dict[str, Any]:
        """Gets the .pyxel JSON data reference for mapping to the PyxelImage
        object. Internal use only.

        :param str file: String pointing to the .pyxel file you are opening.
        :returns: JSON-mapped dictionary.
        """

        with zipfile.ZipFile(file, 'r') as f:
            doc_file = f.read('docData.json')
            return json.loads(doc_file)
