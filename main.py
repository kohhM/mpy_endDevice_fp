
import xbee
from machine import Pin
import time

TARGET_64BIT_ADDR = b'\x00\x13\xA2\x00\x41\xCC\x0D\x58'

MESSAGE_MOTION = "Motion detection"
MESSAGE_NO_MOTION = "Unchanged"

INPUT_PIN_ID = "D1"

SM = 0
# 0で通常動作、1でスリープ

before_state = 2

print(" +-----------------------------+")
print(" | send PIR Motion Sensor info |")
print(" +-----------------------------+\n")

xb = xbee.XBee()

input_pin = Pin(INPUT_PIN_ID, Pin.IN, Pin.PULL_UP)

while True:
    if SM == 0:
#        print("- Digital input value:", input_pin.value())
        if input_pin.value() == 0 and input_pin.value() != before_state:
            print("Sending data to %s >> %s" % (''.join('{:02x}'.format(x).upper() for x in TARGET_64BIT_ADDR),
                                                MESSAGE_NO_MOTION))
            before_state = 0
            try:
                xbee.transmit(TARGET_64BIT_ADDR, MESSAGE_NO_MOTION)
                print("Data sent successfully")
            except Exception as e:
                print("Transmit failure:", str(e))
        elif input_pin.value() == 1 and input_pin.value() != before_state:
            print("Sending data to %s >> %s" % (''.join('{:02x}'.format(x).upper() for x in TARGET_64BIT_ADDR),
                                                MESSAGE_MOTION))
            before_state = 1
            try:
                xbee.transmit(TARGET_64BIT_ADDR, MESSAGE_MOTION)
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
    else:  # SM==1のとき
        #        i = 0
        print("sleep mode")
        sleep_ms = xb.sleep_now(30000, True)

        t = time.time()
        while True:
            to = time.time()
            received_msg = xbee.receive()
            if received_msg:
                payload = received_msg['payload']
                if str(payload.decode()) == 'wakeUp':
                    print("wakeUp")
                    SM = 0
                    break
            if (to - t) >= 5:
                break

    time.sleep(1)