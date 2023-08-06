from typing import Any, Dict


class Animation:
    """
    Represents an individual animation used in the :class:`PyxelImage`.

    Attributes
        :frame_id: Index of the frame.
        :name: Name of the animation.
        :length: Number of frames in the animation.
        :base_tile: Which tile the animation begins on.
        :duration_multipliers:
        :frame_duration: Length in milliseconds that the frame will be displayed.
    """

    __slots__ = ('frame_id', 'name', 'length', 'base_tile', 'duration_multipliers', 'frame_duration')

    def __init__(self, n: int, data: Dict[str, Any]):
        self.frame_id = n
        self.name = data['name']
        self.length = data['length']
        self.base_tile = data['baseTile']
        self.duration_multipliers = data['frameDurationMultipliers']
        self.frame_duration = data['frameDuration']

    def to_dict(self) -> Dict:
        """Returns a dictionary with original `.pyxel` docData.json keys."""
        return {'name': self.name, 'length': self.length, 'baseTile': self.base_tile,
                'frameDurationMultipliers': self.duration_multipliers, 'frameDuration': self.frame_duration}
