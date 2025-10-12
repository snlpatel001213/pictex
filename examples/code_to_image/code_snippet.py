from pictex import Canvas, Row, Text

def transform(values: list[int]) -> list[int]:
    """Applies a transformation."""
    return [v * 2 for v in values if v >= 0 and v != 5]

def render_result(values: list[int]) -> Row:
    result = transform(values)
    arrow = Text("->").color("#C678DD")
    text = Text(f"{result}").color("#98C379")
    return Row(Text("Result").color("#61AFEF"), arrow, text).gap(6)

canvas = Canvas().font_family("FiraCode-VariableFont_wght.ttf")
canvas.render(render_result([1, -2, 5, 10])).show()
