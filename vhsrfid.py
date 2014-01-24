import serial
import time
from datetime import datetime
import requests


def log(message):
    print("[{0}] {1}".format(datetime.now().isoformat(), message))


def initserial():
    init = False

    while not init:
        try:
            log("attempting to init serial")
            time.sleep(0.1)
            ser = serial.Serial("/dev/rfid-reader", baudrate=2400)
            init = True
            log("serial initialized, listening...")
        except serial.serialutil.SerialException:
            log("failed to init serial")
            pass

    return ser


def readkey():
    if c == 'v':
        key = ser.read(8)

        log("Scanned: {0}".format(key))

        key = key.strip()
        r = requests.get('http://localhost/authorize/{0}/'.format(key))

        log("Response: {0}".format(r.text))

        if r.text == "AUTHORIZED":
            log("Authorized {0}".format(key))
            ser.write('t')
            ser.write('d')
            ser.write('Access Granted!\r')
            time.sleep(5)
            ser.write('d')
            ser.write('{0}\r'.format(datetime.now().strftime("%m/%d-%H:%M:%S")))
        else:
            log("Unauthorized {0}".format(key))
            ser.write('d')
            ser.write('Access Denied!\r')
            time.sleep(5)
            ser.write('d')
            ser.write('{0}\r'.format(datetime.now().strftime("%m/%d-%H:%M:%S")))


ser = initserial()

while True:
    time.sleep(0.001)
    try:
        c = ser.read(1)
    except serial.serialutil.SerialException:
        ser = initserial()
        print("SerialException occured.. ignoring.. attempting to re-initalizing serial")
        pass

    if c == 'v':
        try:
            readkey()
        except serial.serialutil.SerialException:
            ser = initserial()
            print("SerialException occured.. ignoring.. attempting to re-initalizing serial")
            pass
