
import xbee
from machine import Pin
import time

INPUT_PIN_ID = "D1"
CO_ADDR = b'\x00\x13\xA2\x00\x41\xC6\x25\x94'

print(" +------------------+")
print(" | New XBee test MP |")
print(" +------------------+\n")

input_pin = Pin(INPUT_PIN_ID, Pin.IN, Pin.PULL_UP)
print("Sending data to %s >> %s" % (''.join('{:02x}'.format(x).upper() for x in CO_ADDR), str(input_pin.value())))

while True:
    try:
        xbee.transmit(CO_ADDR, str(input_pin.value()))
        time.sleep(5)
    except Exception as e:
        print("えらー>>> %s", str(e))
        time.sleep(2)
