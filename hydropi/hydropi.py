from .hardware import AirPump, Lights, WaterPump
from .sensors import Sensors
from copy import copy
import datetime, time
import pandas as pd
from . import db


class HydroPi():
    def __init__(self, config):
        self.config = config

        self.hardware = {
            'air_pump':     AirPump(self.config),
            'lights':       Lights(self.config),
            'water_pump':   WaterPump(self.config)
        }

        self.system_minute = None
        self.sensors = Sensors(self.config)
        self.db_con = db.db_con

    def run(self):

        while True:
            now = datetime.datetime.now()
            current_minute = (now.hour * 60) + now.minute
            # self.sensors.get_sensor_vals()
            # self.log(now=now)
            # check respective hardware schedules each new minute
            if self.system_minute != current_minute:
                self.switch_all_the_things(self.hardware, current_minute)
                self.sensors.get_sensor_vals()

                print('Minute', current_minute)
                print('Air Pump ON   -', self.hardware['air_pump'].is_on)
                print('Lights ON     -', self.hardware['lights'].is_on)
                print('Water Pump ON -', self.hardware['water_pump'].is_on)

                print(self.sensors.values)
                print('----------------------------')
                self.log(now=now)
                self.system_minute = current_minute

            time.sleep(1)
                # test_serial = self.serial.readline()

    def switch_all_the_things(self, the_things, current_minute):
        for thing in the_things.values():
            thing.switch(current_minute)

    def log(self, now):

        vals = copy(self.sensors.values)
        vals['created_at'] = now
        vals['air_pump_on'] = self.hardware['air_pump'].is_on
        vals['lights_on'] = self.hardware['lights'].is_on
        vals['water_pump_on'] = self.hardware['water_pump'].is_on

        df = pd.DataFrame(vals, index=[0])
        df.to_sql(name='readings', con=db.db_con, if_exists='append', index=False)
