from machine import Pin
import xbee

INPUT_PIN_ID = "D1"

CO_addr = b'\x00\x13\xA2\x00\x41\xCB\xF8\xAC'

print(" +-------------------------+")
print(" | xbee end device program |")
print(" +-------------------------+\n")

xb = xbee.XBee()

input_pin = Pin(INPUT_PIN_ID, Pin.IN, Pin.PULL_UP)

NI = str(xbee.atcmd("NI"))

while True:
    print("start sleeping")
    sleep_ms = xb.sleep_now(None, True)
    if xb.wake_rason() is xbee.PIN_WAKE:
        try:
            xbee.transmit(CO_addr, NI+"mdt")
            print("sent mdt")
        except Exception as e:
            print("Transmit failure:", str(e))
