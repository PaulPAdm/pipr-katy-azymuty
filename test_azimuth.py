import unittest

from angle import Angle
from azimuth import Azimuth


class TestAzimuthCreation(unittest.TestCase):
    def test_default_is_north(self):
        self.assertEqual(str(Azimuth()), '000°00\'00"')

    def test_positional_and_keyword_arguments(self):
        self.assertEqual(Azimuth(10, 15), Azimuth(degrees=10, minutes=15))
        self.assertEqual(Azimuth(minutes=30), Azimuth(0, 30, 0))
        self.assertEqual(Azimuth(seconds=45), Azimuth(0, 0, 45))

    def test_minutes_and_seconds_overflow_is_normalized(self):
        self.assertEqual(str(Azimuth(10, 90)), '011°30\'00"')
        self.assertEqual(str(Azimuth(10, 59, 60)), '011°00\'00"')

    def test_full_circle_wraps_to_zero(self):
        self.assertEqual(Azimuth(360), Azimuth(0))
        self.assertEqual(Azimuth(720, 30), Azimuth(0, 30))
        self.assertEqual(Azimuth(seconds=360 * 3600), Azimuth())

    def test_values_above_360_are_wrapped(self):
        self.assertEqual(str(Azimuth(370)), '010°00\'00"')

    def test_negative_values_are_wrapped(self):
        self.assertEqual(str(Azimuth(-10)), '350°00\'00"')
        self.assertEqual(str(Azimuth(minutes=-1)), '359°59\'00"')
        self.assertEqual(str(Azimuth(seconds=-1)), '359°59\'59"')

    def test_non_integer_raises_type_error(self):
        with self.assertRaises(TypeError):
            Azimuth(10.5)
        with self.assertRaises(TypeError):
            Azimuth(minutes="30")

    def test_to_seconds(self):
        self.assertEqual(Azimuth(90).to_seconds(), 324000)
        self.assertEqual(Azimuth(359, 59, 59).to_seconds(), 360 * 3600 - 1)


class TestAzimuthFormatting(unittest.TestCase):
    def test_three_digit_degrees(self):
        self.assertEqual(str(Azimuth(40)), '040°00\'00"')
        self.assertEqual(str(Azimuth(5)), '005°00\'00"')
        self.assertEqual(str(Azimuth(350)), '350°00\'00"')

    def test_minutes_and_seconds_are_zero_padded(self):
        self.assertEqual(str(Azimuth(10, 15)), '010°15\'00"')
        self.assertEqual(str(Azimuth(1, 2, 3)), '001°02\'03"')

    def test_repr(self):
        self.assertEqual(repr(Azimuth(0, 1, 1)), "Azimuth(seconds=61)")


class TestAzimuthPlusMinusAngle(unittest.TestCase):
    def test_add_angle(self):
        result = Azimuth(90, 30) + Angle(30, 45, 50)
        self.assertEqual(str(result), '121°15\'50"')

    def test_add_angle_with_wrapping(self):
        wrapped = Azimuth(degrees=300) + Angle(degrees=100)
        self.assertEqual(str(wrapped), '040°00\'00"')

    def test_subtract_angle_with_wrapping(self):
        wrapped_back = Azimuth(degrees=20) - Angle(degrees=45)
        self.assertEqual(str(wrapped_back), '335°00\'00"')

    def test_subtract_angle_without_wrapping(self):
        self.assertEqual(str(Azimuth(100) - Angle(30)), '070°00\'00"')

    def test_add_negative_angle(self):
        self.assertEqual(Azimuth(10) + Angle(-20), Azimuth(350))

    def test_adding_exactly_to_full_circle_gives_zero(self):
        self.assertEqual(Azimuth(300) + Angle(60), Azimuth(0))

    def test_adding_more_than_full_circle(self):
        self.assertEqual(Azimuth(10) + Angle(730), Azimuth(20))

    def test_result_is_azimuth(self):
        self.assertIsInstance(Azimuth(10) + Angle(5), Azimuth)
        self.assertIsInstance(Azimuth(10) - Angle(5), Azimuth)

    def test_operands_are_not_modified(self):
        azimuth, angle = Azimuth(300), Angle(100)
        _ = azimuth + angle
        _ = azimuth - angle
        self.assertEqual(azimuth, Azimuth(300))
        self.assertEqual(angle, Angle(100))

    def test_unsupported_operands_raise_type_error(self):
        with self.assertRaises(TypeError):
            Azimuth(10) + Azimuth(20)
        with self.assertRaises(TypeError):
            Azimuth(10) + 5
        with self.assertRaises(TypeError):
            Azimuth(10) - 5
        with self.assertRaises(TypeError):
            Angle(10) + Azimuth(20)


class TestAzimuthDifference(unittest.TestCase):
    def setUp(self):
        self.az1 = Azimuth(350)
        self.az2 = Azimuth(10, 15)

    def test_shortest_rotation_clockwise_across_north(self):
        self.assertEqual(str(self.az2 - self.az1), '20°15\'00"')

    def test_shortest_rotation_counterclockwise_across_north(self):
        self.assertEqual(str(self.az1 - self.az2), '-20°15\'00"')

    def test_result_is_angle(self):
        self.assertIsInstance(self.az2 - self.az1, Angle)

    def test_difference_without_crossing_north(self):
        self.assertEqual(Azimuth(90) - Azimuth(40), Angle(50))
        self.assertEqual(Azimuth(40) - Azimuth(90), Angle(-50))

    def test_equal_azimuths_give_zero(self):
        self.assertEqual(Azimuth(123, 45, 6) - Azimuth(123, 45, 6), Angle())

    def test_exactly_opposite_directions_give_plus_180(self):
        # Zakres to (-180°, 180°], więc 180° jest dodatnie w obie strony.
        self.assertEqual(Azimuth(180) - Azimuth(0), Angle(180))
        self.assertEqual(Azimuth(0) - Azimuth(180), Angle(180))
        self.assertEqual(Azimuth(270) - Azimuth(90), Angle(180))

    def test_just_below_and_above_180(self):
        self.assertEqual(Azimuth(179, 59, 59) - Azimuth(0), Angle(179, 59, 59))
        # 180°00'01" to to samo co -179°59'59" (Angle(-180, 0, 1)).
        self.assertEqual(Azimuth(180, 0, 1) - Azimuth(0), Angle(-180, 0, 1))
        self.assertEqual(str(Azimuth(180, 0, 1) - Azimuth(0)), '-179°59\'59"')
        self.assertEqual(Azimuth(181) - Azimuth(0), Angle(-179))

    def test_one_second_across_north(self):
        self.assertEqual(Azimuth(0) - Azimuth(359, 59, 59), Angle(seconds=1))
        self.assertEqual(Azimuth(359, 59, 59) - Azimuth(0), Angle(seconds=-1))

    def test_range_and_consistency_on_grid(self):
        values = [Azimuth(seconds=s) for s in range(0, 360 * 3600, 37 * 3600 + 1234)]
        lower, upper = Angle(-180), Angle(180)
        for a in values:
            for b in values:
                with self.subTest(a=str(a), b=str(b)):
                    diff = a - b
                    self.assertTrue(lower < diff <= upper)
                    # Obrót o `diff` od `b` prowadzi do `a`.
                    self.assertEqual(b + diff, a)


class TestAzimuthComparison(unittest.TestCase):
    def test_ordering_is_plain_numeric(self):
        self.assertTrue(Azimuth(10, 15) < Azimuth(350))
        self.assertTrue(Azimuth(350) > Azimuth(10, 15))
        self.assertTrue(Azimuth(10) <= Azimuth(10))
        self.assertTrue(Azimuth(10) >= Azimuth(10))
        self.assertFalse(Azimuth(350) < Azimuth(10, 15))

    def test_equality(self):
        self.assertEqual(Azimuth(90), Azimuth(minutes=5400))
        self.assertEqual(Azimuth(0), Azimuth(360))
        self.assertNotEqual(Azimuth(90), Azimuth(91))

    def test_equal_azimuths_have_equal_hashes(self):
        self.assertEqual(hash(Azimuth(0)), hash(Azimuth(360)))
        self.assertEqual(len({Azimuth(0), Azimuth(360), Azimuth(10)}), 2)

    def test_comparison_with_angle(self):
        self.assertFalse(Azimuth(10) == Angle(10))
        with self.assertRaises(TypeError):
            Azimuth(10) < Angle(20)


if __name__ == "__main__":
    unittest.main()
