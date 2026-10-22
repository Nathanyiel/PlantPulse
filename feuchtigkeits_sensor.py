import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

GPIO_OUT = 4    # Versorgt Divider kurz
GPIO_IN  = 17   # Liest Messknoten
GPIO_LED = 27   # LED-Anzeige

# Setup
GPIO.setup(GPIO_OUT, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(GPIO_IN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(GPIO_LED, GPIO.OUT, initial=GPIO.LOW)

def measure_once(pulse_ms=10):
    # Versorgung kurz einschalten
    GPIO.output(GPIO_OUT, GPIO.HIGH)
    time.sleep(pulse_ms/1000.0)      # z.B. 10 ms
    val = GPIO.input(GPIO_IN)        # 0 = LOW (wahrscheinlich feucht), 1 = HIGH (trocken)
    GPIO.output(GPIO_OUT, GPIO.LOW)
    return val

try:
    while True:
        v = measure_once(10)   # 10 ms Pulse
        if v == 0:
            # LOW -> feucht (Probe zieht Knoten Richtung GND)
            GPIO.output(GPIO_LED, GPIO.LOW)   # LED an (oder invertieren je nach Schaltung)
            print("Feucht (GPIO_IN LOW)")
        else:
            GPIO.output(GPIO_LED, GPIO.HIGH)
            print("Trocken (GPIO_IN HIGH)")
        time.sleep(2.0)   # Messintervall 2s (anpassbar)
finally:
    GPIO.cleanup()
