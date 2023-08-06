import time
from datetime import datetime
import statistics
try:
    from smbus2 import SMBus
except ImportError:
    from smbus import SMBus
from .libs.bme280 import BME280
from pymongo import MongoClient


class OneHomeSensor:
    def __init__(self, running_args,mongodb_con,corrections):
        self.print_only = running_args.print_only
        self.readings = int(running_args.readings)
        self.mongodb_con = mongodb_con
        self.sensor_instance_name = running_args.sensor_name
        self.waitetime = float(running_args.waitetime)
        self.tempCorrection = corrections.get('temp',0)

    def push_to_mongodb(self,temperature,pressure,humidity):
        client = MongoClient(self.mongodb_con)
        db = client.onehomesensor
        readings = db['readings_'+self.sensor_instance_name]
        time = int(datetime.now().timestamp())
        readings.insert_one({
            'ti' : str(time),
            'te': "{:05.2f}".format(temperature),
            'pr': "{:05.2f}".format(pressure),
            'hu': "{:05.2f}".format(humidity),
        })


    def run(self):        
        # Initialise the BME280
        bus = SMBus(1)
        bme280 = BME280(i2c_dev=bus)
        temperatures = []
        pressures = []
        humiditys = []
        # Read sensors 
        for i in range(self.readings):
            time.sleep(self.waitetime) # initialisation take a little time from what I hav tested
            temperatures.append(bme280.get_temperature())
            pressures.append(bme280.get_pressure())
            humiditys.append(bme280.get_humidity())
        if self.readings > 5: # extract extrem values from the readings
            temperatures = sorted(temperatures)[1:-1]
            pressures = sorted(pressures)[1:-1]
            humiditys = sorted(humiditys)[1:-1]
        temperature = statistics.mean(temperatures) + self.tempCorrection
        pressure = statistics.mean(pressures)
        humidity = statistics.mean(humiditys)

        # Output sensors Data 
        if self.print_only:
            print('{:05.2f}*C {:05.2f}hPa {:05.2f}%'.format(temperature, pressure, humidity))
        else: 
            self.push_to_mongodb(temperature,pressure,humidity)
