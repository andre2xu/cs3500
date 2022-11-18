import time
import random

class PlotGenerator:
    def __init__(self):
        self.plot_id = random.randint(1, 99999)
        self.soil_temp = random.randint(-20, 100)
        self.soil_ph = random.randint(5,9)
        self.co2 = random.randint(200, 2000)
        self.soil_moisture = random.randint(1,100)
        self.light = random.randint(0,10000)


    def package_data(self):
        data = {
                "plot" : self.plot_id,
                "model" : self.soil_temp,
                "soil_ph" : self.soil_ph,
                "co2" : self.co2,
                "moisture" : self.soil_moisture,
                "light" : self.light,
                }
        return data

    