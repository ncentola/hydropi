import RPi.GPIO as GPIO

class Hardware():
    
    def __init__(self, pin):
        self.is_on = False
        self.pin = pin
        self.schedule = create_schedule()

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(pin, GPIO.OUT)


    def switch(self, current_minute):
        if current_minute in self.schedule:
            if self.is_on:
                pass
            else:
                GPIO.output(self.pin, 1)
        else:
            if self.is_on:
                GPIO.output(self.pin, 0)


class Lights(Hardware):
    def __init__(self):
        pass


class AirPump(Hardware):
    def __init__(self):
        pass


class WaterPump(Hardware):
    def __init__(self):
        pass
