#!/usr/bin/env python3
"""
Example script showing how to load and use templates generated from JavaScript pictext.

This demonstrates the interoperability between JavaScript and Python versions.
"""

import json
from pictex import (
    Canvas, Text, Image, Row, Column,
    Shadow, SolidColor, LinearGradient,
    FontWeight, FontStyle, TextAlign, TextWrap,
    BorderStyle, BackgroundImageSizeMode,
    PositionMode
)


def load_color(color_data):
    """Load a color from JSON data."""
    if color_data['type'] == 'SolidColor':
        return SolidColor(
            color_data['r'],
            color_data['g'],
            color_data['b'],
            color_data.get('a', 255)
        )
    elif color_data['type'] == 'LinearGradient':
        colors = [load_color(c) for c in color_data['colors']]
        return LinearGradient(
            colors=colors,
            stops=color_data.get('stops'),
            start_point=tuple(color_data.get('startPoint', [0.0, 0.5])),
            end_point=tuple(color_data.get('endPoint', [1.0, 0.5]))
        )
    return None


def load_shadow(shadow_data):
    """Load a shadow from JSON data."""
    offset = tuple(shadow_data['offset'])
    blur_radius = shadow_data['blurRadius']
    color = load_color(shadow_data['color'])
    return Shadow(offset=offset, blur_radius=blur_radius, color=color)


def load_text_decoration(decoration_data):
    """Load a text decoration from JSON data."""
    from pictex import TextDecoration
    thickness = decoration_data['thickness']
    color = load_color(decoration_data['color']) if decoration_data.get('color') else None
    return TextDecoration(thickness=thickness, color=color)


def load_outline_stroke(stroke_data):
    """Load an outline stroke from JSON data."""
    from pictex import OutlineStroke
    width = stroke_data['width']
    color = load_color(stroke_data['color'])
    return OutlineStroke(width=width, color=color)


def load_padding(padding_data):
    """Load padding from JSON data."""
    from pictex import Padding
    return Padding(
        top=padding_data['top'],
        right=padding_data['right'],
        bottom=padding_data['bottom'],
        left=padding_data['left']
    )


def load_margin(margin_data):
    """Load margin from JSON data."""
    from pictex import Margin
    return Margin(
        top=margin_data['top'],
        right=margin_data['right'],
        bottom=margin_data['bottom'],
        left=margin_data['left']
    )


def load_border(border_data):
    """Load border from JSON data."""
    from pictex import Border, BorderStyle
    width = border_data['width']
    color = load_color(border_data['color'])
    style = BorderStyle(border_data['style'])
    return Border(width=width, color=color, style=style)


def load_border_radius(radius_data):
    """Load border radius from JSON data."""
    from pictex import BorderRadius, BorderRadiusValue
    
    def load_radius_value(value_data):
        return BorderRadiusValue(
            value=value_data['value'],
            mode=value_data['mode']
        )
    
    return BorderRadius(
        top_left=load_radius_value(radius_data['topLeft']),
        top_right=load_radius_value(radius_data['topRight']),
        bottom_right=load_radius_value(radius_data['bottomRight']),
        bottom_left=load_radius_value(radius_data['bottomLeft'])
    )


def load_position(position_data):
    """Load position from JSON data."""
    from pictex import Position, PositionMode
    return Position(
        container_anchor_x=position_data['containerAnchorX'],
        container_anchor_y=position_data['containerAnchorY'],
        content_anchor_x=position_data['contentAnchorX'],
        content_anchor_y=position_data['contentAnchorY'],
        x_offset=position_data['xOffset'],
        y_offset=position_data['yOffset'],
        mode=PositionMode(position_data['mode'])
    )


def load_size_value(size_data):
    """Load size value from JSON data."""
    from pictex import SizeValue, SizeValueMode
    return SizeValue(
        mode=SizeValueMode(size_data['mode']),
        value=size_data['value']
    )


def apply_style_to_element(element, style_data):
    """Apply style data to an element."""
    if 'fontFamily' in style_data:
        element.font_family(style_data['fontFamily'])
    if 'fontFallbacks' in style_data:
        element.font_fallbacks(*style_data['fontFallbacks'])
    if 'fontSize' in style_data:
        element.font_size(style_data['fontSize'])
    if 'fontWeight' in style_data:
        element.font_weight(style_data['fontWeight'])
    if 'fontStyle' in style_data:
        element.font_style(FontStyle(style_data['fontStyle']))
    if 'lineHeight' in style_data:
        element.line_height(style_data['lineHeight'])
    if 'textAlign' in style_data:
        element.text_align(TextAlign(style_data['textAlign']))
    if 'textWrap' in style_data:
        element.text_wrap(TextWrap(style_data['textWrap']))
    if 'color' in style_data:
        element.color(load_color(style_data['color']))
    if 'textShadows' in style_data:
        shadows = [load_shadow(s) for s in style_data['textShadows']]
        element.text_shadows(*shadows)
    if 'boxShadows' in style_data:
        shadows = [load_shadow(s) for s in style_data['boxShadows']]
        element.box_shadows(*shadows)
    if 'textStroke' in style_data and style_data['textStroke']:
        stroke = load_outline_stroke(style_data['textStroke'])
        element.text_stroke(stroke.width, stroke.color)
    if 'underline' in style_data and style_data['underline']:
        deco = load_text_decoration(style_data['underline'])
        element.underline(deco.thickness, deco.color)
    if 'strikethrough' in style_data and style_data['strikethrough']:
        deco = load_text_decoration(style_data['strikethrough'])
        element.strikethrough(deco.thickness, deco.color)
    if 'padding' in style_data:
        padding = load_padding(style_data['padding'])
        element.padding(padding.top, padding.right, padding.bottom, padding.left)
    if 'margin' in style_data:
        margin = load_margin(style_data['margin'])
        element.margin(margin.top, margin.right, margin.bottom, margin.left)
    if 'backgroundColor' in style_data and style_data['backgroundColor']:
        element.background_color(load_color(style_data['backgroundColor']))
    if 'backgroundImage' in style_data and style_data['backgroundImage']:
        bg_img = style_data['backgroundImage']
        size_mode = BackgroundImageSizeMode(bg_img['sizeMode'])
        element.background_image(bg_img['path'], size_mode)
    if 'border' in style_data and style_data['border']:
        border = load_border(style_data['border'])
        element.border(border.width, border.color, border.style)
    if 'borderRadius' in style_data and style_data['borderRadius']:
        radius = load_border_radius(style_data['borderRadius'])
        element.border_radius(
            radius.top_left.value if radius.top_left.mode == 'absolute' else f"{radius.top_left.value}%",
            radius.top_right.value if radius.top_right.mode == 'absolute' else f"{radius.top_right.value}%",
            radius.bottom_right.value if radius.bottom_right.mode == 'absolute' else f"{radius.bottom_right.value}%",
            radius.bottom_left.value if radius.bottom_left.mode == 'absolute' else f"{radius.bottom_left.value}%"
        )
    if 'position' in style_data and style_data['position']:
        position = load_position(style_data['position'])
        if position.mode == PositionMode.ABSOLUTE:
            element.absolute_position(
                position.container_anchor_x,
                position.container_anchor_y,
                position.x_offset,
                position.y_offset
            )
        else:
            element.position(
                position.container_anchor_x,
                position.container_anchor_y,
                position.x_offset,
                position.y_offset
            )
    if 'width' in style_data and style_data['width']:
        size_val = load_size_value(style_data['width'])
        if size_val.mode == SizeValueMode.ABSOLUTE:
            element.size(width=size_val.value)
        elif size_val.mode == SizeValueMode.PERCENT:
            element.size(width=f"{size_val.value}%")
        else:
            element.size(width=size_val.mode.value)
    if 'height' in style_data and style_data['height']:
        size_val = load_size_value(style_data['height'])
        if size_val.mode == SizeValueMode.ABSOLUTE:
            element.size(height=size_val.value)
        elif size_val.mode == SizeValueMode.PERCENT:
            element.size(height=f"{size_val.value}%")
        else:
            element.size(height=size_val.mode.value)


def load_element(elem_data):
    """Load an element from JSON data."""
    elem_type = elem_data['type']
    
    if elem_type == 'Text':
        element = Text(elem_data['text'])
    elif elem_type == 'Image':
        element = Image(elem_data['path'])
        if 'resizeFactor' in elem_data and elem_data['resizeFactor'] != 1.0:
            element.resize(elem_data['resizeFactor'])
    elif elem_type == 'Row':
        children = [load_element(c) for c in elem_data.get('children', [])]
        element = Row(*children)
        if 'style' in elem_data and 'horizontalDistribution' in elem_data['style']:
            from pictex import HorizontalDistribution
            element.horizontal_distribution(HorizontalDistribution(elem_data['style']['horizontalDistribution']))
        if 'style' in elem_data and 'verticalAlignment' in elem_data['style']:
            from pictex import VerticalAlignment
            element.vertical_align(VerticalAlignment(elem_data['style']['verticalAlignment']))
    elif elem_type == 'Column':
        children = [load_element(c) for c in elem_data.get('children', [])]
        element = Column(*children)
        if 'style' in elem_data and 'verticalDistribution' in elem_data['style']:
            from pictex import VerticalDistribution
            element.vertical_distribution(VerticalDistribution(elem_data['style']['verticalDistribution']))
        if 'style' in elem_data and 'horizontalAlignment' in elem_data['style']:
            from pictex import HorizontalAlignment
            element.horizontal_align(HorizontalAlignment(elem_data['style']['horizontalAlignment']))
    else:
        raise ValueError(f"Unknown element type: {elem_type}")
    
    # Apply style
    if 'style' in elem_data:
        apply_style_to_element(element, elem_data['style'])
    
    return element


def load_template(template_path):
    """Load a template from a JSON file and return a Canvas with elements."""
    with open(template_path, 'r') as f:
        template = json.load(f)
    
    # Create canvas
    canvas = Canvas()
    
    # Apply canvas styles
    if 'composition' in template and 'canvasStyle' in template['composition']:
        apply_style_to_element(canvas, template['composition']['canvasStyle'])
    
    # Load elements
    elements = []
    if 'composition' in template and 'elements' in template['composition']:
        for elem_data in template['composition']['elements']:
            elements.append(load_element(elem_data))
    
    return canvas, elements


def main():
    """Example usage."""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python load_js_template.py <template.json> [output.png]")
        print("\nExample:")
        print("  python load_js_template.py pictext_template.json output.png")
        sys.exit(1)
    
    template_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else 'output.png'
    
    try:
        print(f"Loading template from {template_path}...")
        canvas, elements = load_template(template_path)
        
        print(f"Rendering composition with {len(elements)} element(s)...")
        image = canvas.render(*elements)
        
        print(f"Saving to {output_path}...")
        image.save(output_path)
        
        print("✓ Success!")
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()

