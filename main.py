import xbee
from machine import Pin
import time

TARGET_64BIT_ADDR = b'\x00\x13\xA2\x00\x41\xCC\x62\xE4'
#TARGET_64BIT_ADDR = b'\x00\x13\xA2\x00\x41\xCB\xF8\xAC'

srl = '001'

MESSAGE_MOTION = "mdt" #Motion detection
MESSAGE_NO_MOTION = "ucd" #Unchanged

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
        if input_pin.value() == 0 and input_pin.value() != before_state:
#           print("Sending data to %s >> %s" % (''.join('{:02x}'.format(x).upper() for x in TARGET_64BIT_ADDR),
#                                                MESSAGE_NO_MOTION))
            try:
                xbee.transmit(TARGET_64BIT_ADDR, srl + MESSAGE_NO_MOTION)
                print("Data sent successfully")
            except Exception as e:
                print("Transmit failure:", str(e))

        elif input_pin.value() == 1 and input_pin.value() != before_state:
#            print("Sending data to %s >> %s" % (''.join('{:02x}'.format(x).upper() for x in TARGET_64BIT_ADDR),
#                                               MESSAGE_MOTION))
            try:
                xbee.transmit(TARGET_64BIT_ADDR, srl + MESSAGE_MOTION)
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
            elif str(payload.decode()) == srl + MESSAGE_NO_MOTION:
                print("Unchanged")
                before_state = 0
            elif str(payload.decode()) == srl + MESSAGE_MOTION:
                print("Motion detection")
                before_state = 1
            elif str(payload.decode()) == "wakeUp":
                print("wake up res")
                try:
                    xbee.transmit(TARGET_64BIT_ADDR,srl + "wakeUp")
                    print("Data sent successfully")
                except Exception as e:
                    print("Transmit failure:", str(e))

    else:  # SM==1のとき
        #        i = 0
        print("sleep mode")
        sleep_ms = xb.sleep_now(30000, True)
        print("sleepおわり！！")
        
'''
        t = time.time()
        while True:
            to = time.time()
            received_msg = xbee.receive()
            if received_msg:
                payload = received_msg['payload']
                if str(payload.decode()) == 'wakeUp':
                    print("wakeUp")
                    try:
                        xbee.transmit(TARGET_64BIT_ADDR, srl + "wakeUp")
                        print("Data sent successfully")
                    except Exception as e:
                        print("Transmit failure:", str(e))
                    SM = 0
                    break
            if (to - t) >= 5:
                break
'''

    time.sleep(1)
