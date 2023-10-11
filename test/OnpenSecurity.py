import sys
import RPi.GPIO as GPIO
import pn532.pn532 as nfc
from pn532 import *
from hashlib import sha256

pn532 = PN532_SPI(debug=False, reset=20, cs=4)

ic, ver, rev, support = pn532.get_firmware_version()
print('Found PN532 with firmware version: {0}.{1}'.format(ver, rev))

# Configure PN532 to communicate with NTAG215 cards
pn532.SAM_configuration()

print('Waiting for RFID/NFC card to write to!')

if pn532.Try_connect():
    if pn532.GetInfoTag():
        pwd = pn532.CreatePwd()
        if pwd:
            try:
                params = [0x1b] + pwd[0:4]
                response = pn532.Transceive(params = params)
                print('Read frame: ', [hex(i) for i in response])
                confirm_pass = False 
                if response and len(response) >=3:
                    for i, item in enumerate(response[1:]):
                        if hex(pwd[i + 4]) != hex(item):
                            confirm_pass = False
                            break
                        confirm_pass = True    
                # print (confirm_pass)
                if(confirm_pass) :
                    response2 = pn532.Transceive(params = [0x30, pn532.auth0_stamp])
                    print('Read response2: ', [hex(i) for i in response2])
                    if response2:
                        params3 = [0xA2, pn532.auth0_stamp, response2[0] , response2[1], response2[2], 0xff]
                        print('Read params3: ', [hex(i) for i in params3])
                        response3 = pn532.Transceive(params = params3)
                        print (response3)
            except pn532.PN532Error as e:
                print(e)


