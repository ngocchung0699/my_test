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
        try:
            response = pn532.Transceive(params = [0x30, 0])
            uid = response[1:9]
            str_uid = ''.join(str(format(e, 'x')) for e in uid)
            uid_hash = sha256(bytes.fromhex(str_uid)).digest()
            # hx = hash.hexdigest()
            # uid_hash = sha256(str_uid.encode('utf-8')).digest()
            pwd = [uid_hash[2], uid_hash[0], uid_hash[1], uid_hash[5], uid_hash[0], uid_hash[3]]

            print('Read frame: ', [hex(i) for i in pwd])
            # print(str_uid)
            # print(uid_hash)
        except pn532.PN532Error as e:
            print(e)
    

    


