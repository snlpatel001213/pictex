
import json
import sys
import os
from pictex import Canvas, Text, Image, Column, Row, Shadow, LinearGradient, Color
import requests
from io import BytesIO

def load_image(src):
    if src.startswith('http'):
        response = requests.get(src)
        return Image(BytesIO(response.content))
    elif src.startswith('data:image'):
        # Handle base64 if needed, but for now assume URL or path
        # For simplicity in this demo script, we might skip complex base64 handling
        # unless the demo exports it. The demo exports URLs mostly.
        print("Base64 images not fully supported in this simple script yet.")
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

def recreate_from_json(json_path, output_path="recreated_result.png"):
    with open(json_path, 'r') as f:
        data = json.load(f)

    # 1. Load Base Image
    base_src = data.get('base_image')
    # For demo purposes, if base_src is a relative URL from the server, we might need to fix it.
    # But the demo uses unsplash URLs.
    
    # We create a container that holds everything. 
    # Since PicTex is component based, we can use a Box or just a Canvas with absolute positioning.
    # However, PicTex's Canvas.render() takes a root node.
    # We will use the base image as the "container" effectively, or just a wrapper.
    
    # Actually, to support absolute positioning on top of an image, 
    # we should probably use a Container/Box with the image as background or just the image itself 
    # if it supports children (it doesn't usually).
    # PicTex's `Image` is a leaf node.
    # But we can use a `Box` (or `Column`/`Row` acting as one) with dimensions of the image 
    # and put the image inside it, or set the image as background?
    # PicTex `Image` component is best.
    # Let's use a `Box` (from `pictex.nodes`) or just a generic `Column` with no gap.
    # But wait, `pictex` Python API for absolute positioning works on children of a container.
    
    # Let's create a root container.
    # We need to know the size of the base image to set the root container size, 
    # so percentages work correctly.
    
    base_image_node = load_image(base_src)
    # We need to fetch dimensions. PicTex Image doesn't expose them easily before layout?
    # Actually it does if we load it.
    # For this script, let's assume we render it once to get size or just rely on the fact 
    # that the root container will size itself to the image if we put the image in it?
    # But we want to overlay things.
    
    # Strategy:
    # Create a root `Box` (or `Column`).
    # Add the base image as the first child.
    # Add other elements as subsequent children, but with `absolute_position`.
    # This relies on the container allowing overlap. 
    # Standard `Column` stacks things. 
    # Does PicTex have a `Stack` or `Overlay`?
    # Looking at the API, `absolute_position` takes a node out of flow?
    # If so, we can add them to a Column and they won't affect layout if absolute.
    
    # Let's try:
    # Root = Column(base_image, *other_elements)
    # where other_elements have .absolute_position(...)
    
    elements = []
    
    # Add base image first (it's in flow)
    elements.append(base_image_node)
    
    for item in data.get('elements', []):
        node = None
        if item['type'] == 'text':
            node = Text(item['content'])
            node.font_size(item['font_size']) # Percentage string
            node.font_family(item['font_family'])
            node.color(item['color'])
            
            shadow = create_shadow(item.get('shadow'))
            if shadow:
                node.text_shadows(shadow)
                
        elif item['type'] == 'image':
            node = load_image(item['src'])
            node.width(item['width'])
            node.height(item['height'])
            
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
            # item['x'] and item['y'] are strings like "50.00%"
            node.absolute_position(item['x'], item['y'])
            
            elements.append(node)

    # Create the composition
    # We use a Column but since elements (except base image) are absolute, 
    # they should overlay.
    root = Column(*elements)
    
    # Render
    # We need a canvas.
    canvas = Canvas()
    
    # We might need to register fonts if they are custom, 
    # but standard ones might work or fallback.
    
    try:
        final_image = canvas.render(root)
        final_image.save(output_path)
        print(f"Successfully recreated image at {output_path}")
    except Exception as e:
        print(f"Error rendering image: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python recreate_from_json.py <json_file>")
    else:
        recreate_from_json(sys.argv[1])
