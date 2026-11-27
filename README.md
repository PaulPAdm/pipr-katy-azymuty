# Kąty i kierunki na kompasie

Zadanie z PIPR (Podstawy informatyki i programowania, Politechnika Warszawska, WEiTI):
klasy `Angle` (kąt w stopniach, minutach i sekundach kątowych) oraz `Azimuth`
(kierunek na kompasie, azymut z zakresu `[0°, 360°)`).

Rozwiązanie używa wyłącznie biblioteki standardowej Pythona (bez modułu `math`).

## Pliki

| Plik | Zawartość |
| --- | --- |
| `angle.py` | klasa `Angle` |
| `azimuth.py` | klasa `Azimuth` (razem z `to_compass()`) |
| `test_angle.py` | testy jednostkowe `Angle` |
| `test_azimuth.py` | testy jednostkowe `Azimuth` |

## Uruchamianie testów

```bash
python -m unittest -v
```

## Przykład

```python
from angle import Angle
from azimuth import Azimuth

print(Angle(30, 45, 50) + Angle(15, 20, 25))   # 46°06'15"
print(Angle(minutes=-150, seconds=30))         # -2°29'30"

print(Azimuth(10, 15) - Azimuth(350))          # 20°15'00"  (najkrótszy obrót)
print(Azimuth(300) + Angle(100))               # 040°00'00"
print(Azimuth(130).to_compass())               # SE
```

## Decyzje projektowe

* Kąt jest przechowywany jako całkowita liczba sekund kątowych, więc normalizacja
  minut i sekund oraz obsługa wartości ujemnych wynikają wprost z arytmetyki na liczbach całkowitych.
* `Azimuth` nie dziedziczy po `Angle`, dzięki czemu operator `-` jednoznacznie rozróżnia
  `Azimuth - Angle` (daje `Azimuth`) i `Azimuth - Azimuth` (daje `Angle`).
* Różnica azymutów należy do przedziału `(-180°, 180°]`; dokładnie 180° jest zawsze dodatnie.
* `to_compass()`: granica sektora (np. 22°30') należy do następnego sektora zgodnie z ruchem wskazówek zegara.
