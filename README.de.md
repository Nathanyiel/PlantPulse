# 🌱 Plant Moisture Monitor

**Nie wieder vergessen, die Pflanzen zu gießen.** Ein Raspberry Pi, sechs Widerstände und eine LED zeigen dir, wann die Erde trocken ist.

[![Lizenz: MIT](https://img.shields.io/badge/license-MIT-2f7f5f.svg)](LICENSE)
![Python 3](https://img.shields.io/badge/python-3-1d6ba3.svg)
![Raspberry Pi](https://img.shields.io/badge/läuft%20auf-Raspberry%20Pi-b05e14.svg)

**[Zur interaktiven Anleitung](https://nathanyiel.github.io/Raspberry-Pi_Moisture_Sensor/)** (Simulation, Verdrahtung, Code erklärt) · [English version](README.md)

![Schaltplan: GPIO 4 versorgt eine Widerstandskette, der Messknoten geht an GPIO 17 und die Bodensonden, GPIO 27 steuert die LED](assets/circuit.svg)

Das Projekt ist in unserem Programmierkurs während Berufsschule und Ausbildung entstanden. Es ist absichtlich klein, damit du jeden Teil verstehst und darauf aufbauen kannst.

## So funktioniert es

Feuchte Erde leitet Strom, trockene kaum. Der Pi macht daraus mit einem Spannungsteiler und einem digitalen Eingang ein Ja oder Nein. Ein zusätzlicher Chip ist nicht nötig.

1. **Impuls.** GPIO 4 geht für 10 ms auf HIGH und versorgt den Spannungsteiler. Die restliche Zeit fließt kein Strom durch die Sonden, das bremst die Korrosion.
2. **Messen.** GPIO 17 liest den Knoten zwischen Widerständen und Erde. Feuchte Erde zieht ihn auf LOW, trockene Erde lässt ihn auf HIGH.
3. **Reagieren.** Trocken: Die LED leuchtet und die Konsole meldet `Trocken`. Feucht: Die LED bleibt aus und die Konsole meldet `Feucht`. Dann wartet der Pi zwei Sekunden und beginnt von vorn.

## Das brauchst du

| Anzahl | Teil | Hinweis |
| --- | --- | --- |
| 1 | Raspberry Pi | Jedes Modell mit 40-Pin-Leiste. Der Schaltplan wurde für einen Pi 2 B gezeichnet. |
| 3 | 330-Ω-Widerstand | Oberer Teil des Spannungsteilers |
| 2 | 10-kΩ-Widerstand | Oberer Teil des Spannungsteilers |
| 1 | 330-Ω-Widerstand | Vorwiderstand der LED |
| 1 | LED | |
| 2 | Metallsonden | Zum Beispiel zwei Nägel oder Schrauben, oder zwei Kabel mit abisolierten Enden |
| | Jumper-Kabel | Optional ein Steckbrett |

## Verdrahtung

| Pin | GPIO (BCM) | Aufgabe | Verbunden mit |
| --- | --- | --- | --- |
| 7 | GPIO 4 | Versorgungsimpuls | Reihenschaltung aus 3 × 330 Ω und 2 × 10 kΩ, endet am Messknoten |
| 11 | GPIO 17 | Liest den Knoten | Messknoten, direkt |
| 13 | GPIO 27 | LED | 330 Ω, dann das lange Bein der LED. Das kurze Bein geht an GND. |
| 6, 9, … | GND | Rückleiter | Zweite Bodensonde und kurzes Bein der LED |

Der **Messknoten** ist der Punkt, an dem Widerstandskette, GPIO 17 und die erste Bodensonde zusammenkommen.

Die Widerstandskette ergibt etwa 21 kΩ und bildet die obere Hälfte eines Spannungsteilers. Die Erde ist die untere Hälfte. Zusammen mit dem internen Pull-down des Pi (etwa 50 kΩ) kippt GPIO 17 von LOW auf HIGH, wenn die Erde bei etwa 36 kΩ liegt. Das ist ein Schätzwert, weil der Schaltpunkt eines echten Eingangs etwas schwankt.

Der ursprüngliche Schaltplan liegt weiterhin im Repository: [Feuchtigkeitssensor_Schaltplan.drawio.png](Feuchtigkeitssensor_Schaltplan.drawio.png).

## Starten

Mach das auf dem Raspberry Pi. Unter Windows oder macOS kannst du das Skript bearbeiten, aber die GPIO-Bibliothek läuft nur auf einem Pi. Die [interaktive Anleitung](https://nathanyiel.github.io/Raspberry-Pi_Moisture_Sensor/) zeigt dir die Logik überall.

```bash
# 1. GPIO-Bibliothek (Raspberry Pi OS bringt sie meist schon mit)
sudo apt update
sudo apt install python3-rpi.gpio

# 2. Code holen
git clone https://github.com/Nathanyiel/Raspberry-Pi_Moisture_Sensor.git
cd Raspberry-Pi_Moisture_Sensor

# 3. Sensor starten, mit Strg+C beenden
python3 feuchtigkeits_sensor.py
```

Auf einem **Raspberry Pi 5** installierst du `python3-rpi-lgpio` statt `python3-rpi.gpio`. Es ist ein direkter Ersatz, das Skript bleibt gleich.

Beispielausgabe:

```
Feucht (GPIO_IN LOW)
Feucht (GPIO_IN LOW)
Trocken (GPIO_IN HIGH)
```

## Der Code in Kürze

Das Skript heißt [`feuchtigkeits_sensor.py`](feuchtigkeits_sensor.py) und hat rund 30 Zeilen.

- `GPIO_OUT = 4`, `GPIO_IN = 17`, `GPIO_LED = 27` nutzen die BCM-Nummerierung, es sind also GPIO-Nummern und keine physischen Pin-Nummern.
- `measure_once()` schaltet den Spannungsteiler ein, wartet 10 ms, liest GPIO 17, schaltet den Spannungsteiler aus und gibt `0` (feucht) oder `1` (trocken) zurück.
- Die Hauptschleife ruft `measure_once()` auf, setzt die LED, gibt eine Zeile aus und wartet zwei Sekunden. Das Intervall änderst du im letzten `time.sleep(2.0)`.
- `GPIO.cleanup()` läuft bei Strg+C und setzt die Pins zurück.

## Fehlersuche

| Problem | Das prüfen |
| --- | --- |
| `RuntimeError` zum Raspberry Pi oder fehlendes Modul `RPi` | Das Skript läuft nur auf einem Raspberry Pi mit installierter GPIO-Bibliothek. |
| Meldet immer `Trocken` | Beide Sonden in der Erde? GND verbunden? Sonden nicht zu weit auseinander? |
| Meldet immer `Feucht` | Berühren sich die Sonden? Ist die Widerstandskette mit GPIO 4 verbunden? |
| LED leuchtet nie | Richtung der LED (langes Bein zu GPIO 27) und der 330-Ω-Widerstand im LED-Zweig. |

## Bau es weiter aus

- Speichere die Messwerte mit Zeitstempel in einer CSV-Datei und zeichne, wie schnell deine Pflanze austrocknet.
- Schick eine Push-Nachricht oder E-Mail, wenn die Erde mehrere Messungen hintereinander trocken war.
- Ergänze einen Analog-Digital-Wandler wie den MCP3008, um einen Prozentwert statt feucht oder trocken zu bekommen.
- Steuer eine kleine Pumpe über ein Relais oder einen Transistor, um automatisch zu gießen.
- Lass das Skript als systemd-Dienst laufen, damit es beim Start mitläuft.
- Bau den Spannungsteiler auf weiteren GPIO-Pins nach, um mehrere Pflanzen zu überwachen.

## Credits

Gebaut von [Jan (lebor32)](https://github.com/lebor32) und [Nate (Nathanyiel)](https://github.com/Nathanyiel). Veröffentlicht unter der [MIT-Lizenz](LICENSE).
