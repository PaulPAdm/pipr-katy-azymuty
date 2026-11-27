from angle import Angle
from azimuth import Azimuth


# --- tworzenie ---

def test_default_is_north():
    assert str(Azimuth()) == '000°00\'00"'


def test_positional_and_keyword_arguments():
    assert Azimuth(10, 15) == Azimuth(degrees=10, minutes=15)
    assert Azimuth(minutes=30) == Azimuth(0, 30, 0)
    assert Azimuth(seconds=45) == Azimuth(0, 0, 45)


def test_minutes_and_seconds_overflow_is_normalized():
    assert str(Azimuth(10, 90)) == '011°30\'00"'
    assert str(Azimuth(10, 59, 60)) == '011°00\'00"'


def test_full_circle_wraps_to_zero():
    assert Azimuth(360) == Azimuth(0)
    assert Azimuth(720, 30) == Azimuth(0, 30)
    assert Azimuth(seconds=360 * 3600) == Azimuth()


def test_values_above_360_are_wrapped():
    assert str(Azimuth(370)) == '010°00\'00"'


def test_negative_values_are_wrapped():
    assert str(Azimuth(-10)) == '350°00\'00"'
    assert str(Azimuth(minutes=-1)) == '359°59\'00"'
    assert str(Azimuth(seconds=-1)) == '359°59\'59"'


def test_to_seconds():
    assert Azimuth(90).to_seconds() == 324000
    assert Azimuth(359, 59, 59).to_seconds() == 360 * 3600 - 1


# --- formatowanie ---

def test_str_three_digit_degrees():
    assert str(Azimuth(40)) == '040°00\'00"'
    assert str(Azimuth(5)) == '005°00\'00"'
    assert str(Azimuth(350)) == '350°00\'00"'


def test_str_minutes_and_seconds_are_zero_padded():
    assert str(Azimuth(10, 15)) == '010°15\'00"'
    assert str(Azimuth(1, 2, 3)) == '001°02\'03"'


# --- azymut +/- kąt ---

def test_add_angle():
    result = Azimuth(90, 30) + Angle(30, 45, 50)
    assert str(result) == '121°15\'50"'


def test_add_angle_with_wrapping():
    wrapped = Azimuth(degrees=300) + Angle(degrees=100)
    assert str(wrapped) == '040°00\'00"'


def test_subtract_angle_with_wrapping():
    wrapped_back = Azimuth(degrees=20) - Angle(degrees=45)
    assert str(wrapped_back) == '335°00\'00"'


def test_subtract_angle_without_wrapping():
    assert str(Azimuth(100) - Angle(30)) == '070°00\'00"'


def test_add_negative_angle():
    assert Azimuth(10) + Angle(-20) == Azimuth(350)


def test_adding_exactly_to_full_circle_gives_zero():
    assert Azimuth(300) + Angle(60) == Azimuth(0)


def test_adding_more_than_full_circle():
    assert Azimuth(10) + Angle(730) == Azimuth(20)


def test_operands_are_not_modified():
    azimuth = Azimuth(300)
    angle = Angle(100)
    azimuth + angle
    azimuth - angle
    assert azimuth == Azimuth(300)
    assert angle == Angle(100)


# --- azymut - azymut (najkrótszy obrót) ---

def test_shortest_rotation_clockwise_across_north():
    az1 = Azimuth(350)
    az2 = Azimuth(10, 15)
    # wynik jest kątem (Angle), więc stopnie bez zer wiodących
    assert str(az2 - az1) == '20°15\'00"'


def test_shortest_rotation_counterclockwise_across_north():
    az1 = Azimuth(350)
    az2 = Azimuth(10, 15)
    assert str(az1 - az2) == '-20°15\'00"'


def test_difference_without_crossing_north():
    assert Azimuth(90) - Azimuth(40) == Angle(50)
    assert Azimuth(40) - Azimuth(90) == Angle(-50)


def test_equal_azimuths_give_zero():
    assert Azimuth(123, 45, 6) - Azimuth(123, 45, 6) == Angle()


def test_exactly_opposite_directions_give_plus_180():
    # Zakres to (-180°, 180°], więc 180° jest dodatnie w obie strony.
    assert Azimuth(180) - Azimuth(0) == Angle(180)
    assert Azimuth(0) - Azimuth(180) == Angle(180)
    assert Azimuth(270) - Azimuth(90) == Angle(180)


def test_just_below_and_above_180():
    assert Azimuth(179, 59, 59) - Azimuth(0) == Angle(179, 59, 59)
    # 180°00'01" to to samo co -179°59'59" (Angle(-180, 0, 1)).
    assert Azimuth(180, 0, 1) - Azimuth(0) == Angle(-180, 0, 1)
    assert str(Azimuth(180, 0, 1) - Azimuth(0)) == '-179°59\'59"'
    assert Azimuth(181) - Azimuth(0) == Angle(-179)


def test_one_second_across_north():
    assert Azimuth(0) - Azimuth(359, 59, 59) == Angle(seconds=1)
    assert Azimuth(359, 59, 59) - Azimuth(0) == Angle(seconds=-1)


def test_difference_range_and_consistency_on_grid():
    values = []
    for s in range(0, 360 * 3600, 37 * 3600 + 1234):
        values.append(Azimuth(seconds=s))
    lower = Angle(-180)
    upper = Angle(180)
    for a in values:
        for b in values:
            diff = a - b
            assert lower < diff <= upper, (str(a), str(b))
            # obrót o `diff` od `b` prowadzi do `a`
            assert b + diff == a, (str(a), str(b))


# --- porównywanie ---

def test_ordering_is_plain_numeric():
    assert Azimuth(10, 15) < Azimuth(350)
    assert Azimuth(350) > Azimuth(10, 15)
    assert Azimuth(10) <= Azimuth(10)
    assert Azimuth(10) >= Azimuth(10)
    assert not (Azimuth(350) < Azimuth(10, 15))


def test_equality():
    assert Azimuth(90) == Azimuth(minutes=5400)
    assert Azimuth(0) == Azimuth(360)
    assert Azimuth(90) != Azimuth(91)


# --- to_compass ---

def test_compass_main_directions():
    expected = {
        0: "N", 45: "NE", 90: "E", 135: "SE",
        180: "S", 225: "SW", 270: "W", 315: "NW",
    }
    for degrees in expected:
        assert Azimuth(degrees).to_compass() == expected[degrees], degrees


def test_compass_example_from_task():
    assert Azimuth(130).to_compass() == "SE"


def test_compass_north_on_both_sides_of_zero():
    assert Azimuth(350).to_compass() == "N"
    assert Azimuth(10).to_compass() == "N"
    assert Azimuth(359, 59, 59).to_compass() == "N"


def test_compass_sector_boundaries():
    # Granica sektora należy do następnego sektora (zgodnie z zegarem).
    cases = [
        (Azimuth(22, 29, 59), "N"), (Azimuth(22, 30), "NE"),
        (Azimuth(67, 29, 59), "NE"), (Azimuth(67, 30), "E"),
        (Azimuth(112, 29, 59), "E"), (Azimuth(112, 30), "SE"),
        (Azimuth(157, 29, 59), "SE"), (Azimuth(157, 30), "S"),
        (Azimuth(202, 29, 59), "S"), (Azimuth(202, 30), "SW"),
        (Azimuth(247, 29, 59), "SW"), (Azimuth(247, 30), "W"),
        (Azimuth(292, 29, 59), "W"), (Azimuth(292, 30), "NW"),
        (Azimuth(337, 29, 59), "NW"), (Azimuth(337, 30), "N"),
    ]
    for azimuth, name in cases:
        assert azimuth.to_compass() == name, str(azimuth)


def test_compass_after_wrapping():
    assert (Azimuth(300) + Angle(100)).to_compass() == "NE"
    assert (Azimuth(20) - Angle(45)).to_compass() == "NW"


def test_compass_returns_known_direction():
    allowed = ("N", "NE", "E", "SE", "S", "SW", "W", "NW")
    for seconds in range(0, 360 * 3600, 5003):
        assert Azimuth(seconds=seconds).to_compass() in allowed, seconds
