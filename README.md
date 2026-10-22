# Raspi Moisture Sensor # 🌱 Plant Moisture Monitor

A Raspberry Pi project to **monitor soil moisture** using simple components.  
The script regularly checks the soil moisture and provides feedback via an LED and the console.  

> Goal: Never forget to water your plants again! 💧

---

## ✨ Features
- 📊 **Soil moisture measurement** using simple components
- 🌡️ **Boolean output** (wet/dry)  
- 🚨 **Dryness alert** (Console, LED)
- 🕐 **Configurable interval** to reduce probe corrosion

---

## 🔧 Hardware Setup

### Required Components
- Raspberry Pi (with SPI enabled)
- 4x 330 Ω resistors
- 2x 1 kΩ resistors
- 1x LED
- Jumper wires

# 🧰 Installation & Required Libraries

This project uses the Python library **RPi.GPIO** to control the GPIO pins of the Raspberry Pi.  
It is used to both read the moisture sensor and control an LED.

> **Note:** > This library **only works on an actual Raspberry Pi**.  
> You can edit the script on Windows or macOS, but you **cannot run it**.

---

## 💻 Installation on the Raspberry Pi

### Open Terminal
- Raspberry Menu → **Accessories → Terminal** or  
- **Ctrl + Alt + T**

### Install Libraries
```bash
sudo apt update
sudo apt install python-rpi-gpio
```

## 🪟 Windows Users

Windows cannot interface with Raspberry Pi GPIO pins.  
The script **cannot be executed**, but it can be **edited** normally.

### Open CMD
- Start Menu → type **cmd** → Enter

### Open PowerShell
- Start Menu → type **PowerShell** → Enter

---

## 🍎 macOS Users

macOS also cannot control Raspberry Pi GPIOs.  
The script can only be **edited or managed** here.

### Open Terminal
- **Cmd + Spacebar** → type "Terminal" → Enter  
or  
- Finder → **Applications → Utilities → Terminal**

---

## ▶️ Running the Script (Raspberry Pi only)

```bash
python feuchtigkeits_sensor.py
