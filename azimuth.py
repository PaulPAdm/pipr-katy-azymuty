"""Klasa Azimuth - kierunek na kompasie (azymut w zakresie [0°, 360°))."""

from functools import total_ordering

from angle import Angle

FULL_CIRCLE = 360 * 3600  # pełny obrót w sekundach kątowych
HALF_CIRCLE = FULL_CIRCLE // 2

COMPASS_POINTS = ("N", "NE", "E", "SE", "S", "SW", "W", "NW")
COMPASS_SECTOR = FULL_CIRCLE // len(COMPASS_POINTS)  # 45° w sekundach


@total_ordering
class Azimuth:
    """Azymut przechowywany jako liczba sekund kątowych z przedziału [0, 360°).

    Wartości spoza zakresu są "zawijane" (np. 370° -> 10°, -10° -> 350°).
    """

    def __init__(self, degrees=0, minutes=0, seconds=0):
        # Angle sprawdza typy argumentów i normalizuje minuty oraz sekundy.
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
        if not isinstance(other, Angle):
            return NotImplemented
        return Azimuth(seconds=self._seconds + other.to_seconds())

    def __sub__(self, other):
        if isinstance(other, Angle):
            return Azimuth(seconds=self._seconds - other.to_seconds())
        if isinstance(other, Azimuth):
            # Najkrótszy obrót od `other` do `self`, wynik z zakresu (-180°, 180°].
            difference = (self._seconds - other._seconds) % FULL_CIRCLE
            if difference > HALF_CIRCLE:
                difference -= FULL_CIRCLE
            return Angle.from_seconds(difference)
        return NotImplemented

    def __eq__(self, other):
        if not isinstance(other, Azimuth):
            return NotImplemented
        return self._seconds == other._seconds

    def __lt__(self, other):
        if not isinstance(other, Azimuth):
            return NotImplemented
        return self._seconds < other._seconds

    def __hash__(self):
        return hash(self._seconds)

    def __str__(self):
        degrees, rest = divmod(self._seconds, 3600)
        minutes, seconds = divmod(rest, 60)
        return f"{degrees:03d}°{minutes:02d}'{seconds:02d}\""

    def __repr__(self):
        return f"Azimuth(seconds={self._seconds})"
