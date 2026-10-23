import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

GPIO_OUT = 4    # Supplies the voltage divider briefly
GPIO_IN  = 17   # Reads the measuring node
GPIO_LED = 27   # LED indicator

# Setup
GPIO.setup(GPIO_OUT, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(GPIO_IN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(GPIO_LED, GPIO.OUT, initial=GPIO.LOW)

def measure_once(pulse_ms=10):
    # Switch the supply on for a short moment
    GPIO.output(GPIO_OUT, GPIO.HIGH)
    time.sleep(pulse_ms/1000.0)      # e.g. 10 ms
    val = GPIO.input(GPIO_IN)        # 0 = LOW (wet), 1 = HIGH (dry)
    GPIO.output(GPIO_OUT, GPIO.LOW)
    return val

try:
    while True:
        v = measure_once(10)   # 10 ms pulse
        if v == 0:
            # LOW -> wet (the probes pull the node toward GND)
            GPIO.output(GPIO_LED, GPIO.LOW)   # LED off
            print("Wet (GPIO_IN LOW)")
        else:
            # HIGH -> dry: LED on as a warning
            GPIO.output(GPIO_LED, GPIO.HIGH)  # LED on
            print("Dry (GPIO_IN HIGH)")
        time.sleep(2.0)   # Measuring interval in seconds (adjustable)
finally:
    GPIO.cleanup()
