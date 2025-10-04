from pictex import Canvas, LinearGradient, RadialGradient, SweepGradient, TwoPointConicalGradient

def test_linear_gradient_on_text_fill(file_regression, render_engine):
    """
    A basic test to confirm a linear gradient can be applied to the text fill.
    """
    gradient = LinearGradient(
        colors=["#f12711", "#f5af19"],
        start_point=(0, 0.5),
        end_point=(1, 0.5)
    )

    canvas = (
        Canvas()
        .font_family("Arial")
        .font_size(120)
        .color(gradient)
    )
    render_func, check_func = render_engine
    image = render_func(canvas, "GRADIENT")
    check_func(file_regression, image)

def test_linear_gradient_direction_vertical(file_regression, render_engine):
    """
    Tests that start_point and end_point correctly create a vertical gradient.
    """
    gradient = LinearGradient(
        colors=["#00f6ff", "#0052ff"],
        start_point=(0.5, 0),
        end_point=(0.5, 1)
    )

    canvas = (
        Canvas()
        .font_family("Arial")
        .font_size(120)
        .color(gradient)
    )
    render_func, check_func = render_engine
    image = render_func(canvas, "VERTICAL")
    check_func(file_regression, image)

def test_linear_gradient_with_custom_stops(file_regression, render_engine):
    """
    Verifies that the `stops` parameter works, allowing for non-uniform
    color distribution in the gradient.
    """
    gradient = LinearGradient(
        colors=["#e96443", "#904e95"],
        stops=[0.2, 0.8]
    )

    canvas = (
        Canvas()
        .font_family("Arial")
        .font_size(120)
        .padding(20)
        .background_color("#222222")
        .color(gradient)
    )
    render_func, check_func = render_engine
    image = render_func(canvas, "STOPS")
    check_func(file_regression, image)

def test_radial_gradient_on_background(file_regression, render_engine):
    """
    Tests that radial gradient can be applied to background.
    """
    gradient = RadialGradient(
        colors=["yellow", "orange", "purple"],
        center=(0.5, 0.5),
        radius=0.5
    )

    canvas = (
        Canvas()
        .font_family("Arial")
        .font_size(120)
        .background_color(gradient)
        .padding(30)
        .color("white")
    )
    render_func, check_func = render_engine
    image = render_func(canvas, "RADIAL")
    check_func(file_regression, image)

def test_radial_gradient_with_custom_center(file_regression, render_engine):
    """
    Tests radial gradient with off-center position.
    """
    gradient = RadialGradient(
        colors=["white", "blue"],
        center=(0.3, 0.3),
        radius=0.7
    )

    canvas = (
        Canvas()
        .font_family("Arial")
        .font_size(120)
        .background_color(gradient)
        .padding(30)
        .color("white")
    )
    render_func, check_func = render_engine
    image = render_func(canvas, "OFF-CENTER")
    check_func(file_regression, image)

# TODO: sweep gradient is not working on SVGs
def test_sweep_gradient_color_wheel(file_regression, render_engine):
    """
    Tests sweep gradient creating a color wheel effect.
    """
    gradient = SweepGradient(
        colors=["red", "yellow", "lime", "cyan", "blue", "magenta", "red"]
    )

    canvas = (
        Canvas()
        .font_family("Arial")
        .font_size(120)
        .background_color(gradient)
        .padding(30)
        .color("white")
    )
    render_func, check_func = render_engine
    image = render_func(canvas, "SWEEP")
    check_func(file_regression, image)

# TODO: sweep gradient is not working on SVGs
def test_sweep_gradient_with_stops(file_regression, render_engine):
    """
    Tests sweep gradient with custom color stops.
    """
    gradient = SweepGradient(
        colors=["red", "blue", "red"],
        stops=[0.0, 0.5, 1.0]
    )

    canvas = (
        Canvas()
        .font_family("Arial")
        .font_size(120)
        .background_color(gradient)
        .padding(30)
        .color("white")
    )
    render_func, check_func = render_engine
    image = render_func(canvas, "CUSTOM")
    check_func(file_regression, image)

# TODO: colors are being inverted in SVGs
def test_two_point_conical_gradient(file_regression, render_engine):
    """
    Tests two-point conical gradient.
    """
    gradient = TwoPointConicalGradient(
        colors=["yellow", "blue"],
        start=(0.5, 0.0),
        start_radius=0.0,
        end=(0.5, 0.5),
        end_radius=0.5
    )

    canvas = (
        Canvas()
        .font_family("Arial")
        .font_size(120)
        .background_color(gradient)
        .padding(30)
        .color("white")
    )
    render_func, check_func = render_engine
    image = render_func(canvas, "CONICAL")
    check_func(file_regression, image)

# TODO: colors are being inverted in SVGs
def test_two_point_conical_gradient_spotlight(file_regression, render_engine):
    """
    Tests two-point conical gradient with spotlight effect.
    """
    gradient = TwoPointConicalGradient(
        colors=["white", "black"],
        start=(0.3, 0.3),
        start_radius=0.0,
        end=(0.5, 0.5),
        end_radius=0.7
    )

    canvas = (
        Canvas()
        .font_family("Arial")
        .font_size(120)
        .background_color(gradient)
        .padding(30)
        .color("white")
    )
    render_func, check_func = render_engine
    image = render_func(canvas, "SPOTLIGHT")
    check_func(file_regression, image)
