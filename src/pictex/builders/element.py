from .stylable import Stylable
from .with_position_mixin import WithPositionMixin
from .with_size_mixin import WithSizeMixin
from ..nodes import Node

class Element(Stylable, WithPositionMixin, WithSizeMixin):
    
    def __init__(self):
        super().__init__()
        self._rotation = 0.0

    def rotate(self, degrees: float) -> "Element":
        """
        Rotates the element by the specified degrees.
        
        Args:
            degrees: The angle in degrees to rotate the element.
            
        Returns:
            The element instance for chaining.
        """
        self._rotation = degrees
        return self

    def _to_node(self) -> Node:
        raise NotImplementedError()
