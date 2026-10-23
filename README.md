# 🌱 Plant Moisture Monitor

**Never forget to water your plants again.** A Raspberry Pi, six resistors and one LED tell you when the soil is dry.

[![License: MIT](https://img.shields.io/badge/license-MIT-2f7f5f.svg)](LICENSE)
![Python 3](https://img.shields.io/badge/python-3-1d6ba3.svg)
![Raspberry Pi](https://img.shields.io/badge/runs%20on-Raspberry%20Pi-b05e14.svg)

**[Open the interactive guide](https://nathanyiel.github.io/Raspberry-Pi_Moisture_Sensor/)** (simulator, wiring, code walkthrough)

![Circuit diagram: GPIO 4 feeds a resistor chain, the measuring node goes to GPIO 17 and the soil probes, GPIO 27 drives the LED](assets/circuit.svg)

This project came out of the programming course during our vocational school and apprenticeship. It is small on purpose, so you can understand every part and build on it.

## How it works

Wet soil conducts electricity, dry soil hardly does. The Pi turns that into a yes or no with a voltage divider and one digital input. No extra chip is needed.

1. **Pulse.** GPIO 4 goes HIGH for 10 ms and powers the divider. The rest of the time no current flows through the probes, which slows corrosion.
2. **Read.** GPIO 17 reads the node between the resistors and the soil. Wet soil pulls it down to LOW. Dry soil lets it stay HIGH.
3. **React.** Dry: the LED lights up and the console prints `Dry`. Wet: the LED stays off and the console prints `Wet`. Then the Pi waits two seconds and starts again.

## What you need

| Qty | Part | Note |
| --- | --- | --- |
| 1 | Raspberry Pi | Any model with the 40-pin header. The schematic was drawn for a Pi 2 B. |
| 3 | 330 Ω resistor | Upper part of the voltage divider |
| 2 | 10 kΩ resistor | Upper part of the voltage divider |
| 1 | 330 Ω resistor | In series with the LED |
| 1 | LED | |
| 2 | Metal probes | For example two nails or screws, or two wires with stripped ends |
| | Jumper wires | Optionally a breadboard |

## Wiring

| Pin | GPIO (BCM) | Job | Connects to |
| --- | --- | --- | --- |
| 7 | GPIO 4 | Supply pulse | Chain of 3 × 330 Ω and 2 × 10 kΩ in series, ending at the measuring node |
| 11 | GPIO 17 | Reads the node | Measuring node, directly |
| 13 | GPIO 27 | LED | 330 Ω, then the LED's long leg. The short leg goes to GND. |
| 6, 9, … | GND | Return path | Second soil probe and the LED's short leg |

The **measuring node** is the point where the resistor chain, GPIO 17 and the first soil probe meet.

The resistor chain adds up to about 21 kΩ and forms the upper half of a voltage divider. The soil is the lower half. Together with the Pi's internal pull-down (about 50 kΩ), GPIO 17 flips from LOW to HIGH when the soil is around 36 kΩ. This is an estimate, because the switching point of a real input varies a little.

The original schematic is still in the repository: [Feuchtigkeitssensor_Schaltplan.drawio.png](Feuchtigkeitssensor_Schaltplan.drawio.png).

## Run it

Do this on the Raspberry Pi. On Windows or macOS you can edit the script, but the GPIO library only runs on a Pi. The [interactive guide](https://nathanyiel.github.io/Raspberry-Pi_Moisture_Sensor/) lets you try the logic anywhere.

```bash
# 1. GPIO library (Raspberry Pi OS usually has it already)
sudo apt update
sudo apt install python3-rpi.gpio

# 2. Get the code
git clone https://github.com/Nathanyiel/Raspberry-Pi_Moisture_Sensor.git
cd Raspberry-Pi_Moisture_Sensor

# 3. Start the sensor, stop it with Ctrl+C
python3 feuchtigkeits_sensor.py
```

On a **Raspberry Pi 5** install `python3-rpi-lgpio` instead of `python3-rpi.gpio`. It is a drop-in replacement, so the script stays the same.

Example output:

```
Wet (GPIO_IN LOW)
Wet (GPIO_IN LOW)
Dry (GPIO_IN HIGH)
```

## The code in short

The script is [`feuchtigkeits_sensor.py`](feuchtigkeits_sensor.py), about 30 lines.

- `GPIO_OUT = 4`, `GPIO_IN = 17`, `GPIO_LED = 27` use BCM numbering, so these are GPIO numbers and not physical pin numbers.
- `measure_once()` switches the divider on, waits 10 ms, reads GPIO 17, switches the divider off and returns `0` (wet) or `1` (dry).
- The main loop calls `measure_once()`, sets the LED, prints a line and sleeps for two seconds. The interval is easy to change in the last `time.sleep(2.0)`.
- `GPIO.cleanup()` runs when you press Ctrl+C and resets the pins.

## Troubleshooting

| Problem | What to check |
| --- | --- |
| `RuntimeError` about the Raspberry Pi or a missing `RPi` module | The script only runs on a Raspberry Pi with the GPIO library installed. |
| Always prints `Dry` | Both probes in the soil? GND connected? Probes not too far apart? |
| Always prints `Wet` | Probes touching each other? Is the resistor chain connected to GPIO 4? |
| LED never lights up | LED direction (long leg toward GPIO 27), and the 330 Ω resistor in the LED branch. |

## Take it further

- Log the readings with a timestamp to a CSV file and plot how fast your plant dries out.
- Send a push message or email when the soil has been dry several readings in a row.
- Add an analog-to-digital converter such as the MCP3008 to get a percentage instead of wet or dry.
- Drive a small pump through a relay or transistor to water automatically.
- Run the script as a systemd service so it starts on boot.
- Repeat the divider on more GPIO pins to watch several plants.

## Credits

Built by [Jan (lebor32)](https://github.com/lebor32) and [Nate (Nathanyiel)](https://github.com/Nathanyiel). Released under the [MIT license](LICENSE).
