from __future__ import annotations
from dataclasses import dataclass
import skia

from .paint_source import PaintSource

# Obtained from: https://developer.mozilla.org/en-US/docs/Web/CSS/named-color
NAMED_COLORS = {
    'transparent': '#00000000',
    'aliceblue': '#f0f8ff',
    'antiquewhite': '#faebd7',
    'aqua': '#00ffff',
    'aquamarine': '#7fffd4',
    'azure': '#f0ffff',
    'beige': '#f5f5dc',
    'bisque': '#ffe4c4',
    'black': '#000000',
    'blanchedalmond': '#ffebcd',
    'blue': '#0000ff',
    'blueviolet': '#8a2be2',
    'brown': '#a52a2a',
    'burlywood': '#deb887',
    'cadetblue': '#5f9ea0',
    'chartreuse': '#7fff00',
    'chocolate': '#d2691e',
    'coral': '#ff7f50',
    'cornflowerblue': '#6495ed',
    'cornsilk': '#fff8dc',
    'crimson': '#dc143c',
    'cyan': '#00ffff',   # synonym of aqua
    'darkblue': '#00008b',
    'darkcyan': '#008b8b',
    'darkgoldenrod': '#b8860b',
    'darkgray': '#a9a9a9',
    'darkgreen': '#006400',
    'darkgrey': '#a9a9a9',  # synonym of darkgray
    'darkkhaki': '#bdb76b',
    'darkmagenta': '#8b008b',
    'darkolivegreen': '#556b2f',
    'darkorange': '#ff8c00',
    'darkorchid': '#9932cc',
    'darkred': '#8b0000',
    'darksalmon': '#e9967a',
    'darkseagreen': '#8fbc8f',
    'darkslateblue': '#483d8b',
    'darkslategray': '#2f4f4f',
    'darkslategrey': '#2f4f4f',  # synonym
    'darkturquoise': '#00ced1',
    'darkviolet': '#9400d3',
    'deeppink': '#ff1493',
    'deepskyblue': '#00bfff',
    'dimgray': '#696969',
    'dimgrey': '#696969',  # synonym
    'dodgerblue': '#1e90ff',
    'firebrick': '#b22222',
    'floralwhite': '#fffaf0',
    'forestgreen': '#228b22',
    'fuchsia': '#ff00ff',
    'gainsboro': '#dcdcdc',
    'ghostwhite': '#f8f8ff',
    'gold': '#ffd700',
    'goldenrod': '#daa520',
    'gray': '#808080',
    'green': '#008000',
    'greenyellow': '#adff2f',
    'grey': '#808080',  # synonym of gray
    'honeydew': '#f0fff0',
    'hotpink': '#ff69b4',
    'indianred': '#cd5c5c',
    'indigo': '#4b0082',
    'ivory': '#fffff0',
    'khaki': '#f0e68c',
    'lavender': '#e6e6fa',
    'lavenderblush': '#fff0f5',
    'lawngreen': '#7cfc00',
    'lemonchiffon': '#fffacd',
    'lightblue': '#add8e6',
    'lightcoral': '#f08080',
    'lightcyan': '#e0ffff',
    'lightgoldenrodyellow': '#fafad2',
    'lightgray': '#d3d3d3',
    'lightgreen': '#90ee90',
    'lightgrey': '#d3d3d3',  # synonym
    'lightpink': '#ffb6c1',
    'lightsalmon': '#ffa07a',
    'lightseagreen': '#20b2aa',
    'lightskyblue': '#87cefa',
    'lightslategray': '#778899',
    'lightslategrey': '#778899',  # synonym
    'lightsteelblue': '#b0c4de',
    'lightyellow': '#ffffe0',
    'lime': '#00ff00',
    'limegreen': '#32cd32',
    'linen': '#faf0e6',
    'magenta': '#ff00ff',  # synonym of fuchsia
    'maroon': '#800000',
    'mediumaquamarine': '#66cdaa',
    'mediumblue': '#0000cd',
    'mediumorchid': '#ba55d3',
    'mediumpurple': '#9370db',
    'mediumseagreen': '#3cb371',
    'mediumslateblue': '#7b68ee',
    'mediumspringgreen': '#00fa9a',
    'mediumturquoise': '#48d1cc',
    'mediumvioletred': '#c71585',
    'midnightblue': '#191970',
    'mintcream': '#f5fffa',
    'mistyrose': '#ffe4e1',
    'moccasin': '#ffe4b5',
    'navajowhite': '#ffdead',
    'navy': '#000080',
    'oldlace': '#fdf5e6',
    'olive': '#808000',
    'olivedrab': '#6b8e23',
    'orange': '#ffa500',
    'orangered': '#ff4500',
    'orchid': '#da70d6',
    'palegoldenrod': '#eee8aa',
    'palegreen': '#98fb98',
    'paleturquoise': '#afeeee',
    'palevioletred': '#db7093',
    'papayawhip': '#ffefd5',
    'peachpuff': '#ffdab9',
    'peru': '#cd853f',
    'pink': '#ffc0cb',
    'plum': '#dda0dd',
    'powderblue': '#b0e0e6',
    'purple': '#800080',
    'rebeccapurple': '#663399',
    'red': '#ff0000',
    'rosybrown': '#bc8f8f',
    'royalblue': '#4169e1',
    'saddlebrown': '#8b4513',
    'salmon': '#fa8072',
    'sandybrown': '#f4a460',
    'seagreen': '#2e8b57',
    'seashell': '#fff5ee',
    'sienna': '#a0522d',
    'silver': '#c0c0c0',
    'skyblue': '#87ceeb',
    'slateblue': '#6a5acd',
    'slategray': '#708090',
    'slategrey': '#708090',  # synonym
    'snow': '#fffafa',
    'springgreen': '#00ff7f',
    'steelblue': '#4682b4',
    'tan': '#d2b48c',
    'teal': '#008080',
    'thistle': '#d8bfd8',
    'tomato': '#ff6347',
    'turquoise': '#40e0d0',
    'violet': '#ee82ee',
    'wheat': '#f5deb3',
    'white': '#ffffff',
    'whitesmoke': '#f5f5f5',
    'yellow': '#ffff00',
    'yellowgreen': '#9acd32',
}


@dataclass(frozen=True)
class SolidColor(PaintSource):
    """Represents a solid color with RGBA components.

    This class provides a structured way to handle solid colors, with methods
    for creating instances from various string formats like hex codes or
    standard color names.

    Attributes:
        r (int): The red component of the color (0-255).
        g (int): The green component of the color (0-255).
        b (int): The blue component of the color (0-255).
        a (int): The alpha (opacity) component of the color (0-255), where
            255 is fully opaque. Defaults to 255.
    """
    r: int
    g: int
    b: int
    a: int = 255

    @classmethod
    def _from_hex(cls, hex_str: str) -> SolidColor:
        """Creates a SolidColor object from a hexadecimal string.

        Supports various hex formats: '#RGB', '#RRGGBB', and '#RRGGBBAA'.

        Args:
            hex_str: The hexadecimal color string.

        Returns:
            A new `SolidColor` instance.

        Raises:
            ValueError: If the hex string format is invalid.
        """
        hex_str = hex_str.lstrip('#')

        if len(hex_str) == 3:  # Expand short form like #F0C to #FF00CC
            hex_str = "".join(c * 2 for c in hex_str)

        if len(hex_str) == 8:  # RRGGBBAA
            r, g, b, a = (int(hex_str[i:i + 2], 16) for i in (0, 2, 4, 6))
            return cls(r, g, b, a)
        elif len(hex_str) == 6:  # RRGGBB
            r, g, b = (int(hex_str[i:i + 2], 16) for i in (0, 2, 4))
            return cls(r, g, b)
        else:
            raise ValueError(f"Invalid hex color format: '{hex_str}'")

    @classmethod
    def from_str(cls, value: str) -> SolidColor:
        """Creates a SolidColor object from a general color string.

        This method acts as a factory, supporting standard color names
        (e.g., 'red', 'blue') and hexadecimal codes.

        Args:
            value: The color string to parse.

        Returns:
            A new `SolidColor` instance.

        Raises:
            ValueError: If the color name is unknown or the format is invalid.
        """
        clean_value = value.strip().lower()
        if clean_value.startswith('#'):
            return cls._from_hex(clean_value)

        hex_code = NAMED_COLORS.get(clean_value)
        if hex_code:
            return cls._from_hex(hex_code)

        raise ValueError(f"Unknown color name or format: '{value}'")

    def apply_to_paint(self, paint: skia.Paint, bounds: skia.Rect) -> None:
        """Applies this solid color to a Skia Paint object.

        This method is part of the `PaintSource` interface and is used by the
        rendering engine.

        Args:
            paint: The `skia.Paint` object to modify.
            bounds: The bounding box of the area to be painted. This is not
                used for solid colors but is part of the interface for
                compatibility with gradients.
        """
        paint.setColor(skia.Color(self.r, self.g, self.b, self.a))