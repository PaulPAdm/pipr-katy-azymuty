from angle import Angle


# --- tworzenie ---

def test_default_is_zero():
    assert Angle().to_seconds() == 0
    assert str(Angle()) == '0°00\'00"'


def test_positional_arguments():
    assert Angle(30, 45, 50).to_seconds() == 110750


def test_keyword_arguments():
    assert Angle(minutes=90) == Angle(1, 30)
    assert Angle(seconds=45) == Angle(0, 0, 45)
    assert Angle(degrees=2, seconds=5) == Angle(2, 0, 5)


def test_minutes_overflow_is_normalized():
    assert str(Angle(minutes=90)) == '1°30\'00"'
    assert str(Angle(0, 61)) == '1°01\'00"'


def test_seconds_overflow_is_normalized():
    assert str(Angle(seconds=3661)) == '1°01\'01"'
    assert str(Angle(10, 59, 60)) == '11°00\'00"'


def test_negative_minutes_and_seconds():
    assert str(Angle(minutes=-150, seconds=30)) == '-2°29\'30"'
    assert str(Angle(1, -30)) == '0°30\'00"'
    assert str(Angle(10, 0, -1)) == '9°59\'59"'


def test_negative_angle_smaller_than_one_degree():
    assert Angle(-1, 30).to_seconds() == -1800
    assert str(Angle(-1, 30)) == '-0°30\'00"'
    assert str(Angle(seconds=-5)) == '-0°00\'05"'


# --- sekundy ---

def test_to_seconds():
    assert Angle(30, 45, 50).to_seconds() == 110750
    assert Angle(1).to_seconds() == 3600
    assert Angle(0, 1).to_seconds() == 60
    assert Angle(-2, 0, 0).to_seconds() == -7200


def test_from_seconds():
    angle = Angle.from_seconds(5400)
    assert str(angle) == '1°30\'00"'
    assert angle == Angle(minutes=90)


def test_from_negative_seconds():
    assert str(Angle.from_seconds(-8970)) == '-2°29\'30"'


def test_seconds_round_trip():
    for total in (-1296000, -3601, -1, 0, 1, 59, 60, 3599, 3600, 110750, 1296000):
        assert Angle.from_seconds(total).to_seconds() == total, total


# --- formatowanie ---

def test_str_example_from_task():
    assert str(Angle(46, 6, 15)) == '46°06\'15"'


def test_str_minutes_and_seconds_are_zero_padded():
    assert str(Angle(5, 3, 7)) == '5°03\'07"'


def test_str_degrees_are_not_padded():
    assert str(Angle(1)) == '1°00\'00"'
    assert str(Angle(123)) == '123°00\'00"'


def test_str_degrees_above_360_are_kept():
    assert str(Angle(400)) == '400°00\'00"'


# --- arytmetyka ---

def test_addition():
    angle1 = Angle(30, 45, 50)
    angle2 = Angle(15, 20, 25)
    assert str(angle1 + angle2) == '46°06\'15"'


def test_subtraction():
    angle1 = Angle(30, 45, 50)
    angle2 = Angle(15, 20, 25)
    assert str(angle1 - angle2) == '15°25\'25"'


def test_subtraction_giving_negative_result():
    angle1 = Angle(30, 45, 50)
    angle2 = Angle(15, 20, 25)
    assert str(angle2 - angle1) == '-15°25\'25"'


def test_subtraction_of_equal_angles_gives_zero():
    angle = Angle(30, 45, 50)
    assert angle - angle == Angle()


def test_addition_with_negative_angle():
    assert Angle(10) + Angle(-25) == Angle(-15)


def test_operands_are_not_modified():
    angle1 = Angle(30, 45, 50)
    angle2 = Angle(15, 20, 25)
    angle1 + angle2
    angle1 - angle2
    assert angle1.to_seconds() == 110750
    assert str(angle2) == '15°20\'25"'


# --- porównywanie ---

def test_equality_of_different_representations():
    assert Angle(1, 30) == Angle(minutes=90)
    assert Angle(0, 0, 3600) == Angle(1)


def test_inequality():
    assert Angle(1) != Angle(2)
    assert not (Angle(1) != Angle(0, 60))


def test_ordering():
    small = Angle(15, 20, 25)
    big = Angle(30, 45, 50)
    assert small < big
    assert small <= big
    assert big > small
    assert big >= small
    assert not (big < small)
    assert Angle(1) <= Angle(0, 60)
    assert Angle(1) >= Angle(0, 60)


def test_ordering_of_negative_angles():
    assert Angle(-2) < Angle(-1)
    assert Angle(-1) < Angle(0, 0, 1)
