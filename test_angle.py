import unittest

from angle import Angle


class TestAngleCreation(unittest.TestCase):
    def test_default_is_zero(self):
        self.assertEqual(Angle().to_seconds(), 0)
        self.assertEqual(str(Angle()), '0°00\'00"')

    def test_positional_arguments(self):
        self.assertEqual(Angle(30, 45, 50).to_seconds(), 110750)

    def test_keyword_arguments(self):
        self.assertEqual(Angle(minutes=90), Angle(1, 30))
        self.assertEqual(Angle(seconds=45), Angle(0, 0, 45))
        self.assertEqual(Angle(degrees=2, seconds=5), Angle(2, 0, 5))

    def test_minutes_overflow_is_normalized(self):
        self.assertEqual(str(Angle(minutes=90)), '1°30\'00"')
        self.assertEqual(str(Angle(0, 61)), '1°01\'00"')

    def test_seconds_overflow_is_normalized(self):
        self.assertEqual(str(Angle(seconds=3661)), '1°01\'01"')
        self.assertEqual(str(Angle(10, 59, 60)), '11°00\'00"')

    def test_negative_minutes_and_seconds(self):
        self.assertEqual(str(Angle(minutes=-150, seconds=30)), '-2°29\'30"')
        self.assertEqual(str(Angle(1, -30)), '0°30\'00"')
        self.assertEqual(str(Angle(10, 0, -1)), '9°59\'59"')

    def test_negative_angle_smaller_than_one_degree(self):
        self.assertEqual(Angle(-1, 30).to_seconds(), -1800)
        self.assertEqual(str(Angle(-1, 30)), '-0°30\'00"')
        self.assertEqual(str(Angle(seconds=-5)), '-0°00\'05"')

    def test_non_integer_raises_type_error(self):
        with self.assertRaises(TypeError):
            Angle(1.5)
        with self.assertRaises(TypeError):
            Angle(minutes="10")
        with self.assertRaises(TypeError):
            Angle(seconds=None)


class TestAngleSeconds(unittest.TestCase):
    def test_to_seconds(self):
        self.assertEqual(Angle(30, 45, 50).to_seconds(), 110750)
        self.assertEqual(Angle(1).to_seconds(), 3600)
        self.assertEqual(Angle(0, 1).to_seconds(), 60)
        self.assertEqual(Angle(-2, 0, 0).to_seconds(), -7200)

    def test_from_seconds(self):
        angle = Angle.from_seconds(5400)
        self.assertEqual(str(angle), '1°30\'00"')
        self.assertEqual(angle, Angle(minutes=90))

    def test_from_negative_seconds(self):
        self.assertEqual(str(Angle.from_seconds(-8970)), '-2°29\'30"')

    def test_round_trip(self):
        for total in (-1296000, -3601, -1, 0, 1, 59, 60, 3599, 3600, 110750, 1296000):
            with self.subTest(total=total):
                self.assertEqual(Angle.from_seconds(total).to_seconds(), total)


class TestAngleFormatting(unittest.TestCase):
    def test_example_from_task(self):
        self.assertEqual(str(Angle(46, 6, 15)), '46°06\'15"')

    def test_minutes_and_seconds_are_zero_padded(self):
        self.assertEqual(str(Angle(5, 3, 7)), '5°03\'07"')

    def test_degrees_are_not_padded(self):
        self.assertEqual(str(Angle(1)), '1°00\'00"')
        self.assertEqual(str(Angle(123)), '123°00\'00"')

    def test_degrees_above_360_are_kept(self):
        self.assertEqual(str(Angle(400)), '400°00\'00"')

    def test_repr(self):
        self.assertEqual(repr(Angle(1, 0, 1)), "Angle(seconds=3601)")


class TestAngleArithmetic(unittest.TestCase):
    def setUp(self):
        self.angle1 = Angle(30, 45, 50)
        self.angle2 = Angle(15, 20, 25)

    def test_addition(self):
        self.assertEqual(str(self.angle1 + self.angle2), '46°06\'15"')

    def test_subtraction(self):
        self.assertEqual(str(self.angle1 - self.angle2), '15°25\'25"')

    def test_subtraction_giving_negative_result(self):
        self.assertEqual(str(self.angle2 - self.angle1), '-15°25\'25"')

    def test_subtraction_of_equal_angles_gives_zero(self):
        self.assertEqual(self.angle1 - self.angle1, Angle())

    def test_addition_with_negative_angle(self):
        self.assertEqual(Angle(10) + Angle(-25), Angle(-15))

    def test_result_is_angle(self):
        self.assertIsInstance(self.angle1 + self.angle2, Angle)
        self.assertIsInstance(self.angle1 - self.angle2, Angle)

    def test_operands_are_not_modified(self):
        _ = self.angle1 + self.angle2
        _ = self.angle1 - self.angle2
        self.assertEqual(self.angle1.to_seconds(), 110750)
        self.assertEqual(str(self.angle2), '15°20\'25"')

    def test_adding_non_angle_raises_type_error(self):
        with self.assertRaises(TypeError):
            Angle(1) + 5
        with self.assertRaises(TypeError):
            Angle(1) - "5"


class TestAngleComparison(unittest.TestCase):
    def test_equality_of_different_representations(self):
        self.assertEqual(Angle(1, 30), Angle(minutes=90))
        self.assertEqual(Angle(0, 0, 3600), Angle(1))

    def test_inequality(self):
        self.assertNotEqual(Angle(1), Angle(2))

    def test_ordering(self):
        small, big = Angle(15, 20, 25), Angle(30, 45, 50)
        self.assertTrue(small < big)
        self.assertTrue(small <= big)
        self.assertTrue(big > small)
        self.assertTrue(big >= small)
        self.assertFalse(big < small)
        self.assertTrue(Angle(1) <= Angle(0, 60))
        self.assertTrue(Angle(1) >= Angle(0, 60))

    def test_negative_angles_ordering(self):
        self.assertTrue(Angle(-2) < Angle(-1))
        self.assertTrue(Angle(-1) < Angle(0, 0, 1))

    def test_equal_angles_have_equal_hashes(self):
        self.assertEqual(hash(Angle(1, 30)), hash(Angle(minutes=90)))
        self.assertEqual(len({Angle(1, 30), Angle(minutes=90), Angle(2)}), 2)

    def test_comparison_with_other_types(self):
        self.assertFalse(Angle(1) == 3600)
        self.assertTrue(Angle(1) != 3600)
        with self.assertRaises(TypeError):
            Angle(1) < 5


if __name__ == "__main__":
    unittest.main()
