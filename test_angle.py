from angle import Angle


def test_default_is_zero():
    assert Angle().to_seconds() == 0
    assert str(Angle()) == '0°00\'00"'


def test_positional_and_keyword_arguments():
    assert Angle(minutes=90) == Angle(1, 30)
    assert Angle(degrees=2, seconds=5) == Angle(2, 0, 5)


def test_minutes_and_seconds_are_normalized():
    assert str(Angle(minutes=90)) == '1°30\'00"'
    assert str(Angle(seconds=3661)) == '1°01\'01"'


def test_negative_angle():
    assert str(Angle(minutes=-150, seconds=30)) == '-2°29\'30"'
    assert str(Angle(-1, 30)) == '-0°30\'00"'


def test_to_seconds_and_from_seconds():
    assert Angle(30, 45, 50).to_seconds() == 110750
    angle = Angle.from_seconds(5400)
    assert str(angle) == '1°30\'00"'
    assert angle == Angle(minutes=90)


def test_str_format():
    assert str(Angle(46, 6, 15)) == '46°06\'15"'
    assert str(Angle(5, 3, 7)) == '5°03\'07"'


def test_addition_and_subtraction():
    angle1 = Angle(30, 45, 50)
    angle2 = Angle(15, 20, 25)
    assert str(angle1 + angle2) == '46°06\'15"'
    assert str(angle1 - angle2) == '15°25\'25"'
    assert str(angle2 - angle1) == '-15°25\'25"'


def test_comparison():
    small = Angle(15, 20, 25)
    big = Angle(30, 45, 50)
    assert small < big
    assert big > small
    assert small <= small
    assert big >= big
    assert small != big
    assert Angle(1, 30) == Angle(minutes=90)
