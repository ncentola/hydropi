# HydroPi - Hydroponics with Raspberry Pi & Arduino

A brain and monitoring system for your hydroponics setup
![Alt text](dashboard.png?raw=true "Optional Title")
## Overview

### Arduino
Arduino will serve as an aggregator for the following sensors:
* pH
* Water Temperature
* Air Temperature & Humidity
* Electro-Conductivity/TDS

Sensor data will be transmitted via USB (serial) to rPi for use in application.

### Raspberry Pi
The brains of the operation. Using a [config file](config.ini) and [custom scheduling functionality](/hydropi/schedule.py), the rPi provides a minute-by-minute schedule to run the lights and motors. Will also log the state of the system to a DB of your choice

## How-To
Run the thing with...
```
./start.sh
```
