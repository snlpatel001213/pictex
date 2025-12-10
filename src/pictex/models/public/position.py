from dataclasses import dataclass
from enum import Enum
from typing import Tuple, Union

class PositionMode(str, Enum):
    ABSOLUTE = 'absolute'
    RELATIVE = 'relative'

@dataclass
class Position:
    container_anchor_x: float = 0.0
    container_anchor_y: float = 0.0

    content_anchor_x: float = 0.0
    content_anchor_y: float = 0.0

    x_offset: Union[float, str] = 0.0
    y_offset: Union[float, str] = 0.0

    mode: PositionMode = PositionMode.ABSOLUTE

    def get_relative_position(self, content_width: int, content_height: int, container_width: int, container_height: int) -> Tuple[float, float]:
        container_point_x = container_width * self.container_anchor_x
        container_point_y = container_height * self.container_anchor_y

        content_offset_x = content_width * self.content_anchor_x
        content_offset_y = content_height * self.content_anchor_y

        # Convert percentage offsets to pixels
        x_offset_px = self._convert_offset_to_pixels(self.x_offset, container_width)
        y_offset_px = self._convert_offset_to_pixels(self.y_offset, container_height)

        final_x = container_point_x - content_offset_x + x_offset_px
        final_y = container_point_y - content_offset_y + y_offset_px

        return final_x, final_y
    
    def _convert_offset_to_pixels(self, offset: Union[float, str], reference_size: float) -> float:
        """Convert offset to pixels. If it's a percentage string, convert based on reference_size."""
        if isinstance(offset, str):
            if not offset.endswith('%'):
                raise ValueError(f"Offset string must end with '%' (e.g., '5%')")
            percentage = float(offset.rstrip('%'))
            return reference_size * (percentage / 100.0)
        return float(offset)
