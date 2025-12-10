"""Tests for percentage-based coordinates in shadows and positioning."""

from pictex import Canvas, Shadow, Text


def test_shadow_with_percentage_offset(file_regression, render_engine):
    """
    Tests that shadow offsets can be specified as percentages.
    The shadow should scale proportionally with the element size.
    """
    canvas = (
        Canvas()
        .font_family("Arial")
        .font_size(120)
        .color("white")
        .padding(20)
        .text_shadows(Shadow(offset=("2%", "2%"), blur_radius=10, color="#000000A0"))
    )
    render_func, check_func = render_engine
    image = render_func(canvas, "Percentage Shadow")
    check_func(file_regression, image)


def test_box_shadow_with_percentage_offset(file_regression, render_engine):
    """
    Tests that box shadow offsets can be specified as percentages.
    """
    canvas = (
        Canvas()
        .font_family("Arial")
        .font_size(80)
        .color("black")
        .padding(30)
        .background_color("white")
        .border_radius(15)
        .box_shadows(Shadow(offset=("3%", "3%"), blur_radius=20, color="#00000060"))
    )
    render_func, check_func = render_engine
    image = render_func(canvas, "Percentage Box Shadow")
    check_func(file_regression, image)


def test_mixed_shadow_offsets(file_regression, render_engine):
    """
    Tests mixing percentage and pixel offsets in multiple shadows.
    """
    canvas = (
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
    render_func, check_func = render_engine
    image = render_func(canvas, "Mixed Offsets")
    check_func(file_regression, image)


def test_position_with_percentage_offset(file_regression, render_engine):
    """
    Tests that position offsets can be specified as percentages.
    """
    canvas = (
        Canvas()
        .font_family("Arial")
        .font_size(60)
        .size(800, 600)  # Set explicit canvas size for absolute positioning
    )
    
    # Create a positioned element with percentage offset
    text_element = (
        Text("Positioned Text")
        .color("blue")
        .background_color("yellow")
        .padding(10)
        .absolute_position("50%", "50%", x_offset="5%", y_offset="5%")
    )
    
    render_func, check_func = render_engine
    image = render_func(canvas, text_element)
    check_func(file_regression, image)

