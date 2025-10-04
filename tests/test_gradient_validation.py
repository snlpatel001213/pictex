import pytest
from pictex import LinearGradient, RadialGradient, SweepGradient, TwoPointConicalGradient


class TestLinearGradientValidation:
    def test_requires_at_least_two_colors(self):
        with pytest.raises(ValueError, match="At least 2 colors are required"):
            LinearGradient(colors=["red"])

    def test_stops_length_must_match_colors(self):
        with pytest.raises(ValueError, match="Length of 'stops'.*must match length of 'colors'"):
            LinearGradient(
                colors=["red", "blue"],
                stops=[0.0, 0.5, 1.0]
            )

    def test_stops_must_be_between_0_and_1(self):
        with pytest.raises(ValueError, match="All values in 'stops' must be between 0.0 and 1.0"):
            LinearGradient(
                colors=["red", "blue"],
                stops=[0.0, 1.5]
            )

    def test_stops_must_be_increasing(self):
        with pytest.raises(ValueError, match="Values in 'stops' must be strictly increasing"):
            LinearGradient(
                colors=["red", "blue", "green"],
                stops=[0.0, 0.5, 0.3]
            )

    def test_start_point_must_be_tuple_of_2(self):
        with pytest.raises(ValueError, match="start_point must be a tuple of 2 values"):
            LinearGradient(
                colors=["red", "blue"],
                start_point=(0.5,)
            )

    def test_end_point_must_be_tuple_of_2(self):
        with pytest.raises(ValueError, match="end_point must be a tuple of 2 values"):
            LinearGradient(
                colors=["red", "blue"],
                end_point=(0.5, 0.5, 0.5)
            )

    def test_start_point_values_must_be_between_0_and_1(self):
        with pytest.raises(ValueError, match="start_point values must be between 0.0 and 1.0"):
            LinearGradient(
                colors=["red", "blue"],
                start_point=(-0.1, 0.5)
            )

    def test_end_point_values_must_be_between_0_and_1(self):
        with pytest.raises(ValueError, match="end_point values must be between 0.0 and 1.0"):
            LinearGradient(
                colors=["red", "blue"],
                end_point=(0.5, 1.5)
            )

    def test_accepts_string_colors(self):
        gradient = LinearGradient(colors=["red", "#00FF00"])
        assert len(gradient.colors) == 2

    def test_valid_gradient_with_all_parameters(self):
        gradient = LinearGradient(
            colors=["red", "blue", "green"],
            stops=[0.0, 0.5, 1.0],
            start_point=(0.0, 0.0),
            end_point=(1.0, 1.0)
        )
        assert len(gradient.colors) == 3


class TestRadialGradientValidation:
    def test_requires_at_least_two_colors(self):
        with pytest.raises(ValueError, match="At least 2 colors are required"):
            RadialGradient(colors=["red"])

    def test_center_must_be_tuple_of_2(self):
        with pytest.raises(ValueError, match="center must be a tuple of 2 values"):
            RadialGradient(
                colors=["red", "blue"],
                center=(0.5,)
            )

    def test_center_values_must_be_between_0_and_1(self):
        with pytest.raises(ValueError, match="center values must be between 0.0 and 1.0"):
            RadialGradient(
                colors=["red", "blue"],
                center=(1.5, 0.5)
            )

    def test_radius_must_be_positive(self):
        with pytest.raises(ValueError, match="Radius must be between 0.0 and 1.0"):
            RadialGradient(
                colors=["red", "blue"],
                radius=0.0
            )

    def test_radius_must_be_at_most_1(self):
        with pytest.raises(ValueError, match="Radius must be between 0.0 and 1.0"):
            RadialGradient(
                colors=["red", "blue"],
                radius=1.5
            )

    def test_stops_must_be_increasing(self):
        with pytest.raises(ValueError, match="Values in 'stops' must be strictly increasing"):
            RadialGradient(
                colors=["red", "blue", "green"],
                stops=[0.0, 0.8, 0.5]
            )

    def test_valid_gradient_with_all_parameters(self):
        gradient = RadialGradient(
            colors=["red", "blue"],
            stops=[0.0, 1.0],
            center=(0.3, 0.7),
            radius=0.8
        )
        assert len(gradient.colors) == 2


class TestSweepGradientValidation:
    def test_requires_at_least_two_colors(self):
        with pytest.raises(ValueError, match="At least 2 colors are required"):
            SweepGradient(colors=["red"])

    def test_center_must_be_tuple_of_2(self):
        with pytest.raises(ValueError, match="center must be a tuple of 2 values"):
            SweepGradient(
                colors=["red", "blue"],
                center=(0.5, 0.5, 0.5)
            )

    def test_center_values_must_be_between_0_and_1(self):
        with pytest.raises(ValueError, match="center values must be between 0.0 and 1.0"):
            SweepGradient(
                colors=["red", "blue"],
                center=(-0.1, 0.5)
            )

    def test_stops_length_must_match_colors(self):
        with pytest.raises(ValueError, match="Length of 'stops'.*must match length of 'colors'"):
            SweepGradient(
                colors=["red", "blue"],
                stops=[0.0, 0.5, 1.0]
            )

    def test_stops_must_be_increasing(self):
        with pytest.raises(ValueError, match="Values in 'stops' must be strictly increasing"):
            SweepGradient(
                colors=["red", "blue", "green"],
                stops=[0.0, 0.5, 0.3]
            )

    def test_valid_gradient_with_all_parameters(self):
        gradient = SweepGradient(
            colors=["red", "yellow", "blue"],
            stops=[0.0, 0.3, 1.0],
            center=(0.5, 0.5)
        )
        assert len(gradient.colors) == 3


class TestTwoPointConicalGradientValidation:
    def test_requires_at_least_two_colors(self):
        with pytest.raises(ValueError, match="At least 2 colors are required"):
            TwoPointConicalGradient(colors=["red"])

    def test_start_must_be_tuple_of_2(self):
        with pytest.raises(ValueError, match="start must be a tuple of 2 values"):
            TwoPointConicalGradient(
                colors=["red", "blue"],
                start=(0.5,)
            )

    def test_end_must_be_tuple_of_2(self):
        with pytest.raises(ValueError, match="end must be a tuple of 2 values"):
            TwoPointConicalGradient(
                colors=["red", "blue"],
                end=(0.5,)
            )

    def test_start_values_must_be_between_0_and_1(self):
        with pytest.raises(ValueError, match="start values must be between 0.0 and 1.0"):
            TwoPointConicalGradient(
                colors=["red", "blue"],
                start=(1.1, 0.5)
            )

    def test_end_values_must_be_between_0_and_1(self):
        with pytest.raises(ValueError, match="end values must be between 0.0 and 1.0"):
            TwoPointConicalGradient(
                colors=["red", "blue"],
                end=(0.5, -0.1)
            )

    def test_start_radius_must_be_non_negative(self):
        with pytest.raises(ValueError, match="start_radius must be between 0.0 and 1.0"):
            TwoPointConicalGradient(
                colors=["red", "blue"],
                start_radius=-0.1
            )

    def test_start_radius_must_be_at_most_1(self):
        with pytest.raises(ValueError, match="start_radius must be between 0.0 and 1.0"):
            TwoPointConicalGradient(
                colors=["red", "blue"],
                start_radius=1.5
            )

    def test_end_radius_must_be_non_negative(self):
        with pytest.raises(ValueError, match="end_radius must be between 0.0 and 1.0"):
            TwoPointConicalGradient(
                colors=["red", "blue"],
                end_radius=-0.1
            )

    def test_end_radius_must_be_at_most_1(self):
        with pytest.raises(ValueError, match="end_radius must be between 0.0 and 1.0"):
            TwoPointConicalGradient(
                colors=["red", "blue"],
                end_radius=2.0
            )

    def test_stops_must_be_increasing(self):
        with pytest.raises(ValueError, match="Values in 'stops' must be strictly increasing"):
            TwoPointConicalGradient(
                colors=["red", "blue", "green"],
                stops=[0.0, 0.9, 0.5]
            )

    def test_valid_gradient_with_all_parameters(self):
        gradient = TwoPointConicalGradient(
            colors=["red", "blue"],
            stops=[0.0, 1.0],
            start=(0.3, 0.3),
            start_radius=0.0,
            end=(0.7, 0.7),
            end_radius=0.9
        )
        assert len(gradient.colors) == 2
