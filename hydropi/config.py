from configparser import ConfigParser
import json

class Config():
    def __init__(self, path_to_config_file):
        cfp = ConfigParser()
        cfp.read(path_to_config_file)

        self.method = cfp.get('general', 'method')
        self.day_start = int(cfp.get('general', 'day_start'))
        self.day_end = int(cfp.get('general', 'day_end'))

        self.air_pump_pin = int(cfp.get('general', 'air_pump_pin'))
        self.lights_pin = int(cfp.get('general', 'lights_pin'))
        self.water_pump_pin = int(cfp.get('general', 'water_pump_pin'))

        self.lights_starts = list(range(self.day_start, self.day_end+1))
        self.lights_on_mins = 60

        self.air_pump_starts = json.loads(cfp.get(self.method, 'air_pump_starts'))
        self.air_pump_time_on_mins = int(cfp.get(self.method, 'air_pump_time_on_mins'))

        self.water_pump_starts = json.loads(cfp.get(self.method, 'water_pump_starts'))
        self.water_pump_time_on_mins = int(cfp.get(self.method, 'water_pump_time_on_mins'))
