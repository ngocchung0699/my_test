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
    # print("read1_____________")
    # response = pn532.Read_page(6)
    # print('Read frame: ', [hex(i) for i in response])

    # print("read2_____________")
    # response = pn532.Read_page1(6)
    # print('Read frame: ', [hex(i) for i in response])

    # if pn532.GetInfoTag():
    #     pwd = pn532.CreatePwd()
    #     print(pn532.SetPwd(pwd))


    if pn532.GetInfoTag():
        pwd = pn532.CreatePwd()
        if pwd:
            is_protected = pn532.IsProtectedPwd()
            if is_protected: 
                if pn532.Try_connect():   
                    if pn532.OpenSecurity(pwd):
                        print ("reset pw thanh cong")
                        # print(pn532.SetPwd(pwd))
                    else:
                        print ("reset pw error")
            else:
                print ("-----------------------")
                print ("Set pw khong co mat khau")
                print(pn532.SetPwd(pwd))
            




