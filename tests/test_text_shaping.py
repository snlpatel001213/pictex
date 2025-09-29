from pictex import Canvas, NamedColor
from .conftest import FONT_WITH_LIGATURES_PATH

# TODO: vector image is actually not working for ligatures
def test_ligature_rendering(file_regression, render_engine):
    """
    Tests that ligatures are properly rendered when using a font that supports them.
    Characters like '->' and '==' should be rendered as single ligature glyphs.
    """
    canvas = (
        Canvas()
        .font_family(FONT_WITH_LIGATURES_PATH)
        .font_size(120)
        .color(NamedColor.BLUE)
        .background_color(NamedColor.BEIGE)
        .padding(20)
    )
    render_func, check_func = render_engine
    image = render_func(canvas, "-> ==")
    check_func(file_regression, image)

def test_kerning_support(file_regression, render_engine):
    """
    Tests that kerning is properly applied to character pairs.
    Characters like 'AV' and 'TY' should have adjusted spacing between them.
    """
    canvas = (
        Canvas()
        .font_family("Impact")
        .font_size(120)
        .color(NamedColor.BLUE)
        .background_color(NamedColor.BEIGE)
        .padding(20)
    )
    render_func, check_func = render_engine
    image = render_func(canvas, "AV TY")
    check_func(file_regression, image)

# TODO: vector image is actually not working for this complex emoji
def test_complex_emoji_rendering(file_regression, render_engine):
    """
    Tests that complex emoji sequences (like woman scientist) are properly rendered
    as a single glyph instead of separate emoji characters.
    """
    canvas = (
        Canvas()
        .font_size(120)
        .color(NamedColor.BLUE)
        .background_color(NamedColor.BEIGE)
        .padding(20)
    )
    render_func, check_func = render_engine
    image = render_func(canvas, "👩‍🔬")
    check_func(file_regression, image)

def test_arabic_text_shaping(file_regression, render_engine):
    """
    Tests that Arabic text is properly shaped and rendered with correct
    character connections and forms.
    """
    canvas = (
        Canvas()
        .font_size(120)
        .color(NamedColor.BLUE)
        .background_color(NamedColor.BEIGE)
        .padding(20)
    )
    render_func, check_func = render_engine
    image = render_func(canvas, "كتاب")
    check_func(file_regression, image)
