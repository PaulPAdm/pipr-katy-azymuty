"""Klasa Angle - kąt w stopniach, minutach i sekundach kątowych."""

SECONDS_IN_MINUTE = 60
SECONDS_IN_DEGREE = 3600


class Angle:
    """Kąt (również ujemny) przechowywany jako liczba sekund kątowych.

    Minuty i sekundy spoza zakresu 0-59 oraz wartości ujemne są
    normalizowane automatycznie (1° = 60', 1' = 60").
    """

    def __init__(self, degrees=0, minutes=0, seconds=0):
        """Tworzy kąt.

        degrees (int): stopnie
        minutes (int): minuty kątowe
        seconds (int): sekundy kątowe
        """
        self._seconds = (
            degrees * SECONDS_IN_DEGREE + minutes * SECONDS_IN_MINUTE + seconds
        )

    def from_seconds(total_seconds):
        """Tworzy kąt z całkowitej liczby sekund kątowych.

        Nie ma parametru self, więc wołamy ją przez klasę:
        Angle.from_seconds(5400).
        """
        return Angle(seconds=total_seconds)

    def to_seconds(self):
        """Zwraca kąt jako całkowitą liczbę sekund kątowych."""
        return self._seconds

    def __add__(self, other):
        return Angle(seconds=self._seconds + other.to_seconds())

    def __sub__(self, other):
        return Angle(seconds=self._seconds - other.to_seconds())

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
        sign = "-" if self._seconds < 0 else ""
        total = abs(self._seconds)
        degrees = total // SECONDS_IN_DEGREE
        minutes = (total % SECONDS_IN_DEGREE) // SECONDS_IN_MINUTE
        seconds = total % SECONDS_IN_MINUTE
        return f"{sign}{degrees}°{minutes:02d}'{seconds:02d}\""
