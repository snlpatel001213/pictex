
import sys
import os
import json

# Add pictex/src to python path
current_dir = os.path.dirname(os.path.abspath(__file__))
pictex_src = os.path.join(current_dir, 'pictex', 'src')
sys.path.append(pictex_src)

from pictex import Canvas, Text, Image, SolidColor

def test_rotation():
    print("Testing PicTex Rotation...")
    try:
        # Create a simple test
        canvas = Canvas()
        canvas.size(width=800, height=600)
        canvas.background_color(SolidColor.from_str("white"))
        
        # Rotated Text
        t = Text("Rotated Text").font_size(60).color("blue")
        t.absolute_position(300, 200)
        t.rotate(45) # 45 degrees
        
        # Rotated Image (just a placeholder shape if no image file, but let's try to load one if exists, or just use text)
        # We will just verify text rotation first as it uses the same underlying Node rotation logic.
        
        t2 = Text("Normal Text").font_size(40).color("black")
        t2.absolute_position(50, 50)
        
        t3 = Text("90 Deg").font_size(40).color("red")
        t3.absolute_position(100, 400)
        t3.rotate(90)

        canvas.render(t2, t, t3).save("test_rotation_result.png")
        print("Successfully rendered test_rotation_result.png")
        
    except Exception as e:
        print(f"FAILED: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    test_rotation()
