from angle import Angle
from azimuth import Azimuth


def test_str_format():
    assert str(Azimuth()) == '000°00\'00"'
    assert str(Azimuth(40)) == '040°00\'00"'
    assert str(Azimuth(10, 15)) == '010°15\'00"'


def test_constructor_wraps_values():
    assert Azimuth(360) == Azimuth(0)
    assert str(Azimuth(370)) == '010°00\'00"'
    assert str(Azimuth(-10)) == '350°00\'00"'


def test_add_angle():
    assert str(Azimuth(90, 30) + Angle(30, 45, 50)) == '121°15\'50"'


def test_add_angle_with_wrapping():
    assert str(Azimuth(degrees=300) + Angle(degrees=100)) == '040°00\'00"'


def test_subtract_angle_with_wrapping():
    assert str(Azimuth(degrees=20) - Angle(degrees=45)) == '335°00\'00"'


def test_difference_across_north():
    az1 = Azimuth(350)
    az2 = Azimuth(10, 15)
    # wynik jest kątem (Angle), więc stopnie bez zer wiodących
    assert str(az2 - az1) == '20°15\'00"'
    assert str(az1 - az2) == '-20°15\'00"'


def test_difference_at_180_degrees():
    # zakres to (-180°, 180°], więc dokładnie 180° jest dodatnie w obie strony
    assert Azimuth(180) - Azimuth(0) == Angle(180)
    assert Azimuth(0) - Azimuth(180) == Angle(180)
    assert Azimuth(181) - Azimuth(0) == Angle(-179)


def test_comparison():
    assert Azimuth(10, 15) < Azimuth(350)
    assert Azimuth(350) > Azimuth(10, 15)
    assert Azimuth(90) == Azimuth(minutes=5400)


def test_to_compass():
    assert Azimuth(0).to_compass() == "N"
    assert Azimuth(130).to_compass() == "SE"
    assert Azimuth(270).to_compass() == "W"
    assert Azimuth(350).to_compass() == "N"


def test_to_compass_sector_boundary():
    assert Azimuth(22, 29, 59).to_compass() == "N"
    assert Azimuth(22, 30).to_compass() == "NE"
