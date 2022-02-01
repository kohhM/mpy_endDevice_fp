
from machine import Pin
import xbee

INPUT_PIN_ID = "D1"

CO_addr = b'\x00\x13\xA2\x00\x41\xCB\xF8\xAC'

NI = str(xbee.atcmd("NI"))
input_pin = Pin(INPUT_PIN_ID, Pin.IN, Pin.PULL_UP)

xb = xbee.XBee()

while True:
    if input_pin.value() == 0:
        sleep_ms = xb.sleep_now(60000,True)
        if xb.wake_reason() is xbee.PIN_WAKE:
            try:
                xbee.transmit(CO_addr, NI + "mdt")
            except Exception as e:
                print("Transmit failure:", str(e))
                
