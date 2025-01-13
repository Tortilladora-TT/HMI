#pruebas_propias.py
from hx711 import HX711
import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)
hx = HX711(5, 6)  # Pines DT y SCK
hx.set_reference_unit(1)

print("Tara realizada. Coloca peso en la báscula.")
while True:
    try:
        val = hx.get_weight(5) / 1000  # Convertir a kg
        print(f"Peso: {round(val, 3)} kg")
        hx.power_down()
        hx.power_up()
        time.sleep(1)
    except (KeyboardInterrupt, SystemExit):
        GPIO.cleanup()
        break
