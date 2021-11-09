import xbee
from machine import Pin
import time

S101_addr = b'\x00\x13\xA2\x00\x41\xB7\x9A\xB7'
R501_addr = b'\x00\x13\xA2\x00\x41\xCC\x62\xE4'
R401_addr = b'\x00\x13\xA2\x00\x41\xCC\x0D\x58'
R301_addr = b'\x00\x13\xA2\x00\x41\xCD\x90\xE0'
R201_addr = b'\x00\x13\xA2\x00\x41\xCC\x62\x89'
R101_addr = b'\x00\x13\xA2\x00\x41\xB7\x97\xB7'
R102_addr = b'\x00\x13\xA2\x00\x41\xCC\x62\xD9'
cood_ADDR = b'\x00\x13\xA2\x00\x41\xCB\xF8\xAC'

MESSAGE_MOTION = "mdt"
# Motion detection
MESSAGE_NO_MOTION = "ucd"
# Unchanged

INPUT_PIN_ID = "D1"

SM = 0
# 0で通常動作、1でスリープ

before_state = 2

print(" +-----------------------------+")
print(" | send PIR Motion Sensor info |")
print(" +-----------------------------+\n")

xb = xbee.XBee()

input_pin = Pin(INPUT_PIN_ID, Pin.IN, Pin.PULL_UP)

NI = str(xbee.atcmd("NI"))
if NI == 'S101':
    TARGET_64BIT_ADDR = R501_addr
else:
    TARGET_64BIT_ADDR = R501_addr

while True:
    if SM == 0:
        if input_pin.value() == 0 and input_pin.value() != before_state:
            print("Sending data to %s >> %s" % (''.join('{:02x}'.format(x).upper() for x in TARGET_64BIT_ADDR),
                                                MESSAGE_NO_MOTION))
            try:
                xbee.transmit(TARGET_64BIT_ADDR, NI + MESSAGE_NO_MOTION)
                print("Data sent successfully")
            except Exception as e:
                print("Transmit failure:", str(e))

        elif input_pin.value() == 1 and input_pin.value() != before_state:
            try:
                xbee.transmit(TARGET_64BIT_ADDR, NI + MESSAGE_MOTION)
                print("Data sent successfully")
            except Exception as e:
                print("Transmit failure:", str(e))

        else:
            pass

        received_msg = xbee.receive()
        if received_msg:
            sender = received_msg['sender_eui64']
            payload = received_msg['payload']
            print("Data received from %s >> %s" % (''.join('{:02x}'.format(x).upper() for x in sender),
                                                   payload.decode()))
            if str(payload.decode()) == 'sleep':
                print("sleeping")
                SM = 1
            elif str(payload.decode()) == NI + MESSAGE_NO_MOTION:
                print("Unchanged")
                before_state = 0
            elif str(payload.decode()) == NI + MESSAGE_MOTION:
                print("Motion detection")
                before_state = 1
            elif str(payload.decode()) == "wakeUp":
                print("wake up res")
                try:
                    xbee.transmit(TARGET_64BIT_ADDR, NI + "wakeUp")
                    print("Data sent successfully")
                except Exception as e:
                    print("Transmit failure:", str(e))

    else:  # SM==1のとき
        #        i = 0
        print("sleep mode")
        sleep_ms = xb.sleep_now(800, True)
        print("sleep finished")
        SM = 0

    time.sleep(1)
