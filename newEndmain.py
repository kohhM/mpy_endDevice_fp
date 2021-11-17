
import xbee
from machine import Pin
# import time

MESSAGE_MOTION = "mdt"
# Motion detection

MESSAGE_NO_MOTION = "ucd"
# Unchanged

INPUT_PIN_ID = "D1"

CO_addr = b'\x00\x13\xA2\x00\x41\xC6\x25\x94'
# コーディネータのアドレス．要変更

SM = 0
# 0で通常動作，1でスリープ

before_state = 2
# 0でunchanged,1でmotion detection,2が初期値

print(" +-----------------------------+")
print(" | new xbee end device program |")
print(" +-----------------------------+\n")

xb = xbee.XBee()

input_pin = Pin(INPUT_PIN_ID, Pin.IN, Pin.PULL_UP)

NI = str(xbee.atcmd("NI"))

while True:
    if SM == 0:
        if input_pin.value() == 0 and input_pin.value() != before_state:
            print("Sending data to %s >> %s" % (''.join('{:02x}'.format(x).upper() for x in CO_addr),
                                                MESSAGE_NO_MOTION))
            try:
                xbee.transmit(CO_addr, NI + MESSAGE_NO_MOTION)
                print("Data sent successfully")
            except Exception as e:
                print("Transmit failure:", str(e))
                # ここでatコマンドか何かで再接続処理などしたい

        elif input_pin.value() == 1 and input_pin.value() != before_state:
            try:
                xbee.transmit(CO_addr, NI + MESSAGE_MOTION)
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

    else:
        print("sleep mode")
        sleep_ms = xb.sleep_now(800, True)
        print("sleep finished")
        SM = 0

#    time.sleep(1)
