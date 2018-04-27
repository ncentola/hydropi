import datetime
import serial

class HydroPi():
    def __init__(self, config):
        self.config = config
        self.serial = serial.Serial('/dev/ttyACM0',9600)

    def start(self):

        while True:
            now = datetime.datetime.now()
            current_minute = (now.hour * 60) + now.minute


            # test_serial = self.serial.readline()
