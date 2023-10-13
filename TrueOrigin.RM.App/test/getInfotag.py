import sys
import RPi.GPIO as GPIO
import pn532.pn532 as nfc
from pn532 import *

AUTH0_213   = 0x29
AUTH0_215   = 0x83
AUTH0_216   = 0xE3

PWD_213     = 0x2B
PWD_215     = 0x85
PWD_216     = 0xE5

STORAGE_SIZE_213    = 0x0F
STORAGE_SIZE_215    = 0X11
STORAGE_SIZE_216    = 0X13

STORAGE_INDEX       = 0X07

pn532 = PN532_SPI(debug=False, reset=20, cs=4)
auth0_stamp = None
pwd_stamp = None

ic, ver, rev, support = pn532.get_firmware_version()
print('Found PN532 with firmware version: {0}.{1}'.format(ver, rev))

# Configure PN532 to communicate with NTAG215 cards
pn532.SAM_configuration()

print('Waiting for RFID/NFC card to write to!')

if pn532.Try_connect():
    response = pn532.GetInfoTag()
    
    print(hex(response[STORAGE_INDEX]))
    if hex(response[STORAGE_INDEX]) == hex(STORAGE_SIZE_213):
        auth0_stamp = AUTH0_213
        pwd_stamp = PWD_213
    elif hex(response[STORAGE_INDEX]) == hex(STORAGE_SIZE_215):
        auth0_stamp = AUTH0_215
        pwd_stamp = PWD_215
    elif hex(response[STORAGE_INDEX]) == hex(STORAGE_SIZE_216):
        auth0_stamp = AUTH0_216
        pwd_stamp = PWD_216
    print (hex(auth0_stamp))
    print (hex(pwd_stamp))
    

    


