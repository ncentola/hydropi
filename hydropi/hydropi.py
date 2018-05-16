from .hardware import AirPump, Lights, WaterPump
import datetime, time
#import serial

class HydroPi():
    def __init__(self, config):
        self.config = config

        self.hardware = {
            'air_pump':     AirPump(self.config),
            'lights':       Lights(self.config),
            'water_pump':   WaterPump(self.config)
        }

        self.system_minute = None
        #self.serial = serial.Serial('/dev/ttyACM0',9600)

    def run(self):

        while True:
            now = datetime.datetime.now()
            current_minute = (now.hour * 60) + now.minute

            # check respective hardware schedules each new minute
            if self.system_minute != current_minute:
                self.switch_all_the_things(self.hardware, current_minute)
                print('Minute', current_minute)
                print('Air Pump ON   -', self.hardware['air_pump'].is_on)
                print('Lights ON     -', self.hardware['lights'].is_on)
                print('Water Pump ON -', self.hardware['water_pump'].is_on)
                print('----------------------------')
                self.system_minute = current_minute

            time.sleep(5)
                # test_serial = self.serial.readline()

    def switch_all_the_things(self, the_things, current_minute):
        for thing in the_things.values():
            thing.switch(current_minute)
