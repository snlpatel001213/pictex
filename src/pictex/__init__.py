"""
pictex: A Python library for creating complex visual compositions and beautifully styled images.
"""

from .builders import Canvas, Text, Row, Column, Image, Element
from .models.public import *
from .bitmap_image import BitmapImage
from .vector_image import VectorImage

__version__ = "1.3.3"

__all__ = [
    "Canvas", "Text", "Row", "Column", "Image", "Element",
    
    "Shadow", "OutlineStroke",
    "Style",
    "FontStyle", "FontWeight", "FontSmoothing", "TextAlign", "TextWrap",
    "PaintSource",
    "SolidColor", "NamedColor",
    "LinearGradient",
    "TextDecoration",
    "CropMode",
    "Box",
    "Position", "PositionMode",
    "SizeValue", "SizeValueMode",
    "Margin", "Padding", "HorizontalDistribution", "VerticalAlignment", "HorizontalAlignment", "VerticalDistribution",
    "BackgroundImage", "BackgroundImageSizeMode",
    "Border", "BorderStyle", "BorderRadiusValue", "BorderRadius",
    "RenderNode",
    "NodeType",

    "BitmapImage",
    "VectorImage",
]
