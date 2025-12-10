
import json
import sys
import os
from pictex import Canvas, Text, Image, Column, Row, Shadow, LinearGradient
import requests
from io import BytesIO

import base64

def load_image(src):
    if src.startswith('http'):
        response = requests.get(src)
        return Image(BytesIO(response.content))
    elif src.startswith('data:image'):
        # Handle base64
        try:
            header, encoded = src.split(',', 1)
            data = base64.b64decode(encoded)
            return Image(BytesIO(data))
        except Exception as e:
            print(f"Error decoding base64 image: {e}")
            return None
    else:
        return Image(src)

def parse_color(color_str):
    return color_str

def create_shadow(shadow_data):
    if not shadow_data:
        return None
    return Shadow(
        offset=shadow_data.get('offset', (2, 2)),
        blur_radius=shadow_data.get('blur', 0),
        color=shadow_data.get('color', 'black')
    )

def create_background(bg_data):
    if not bg_data:
        return None
    if isinstance(bg_data, dict) and bg_data.get('type') == 'linear_gradient':
        return LinearGradient(bg_data['colors'])
    return bg_data # Solid color string

def parse_percentage(value, total):
    if isinstance(value, str) and value.endswith('%'):
        return float(value.rstrip('%')) / 100 * total
    return float(value)

def recreate_from_json(json_path, output_path="recreated_result.png"):
    with open(json_path, 'r') as f:
        data = json.load(f)

    # 1. Load Base Image
    base_src = data.get('base_image')
    base_image_node = load_image(base_src)
    
    # Get dimensions
    # Access internal skia image to get dimensions
    skia_image = base_image_node._style.background_image.get().get_skia_image()
    base_width = skia_image.width()
    base_height = skia_image.height()
    
    elements = []
    
    # Add base image first
    elements.append(base_image_node)
    
    for item in data.get('elements', []):
        node = None
        if item['type'] == 'text':
            node = Text(item['content'])
            
            # Font Size
            font_size = parse_percentage(item['font_size'], base_height)
            node.font_size(font_size)
            
            node.font_family(item['font_family'])
            node.color(item['color'])
            
            shadow = create_shadow(item.get('shadow'))
            if shadow:
                node.text_shadows(shadow)
                
        elif item['type'] == 'image':
            node = load_image(item['src'])
            
            # Size
            w = parse_percentage(item['width'], base_width)
            h = parse_percentage(item['height'], base_height)
            node.size(width=w, height=h)
            
            shadow = create_shadow(item.get('shadow'))
            if shadow:
                node.box_shadows(shadow)

        if node:
            # Common styles
            if item.get('padding'):
                node.padding(item['padding'])
            if item.get('border_radius'):
                node.border_radius(item['border_radius'])
            
            bg = create_background(item.get('background'))
            if bg:
                node.background_color(bg)
            
            # Absolute Position
            x = parse_percentage(item['x'], base_width)
            y = parse_percentage(item['y'], base_height)
            node.absolute_position(x, y)
            
            elements.append(node)

    # Create the composition
    root = Column(*elements)
    
    # Render
    canvas = Canvas()
    
    try:
        final_image = canvas.render(root)
        final_image.save(output_path)
        print(f"Successfully recreated image at {output_path}")
    except Exception as e:
        print(f"Error rendering image: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python recreate_from_json.py <json_file>")
    else:
        recreate_from_json(sys.argv[1])
