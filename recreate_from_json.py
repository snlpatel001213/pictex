#!/usr/bin/env python3
"""
Script to recreate an image from PicTex JSON metadata, applying variable substitution.
"""

import json
import argparse
import sys
import os
import re

# Add pictex/src to python path
current_dir = os.path.dirname(os.path.abspath(__file__))
pictex_src = os.path.join(current_dir, 'pictex', 'src')
sys.path.append(pictex_src)

from pictex import (
    Canvas, Text, Image, Shadow, SolidColor, LinearGradient, PositionMode
)
import urllib.request
import tempfile
import atexit
import shutil

# Keep track of temp files to clean up
temp_files = []

def cleanup_temp_files():
    for f in temp_files:
        if os.path.exists(f):
            try:
                os.remove(f)
            except:
                pass

atexit.register(cleanup_temp_files)

def get_image_path(src):
    """If src is a URL, download it to a temp file. Otherwise return it."""
    if not src:
        return src
    
    if src.startswith('http://') or src.startswith('https://'):
        try:
            suffix = os.path.splitext(src)[1]
            if not suffix: suffix = '.png'
            # Remove query params from suffix if present
            if '?' in suffix:
                suffix = suffix.split('?')[0]
                
            tf = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
            tf.close()
            
            print(f"Downloading {src} to {tf.name}...")
            # Use a User-Agent to avoid some 403s
            req = urllib.request.Request(src, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req) as response, open(tf.name, 'wb') as out_file:
                shutil.copyfileobj(response, out_file)
            
            temp_files.append(tf.name)
            return tf.name
        except Exception as e:
            print(f"Failed to download image {src}: {e}")
            return src # Fallback, likely will fail in PicTex too but preserves original error flow
            
    return src

def apply_variables(text, child_name, gender):
    """Replace placeholders and apply gender conversion."""
    if not text:
        return text
    
    # 1. Basic Substitution
    text = text.replace('{child_name}', child_name)
    text = text.replace('{gender}', gender)
    
    # 2. Gender Conversion (Male -> Female)
    # Assuming text is written for Male ("He", "Him", "Boy")
    if gender.lower() == 'female':
        # Substitution rules: (Pattern, Replacement)
        # Order matters for overlapping words (though regex \b handles boundaries)
        rules = [
            (r'\b[Hh]e\b', lambda m: 'She' if m.group(0)[0].isupper() else 'she'),
            (r'\b[Hh]im\b', lambda m: 'Her' if m.group(0)[0].isupper() else 'her'),
            (r'\b[Hh]is\b', lambda m: 'Her' if m.group(0)[0].isupper() else 'her'), # "His book" -> "Her book", "It is his" -> "It is her" (Wait, 'It is hers'?)
            # Refinement: "It is his" -> "It is hers". "His book" -> "Her book".
            # This is complex without NLP. For now, let's stick to the prompt's simplicity or commonly accepted simple rules.
            # The prompt says: "He-> She, Him -> Her etc"
            # Let's add:
            (r'\b[Hh]imself\b', lambda m: 'Herself' if m.group(0)[0].isupper() else 'herself'),
            (r'\b[Bb]oy\b', lambda m: 'Girl' if m.group(0)[0].isupper() else 'girl'),
            (r'\b[Ss]on\b', lambda m: 'Daughter' if m.group(0)[0].isupper() else 'daughter'),
            (r'\b[Bb]rother\b', lambda m: 'Sister' if m.group(0)[0].isupper() else 'sister'),
             (r'\b[Nn]ephew\b', lambda m: 'Niece' if m.group(0)[0].isupper() else 'niece'),
        ]
        
        for pattern, replacement_func in rules:
            text = re.sub(pattern, replacement_func, text)

    return text

def parse_percentage(val, base):
    """Parse percentage string to pixel value."""
    if isinstance(val, str) and val.endswith('%'):
        return (float(val.strip('%')) / 100.0) * base
    return float(val) if val is not None else 0

def create_element(el_data, base_width, base_height, child_name, gender):
    """Create a PicTex element from JSON data."""
    el_type = el_data.get('type')
    
    x = parse_percentage(el_data.get('x', '0'), base_width)
    y = parse_percentage(el_data.get('y', '0'), base_height)
    
    pictex_el = None
    
    if el_type == 'text':
        content = apply_variables(el_data.get('content', ''), child_name, gender)
        pictex_el = Text(content)
        
        # Font Style
        # Note: pictex.Text might parse font string or have separate setters
        font_size_val = parse_percentage(el_data.get('font_size', '20'), base_height)
        pictex_el.font_size(font_size_val)
        pictex_el.font_family(el_data.get('font_family', 'Arial'))
        
        # Color
        c = el_data.get('color', '#000000')
        pictex_el.color(SolidColor.from_str(c) if c.startswith('#') else SolidColor(0,0,0))
        
        # Shadow
        shadow_data = el_data.get('shadow')
        if shadow_data:
            sc = shadow_data.get('color', '#000000')
            pictex_el.text_shadows(Shadow(
                blur_radius=shadow_data.get('blur', 0),
                color=SolidColor.from_str(sc) if sc.startswith('#') else SolidColor(0,0,0),
                offset=tuple(shadow_data.get('offset', [2, 2]))
            ))

    elif el_type == 'image':
        src = el_data.get('src') 
        # Handle remote URLs
        local_src = get_image_path(src)
        pictex_el = Image(local_src)
        
        w = parse_percentage(el_data.get('width'), base_width)
        h = parse_percentage(el_data.get('height'), base_height)
        pictex_el.size(width=w, height=h) # Using size to set explicit dimensions
        
        # Shadow for image (box shadow)
        shadow_data = el_data.get('shadow')
        if shadow_data:
             sc = shadow_data.get('color', '#000000')
             pictex_el.box_shadows(Shadow(
                blur_radius=shadow_data.get('blur', 0),
                color=SolidColor.from_str(sc) if sc.startswith('#') else SolidColor(0,0,0),
                offset=tuple(shadow_data.get('offset', [2, 2]))
            ))

    if pictex_el:
        # Rotation - New Feature
        # Support both 'angle' (common) and 'rotation' (PicTex naming)
        angle = float(el_data.get('angle', el_data.get('rotation', 0)))
        if angle != 0:
            pictex_el.rotate(angle)

        # Common properties
        # Position
        pictex_el.absolute_position(0, 0, x, y) # Top-left anchors, then offsets
        
        # Padding
        p = el_data.get('padding')
        if p is None: p = 0
        pictex_el.padding(p, p, p, p)
        
        # Border Radius
        br = el_data.get('border_radius')
        if br is None: br = 0
        # pictex might expect 4 values or 1
        pictex_el.border_radius(br, br, br, br) 
        
        # Background
        bg = el_data.get('background')
        if bg:
            if isinstance(bg, dict) and bg.get('type') == 'linear_gradient':
                pass # Complex gradient parsing, skipped for brevity in this iteration unless needed
            elif isinstance(bg, str) and bg.startswith('#'):
                 pictex_el.background_color(SolidColor.from_str(bg))

        # Effects
        effects = el_data.get('effects')
        if effects:
            pictex_el.brightness(float(effects.get('brightness', 100)))
            pictex_el.contrast(float(effects.get('contrast', 100)))
            pictex_el.saturation(float(effects.get('saturation', 100)))
            pictex_el.warmth(float(effects.get('warmth', 0)))

    return pictex_el

def main():
    parser = argparse.ArgumentParser(description="Recreate Image from JSON with Variables")
    parser.add_argument("input_json", help="Path to input JSON file")
    parser.add_argument("output_image", help="Path to output image file")
    parser.add_argument("--child-name", default="Child", help="Name of the child")
    parser.add_argument("--gender", default="Male", help="Gender of the child (Male/Female)")
    
    args = parser.parse_args()
    
    try:
        with open(args.input_json, 'r') as f:
            data = json.load(f)
            
        print(f"Loaded JSON. Elements: {len(data.get('elements', []))}")
        
        # Base Image Logic
        # We need a canvas. If there is a base image, we might load it into the canvas or as the first element.
        # PicTex Canvas usually starts blank.
        base_img_path = data.get('base_image')
        
        # We need to determine canvas size.
        # If base image exists, use its size? Or 800x600 default?
        # For now, let's assume 800x600 if can't determine, or check 'composition' if it exists.
        # But this export format is flat.
        
        width = 800
        height = 600
        
        canvas = Canvas()
        canvas.size(width=width, height=height)
        
        elements_to_render = []
        
        if base_img_path:
             # Add base image as the first element background
             local_base_path = get_image_path(base_img_path)
             base_img = Image(local_base_path)
             # If we can get size of base_img, we should set canvas size.
             # but PicTex Image object might not load generic IO immediately without render.
             # Let's assume for now we just add it.
             # Warning: base_image path from web (http) vs local file.
             # If 'base_image' is just a reference, we might need to rely on the user ensuring it's valid.
             elements_to_render.append(base_img)
        
        # Process elements
        for el in data.get('elements', []):
            rendered_el = create_element(el, width, height, args.child_name, args.gender)
            if rendered_el:
                elements_to_render.append(rendered_el)
                
        print(f"Rendering {len(elements_to_render)} elements...")
        result_image = canvas.render(*elements_to_render)
        
        result_image.save(args.output_image)
        print(f"Saved to {args.output_image}")
        
    except Exception as e:
        # print(f"Error: {e}")
        import traceback
        traceback.print_exc()[:1000]
        sys.exit(1)

if __name__ == "__main__":
    main()
