"""Klasa Angle - kąt w stopniach, minutach i sekundach kątowych."""

from functools import total_ordering

SECONDS_IN_MINUTE = 60
SECONDS_IN_DEGREE = 3600


@total_ordering
class Angle:
    """Kąt (również ujemny) przechowywany jako całkowita liczba sekund kątowych.

    Dzięki temu minuty i sekundy spoza zakresu 0-59 oraz wartości ujemne
    są normalizowane automatycznie (1° = 60', 1' = 60").
    """

    def __init__(self, degrees=0, minutes=0, seconds=0):
        for name, value in (("degrees", degrees), ("minutes", minutes), ("seconds", seconds)):
            if not isinstance(value, int) or isinstance(value, bool):
                raise TypeError(f"{name} musi być liczbą całkowitą, otrzymano: {value!r}")
        self._seconds = (
            degrees * SECONDS_IN_DEGREE + minutes * SECONDS_IN_MINUTE + seconds
        )

    @classmethod
    def from_seconds(cls, total_seconds):
        """Tworzy kąt z całkowitej liczby sekund kątowych."""
        return cls(seconds=total_seconds)

    def to_seconds(self):
        """Zwraca kąt jako całkowitą liczbę sekund kątowych."""
        return self._seconds

    def __add__(self, other):
        if not isinstance(other, Angle):
            return NotImplemented
        return Angle.from_seconds(self._seconds + other._seconds)

    def __sub__(self, other):
        if not isinstance(other, Angle):
            return NotImplemented
        return Angle.from_seconds(self._seconds - other._seconds)

    def __eq__(self, other):
        if not isinstance(other, Angle):
            return NotImplemented
        return self._seconds == other._seconds

    def __lt__(self, other):
        if not isinstance(other, Angle):
            return NotImplemented
        return self._seconds < other._seconds

    def __hash__(self):
        return hash(self._seconds)

    def __str__(self):
        sign = "-" if self._seconds < 0 else ""
        degrees, rest = divmod(abs(self._seconds), SECONDS_IN_DEGREE)
        minutes, seconds = divmod(rest, SECONDS_IN_MINUTE)
        return f"{sign}{degrees}°{minutes:02d}'{seconds:02d}\""

    def __repr__(self):
        return f"Angle(seconds={self._seconds})"
