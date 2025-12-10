import skia
from typing import Optional, Union
from ..models import Shadow

def _convert_offset_to_pixels(offset: Union[float, str], reference_size: float) -> float:
    """Convert offset to pixels. If it's a percentage string, convert based on reference_size."""
    if isinstance(offset, str):
        if not offset.endswith('%'):
            raise ValueError(f"Offset string must end with '%' (e.g., '5%')")
        percentage = float(offset.rstrip('%'))
        return reference_size * (percentage / 100.0)
    return float(offset)

def create_composite_shadow_filter(
    shadows: list[Shadow], 
    should_remove_content: bool = False,
    element_width: Optional[float] = None,
    element_height: Optional[float] = None
) -> Optional[skia.ImageFilter]:
    """Create a composite shadow filter from a list of shadows.
    
    Args:
        shadows: List of Shadow objects to composite
        should_remove_content: Whether to remove the original content (for box shadows)
        element_width: Width of the element (for percentage offset conversion)
        element_height: Height of the element (for percentage offset conversion)
    """
    if len(shadows) == 0:
        return None

    skia_shadow_filters = []
    filter = lambda **kwargs: skia.ImageFilters.DropShadowOnly(**kwargs) if should_remove_content else skia.ImageFilters.DropShadow(**kwargs)
    
    for shadow in shadows:
        # Convert offset to pixels if percentages are used
        dx = shadow.offset[0]
        dy = shadow.offset[1]
        
        # Use element dimensions for percentage conversion, fallback to 0 if not provided
        ref_width = element_width if element_width is not None else 0
        ref_height = element_height if element_height is not None else 0
        
        dx_px = _convert_offset_to_pixels(dx, ref_width)
        dy_px = _convert_offset_to_pixels(dy, ref_height)
        
        skia_shadow_filters.append(
            filter(
                dx=dx_px, dy=dy_px,
                sigmaX=shadow.blur_radius, sigmaY=shadow.blur_radius,
                color=skia.Color(
                    shadow.color.r, shadow.color.g,
                    shadow.color.b, shadow.color.a
                )
            )
        )

    if len(skia_shadow_filters) == 1:
        return skia_shadow_filters[0]

    composite_filter = skia_shadow_filters[0]
    for i in range(1, len(skia_shadow_filters)):
        composite_filter = skia.ImageFilters.Compose(skia_shadow_filters[i], composite_filter)

    return composite_filter