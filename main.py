from machine import Pin
import xbee

NI = str(xbee.atcmd("NI"))
input_pin = Pin("D1", Pin.IN, Pin.PULL_UP)

xb = xbee.XBee()

while True:
    if input_pin.value() == 0:
        sleep_ms = xb.sleep_now(60000,True)
        if xb.wake_reason() is xbee.PIN_WAKE:
            try:
                xbee.transmit(xbee.ADDR_COORDINATOR, NI + "mdt")
            except Exception as e:
                print("Transmit failure:", str(e))
                
