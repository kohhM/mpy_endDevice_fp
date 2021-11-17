
import xbee
from machine import Pin
# import time

INPUT_PIN_ID = "D1"

CO_addr = b'\x00\x13\xA2\x00\x41\xC6\x25\x94'
# コーディネータのアドレス．要変更

SM = 0
# 0で通常動作，1でスリープ

before_state = 0
# 0でunchanged,1でmotion detection

print(" +-----------------------------+")
print(" | new xbee end device program |")
print(" +-----------------------------+\n")

xb = xbee.XBee()

input_pin = Pin(INPUT_PIN_ID, Pin.IN, Pin.PULL_UP)

while True:
    if SM == 0:
        if input_pin.value() == 0 and input_pin.value() != before_state:
            try:
                xbee.transmit(CO_addr, 'ucd')
                print("sent ucd")
                before_state = 0
            except Exception as e:
                print("Transmit failure:", str(e))
                # ここでatコマンドか何かで再接続処理などしたい

        elif input_pin.value() == 1 and input_pin.value() != before_state:
            try:
                xbee.transmit(CO_addr, 'mdt')
                print("sent mdt")
                before_state = 1
            except Exception as e:
                print("Transmit failure:", str(e))
        else:
            pass

        received_msg = xbee.receive()
        if received_msg:
            payload = received_msg['payload']
            if str(payload.decode()) == 'sleep':
                print("sleeping")
                SM = 1

    else:
        print("sleep mode")
        sleep_ms = xb.sleep_now(800, True)
        print("sleep finished")
        SM = 0

#    time.sleep(1)
