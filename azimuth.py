"""Klasa Azimuth - kierunek na kompasie (azymut w zakresie [0°, 360°))."""

from angle import Angle

FULL_CIRCLE = 360 * 3600  # pełny obrót w sekundach kątowych
HALF_CIRCLE = FULL_CIRCLE // 2

COMPASS_POINTS = ("N", "NE", "E", "SE", "S", "SW", "W", "NW")
COMPASS_SECTOR = FULL_CIRCLE // len(COMPASS_POINTS)  # 45° w sekundach


class Azimuth:
    """Azymut przechowywany jako liczba sekund kątowych z przedziału [0, 360°).

    Wartości spoza zakresu są "zawijane" (np. 370° -> 10°, -10° -> 350°).
    """

    def __init__(self, degrees=0, minutes=0, seconds=0):
        """Tworzy azymut.

        degrees (int): stopnie
        minutes (int): minuty kątowe
        seconds (int): sekundy kątowe
        """
        # Operator % daje wynik z zakresu [0, FULL_CIRCLE) także dla liczb
        # ujemnych, więc zawijanie wartości dzieje się samo.
        self._seconds = Angle(degrees, minutes, seconds).to_seconds() % FULL_CIRCLE

    def to_seconds(self):
        """Zwraca azymut jako całkowitą liczbę sekund kątowych."""
        return self._seconds

    def to_compass(self):
        """Zwraca najbliższy z ośmiu kierunków róży wiatrów (N, NE, E, ...).

        Każdy kierunek obejmuje sektor 45° wyśrodkowany na kierunku głównym,
        np. N to [337°30', 360°) oraz [0°, 22°30'). Granica sektora należy
        do kolejnego sektora (zgodnie z ruchem wskazówek zegara).
        """
        index = (self._seconds + COMPASS_SECTOR // 2) // COMPASS_SECTOR
        return COMPASS_POINTS[index % len(COMPASS_POINTS)]

    def __add__(self, other):
        """Azymut + kąt (Angle) = nowy azymut."""
        return Azimuth(seconds=self._seconds + other.to_seconds())

    def __sub__(self, other):
        """Azymut - kąt (Angle) = azymut; azymut - azymut = kąt (Angle).

        Różnica dwóch azymutów to najkrótszy obrót od `other` do `self`,
        czyli wartość z zakresu (-180°, 180°].
        """
        if isinstance(other, Azimuth):
            difference = (self._seconds - other.to_seconds()) % FULL_CIRCLE
            if difference > HALF_CIRCLE:
                difference = difference - FULL_CIRCLE
            return Angle(seconds=difference)
        return Azimuth(seconds=self._seconds - other.to_seconds())

    def __eq__(self, other):
        return self._seconds == other.to_seconds()

    def __lt__(self, other):
        return self._seconds < other.to_seconds()

    def __le__(self, other):
        return self._seconds <= other.to_seconds()

    def __gt__(self, other):
        return self._seconds > other.to_seconds()

    def __ge__(self, other):
        return self._seconds >= other.to_seconds()

    def __str__(self):
        degrees = self._seconds // 3600
        minutes = (self._seconds % 3600) // 60
        seconds = self._seconds % 60
        return f"{degrees:03d}°{minutes:02d}'{seconds:02d}\""
