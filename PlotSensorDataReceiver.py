import random

class PlotSensorDataReceiver:
    def __init__(self, plotNum):
        self.plot_num = plotNum

        # initializing crop variables with average values
        self.soil_temp = random.uniform(6.0, 8.0) # celsius
        self.soil_pH = random.uniform(6.0, 7.0) # pH scale
        self.co2_concentration = random.uniform(400.0, 500.0) # ppm
        self.soil_moisture = random.uniform(10.0, 12.5) # %
        self.light_levels = random.randint(9000, 10000) # lux

    def __str__(self):
        return f"Sensor data for Plot {self.plot_num}"


    # GETTERS
    def getData(self):
        data = {
            "plotNum" : self.plot_num,
            "soilTemp" : self.soil_temp,
            "pH" : self.soil_pH,
            "co2" : self.co2_concentration,
            "moisture" : self.soil_moisture,
            "lighting" : self.light
        }

        return data


    # SETTERS
    def collectNewData(self):
        self.soil_temp += random.uniform(-5.0, 5)
        self.soil_pH += random.uniform(0, 3.0)
        self.co2_concentration += random.uniform(0, 300.0)
        self.soil_moisture += random.uniform(0, 5.0)
        self.light_levels += random.randint(0, 2000)
