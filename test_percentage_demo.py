#!/usr/bin/env python3
"""Simple test script to demonstrate percentage-based coordinates."""

from pictex import Canvas, Shadow, Text

# Test 1: Shadow with percentage offset
print("Test 1: Creating canvas with percentage shadow offset...")
canvas1 = (
    Canvas()
    .font_family("Arial")
    .font_size(120)
    .color("white")
    .padding(20)
    .text_shadows(Shadow(offset=("2%", "2%"), blur_radius=10, color="#000000A0"))
)
image1 = canvas1.render("Percentage Shadow Test")
image1.save("test_percentage_shadow.png")
print("✓ Saved test_percentage_shadow.png")

# Test 2: Box shadow with percentage offset
print("\nTest 2: Creating canvas with percentage box shadow offset...")
canvas2 = (
    Canvas()
    .font_family("Arial")
    .font_size(80)
    .color("black")
    .padding(30)
    .background_color("white")
    .border_radius(15)
    .box_shadows(Shadow(offset=("3%", "3%"), blur_radius=20, color="#00000060"))
)
image2 = canvas2.render("Percentage Box Shadow")
image2.save("test_percentage_box_shadow.png")
print("✓ Saved test_percentage_box_shadow.png")

# Test 3: Position with percentage offset
print("\nTest 3: Creating canvas with percentage position offset...")
canvas3 = (
    Canvas()
    .font_family("Arial")
    .font_size(60)
    .size(800, 600)  # Set explicit canvas size for absolute positioning
)
text_element = (
    Text("Positioned Text")
    .color("blue")
    .background_color("yellow")
    .padding(10)
    .absolute_position("50%", "50%", x_offset="5%", y_offset="5%")
)
image3 = canvas3.render(text_element)
image3.save("test_percentage_position.png")
print("✓ Saved test_percentage_position.png")

# Test 4: Mixed percentage and pixel offsets
print("\nTest 4: Creating canvas with mixed offsets...")
canvas4 = (
    Canvas()
    .font_family("Arial")
    .font_size(100)
    .padding(40)
    .background_color("#EEEEEE")
    .border_radius(20)
    .color("#2c3e50")
    .text_shadows(Shadow(offset=("1%", "1%"), blur_radius=2, color="red"))
    .box_shadows(Shadow(offset=(5, 5), blur_radius=3, color="#00000050"))
)
image4 = canvas4.render("Mixed Offsets")
image4.save("test_mixed_offsets.png")
print("✓ Saved test_mixed_offsets.png")

print("\n✅ All tests completed successfully!")
print("\nGenerated files:")
print("  - test_percentage_shadow.png")
print("  - test_percentage_box_shadow.png")
print("  - test_percentage_position.png")
print("  - test_mixed_offsets.png")

