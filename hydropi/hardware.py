from .schedule import Schedule
from warnings import warn

# use this for dev where you can't install the gpio lib
gpio_working=False
try:
    import RPi.GPIO as GPIO
    gpio_working=True
except:
    warn('RPi.GPIO not found, GPIO functionality will not work')


class Hardware():

    def __init__(self, pin, raw_schedule):
        self.is_on = False
        self.pin = pin
        self.schedule = Schedule(raw_schedule)

        if gpio_working:
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(pin, GPIO.OUT)


    def switch(self, current_minute):
        # check schedule to see if the thing is supposed to be on in the current minute
        if self.schedule.minutes[current_minute]:
            if self.is_on:
                pass
            else:
                if gpio_working:
                    GPIO.output(self.pin, 1)
                self.is_on = True
        else:
            if self.is_on:
                if gpio_working:
                    GPIO.output(self.pin, 0)
                self.is_on = False


class Lights(Hardware):
    def __init__(self, config):
        pin = config.lights_pin
        raw_schedule = {
            'hour_starts':      config.lights_starts,
            'duration_mins':    config.lights_on_mins
        }
        super(Lights, self).__init__(pin=pin, raw_schedule=raw_schedule)


class AirPump(Hardware):
    def __init__(self, config):
        pin = config.air_pump_pin
        raw_schedule = {
            'hour_starts':      config.air_pump_starts,
            'duration_mins':    config.air_pump_time_on_mins
        }
        super(AirPump, self).__init__(pin, raw_schedule)


class WaterPump(Hardware):
    def __init__(self, config):
        pin = config.water_pump_pin
        raw_schedule = {
            'hour_starts':      config.water_pump_starts,
            'duration_mins':    config.water_pump_time_on_mins
        }
        super(WaterPump, self).__init__(pin, raw_schedule)
