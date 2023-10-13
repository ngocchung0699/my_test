import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import RPi.GPIO as GPIO
import pn532.pn532 as nfc
from pn532 import *

def window():
    app = QApplication(sys.argv)
    win = QDialog()
    b1 = QPushButton(win)
    b1.setText("Button1")
    b1.move(50,20)
    b1.clicked.connect(b1_clicked)
    
    b2 = QPushButton(win)
    b2.setText("Button2")
    b2.move(50,50)
    b2.clicked.connect(b2_clicked)
    
    win.setGeometry(100,100,200,100)
    
    win.setWindowTitle("PyQt5")
    
    win.show()
    sys.exit(app.exec_())

def b1_clicked():
    pn532 = PN532_SPI(debug=False, reset=20, cs=4)
    ic, ver, rev, support = pn532.get_firmware_version()
    print('Found PN532 with firmware version: {0}.{1}'.format(ver, rev))
    # Configure PN532 to communicate with NTAG215 cards
    pn532.SAM_configuration()
    print('Reading for RFID/NFC card!')
    
    block_number = 0
    while True:
        # Check if a card is available to read
        uid = pn532.read_passive_target(timeout=0.5)
        # print('.', end="")
        # Try again if no card is available.
        if uid is None:
            continue
#         pwd = pn532.create_password()
        data = pn532.ntag2xx_write_block_version()
        print(data)
        
#         result = pn532.ntag2xx_read_block(block_number)
#         print('%d', result)
        break

def b2_clicked():
    pn532 = PN532_SPI(debug=False, reset=20, cs=4)

    ic, ver, rev, support = pn532.get_firmware_version()
    print('Found PN532 with firmware version: {0}.{1}'.format(ver, rev))

    # Configure PN532 to communicate with NTAG215 cards
    pn532.SAM_configuration()

    print('Waiting for RFID/NFC card to write to!')
    while True:
        # Check if a card is available to read
        uid = pn532.read_passive_target(timeout=0.5)
        print('.', end="")
        # Try again if no card is available.
        if uid is not None:
            break
        
    print('Found card with UID:', [hex(i) for i in uid])

    # Write block #6
    block_number = 6
    data = bytes([0x02, 0x03, 0x03, 0x04])

    try:
    #result = pn532.ntag2xx_read_block(block_number)
    #print('%d', result)
        pn532.ntag2xx_write_block(block_number, data)
        if pn532.ntag2xx_read_block(block_number) == data:
            print('write block %d successfully' % block_number)
    except nfc.PN532Error as e:
        print(e.errmsg)

if __name__ == '__main__':
   window()
