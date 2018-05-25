

class Sensors(object):
    def __init__(self, config):
        self.config = config
        self.values = self.get_sensor_vals()

    def get_sensor_vals(self):
        if self.config.prod_mode:
            global serial
            import serial
            self.values = self.get_real_sensor_vals()
        else:
            global random
            import random
            self.values = self.get_dummy_sensor_vals()

    def get_real_sensor_vals(self):
        thing = serial.Serial('/dev/ttyACM0',9600)
        return thing

    def get_dummy_sensor_vals(self):
        '''
        For testing
        '''
        ph = 6 + random.randint(-10, 10)/100.0
        ec = 800 + random.randint(-200, 200)/100.0
        air_temp = 75 + random.randint(-50, 50)/100.0
        humidity = .4 + random.randint(-2, 2)/100.0
        water_temp = 72 + random.randint(-50, 50)/100.0
        dummy_vals = {
            'ph':           ph,
            'ec':           ec,
            'air_temp':     air_temp,
            'humidity':     humidity,
            'water_temp':   water_temp
        }
        return dummy_vals
