import random, threading

class PlotSensorDataReceiver:
    def __init__(self, plotNum):
        self.plot_num = plotNum

        # initializing crop variables with average values
        self.soil_temp = round(random.uniform(6.0, 8.0), 2) # celsius
        self.soil_pH = round(random.uniform(6.0, 7.0), 2) # pH scale
        self.co2_concentration = round(random.uniform(400.0, 500.0), 2) # ppm
        self.soil_moisture = round(random.uniform(10.0, 12.5), 2) # %
        self.light_levels = random.randint(9000, 10000) # lux

    def __str__(self):
        return f"Sensor data for Plot {self.plot_num}"



    # PRIVATE
    def __generateChange(self, randomFunc, metric, changeMin, changeMax, metricMin, metricMax):
        metricToChange = getattr(self, metric)

        change = randomFunc(changeMin, changeMax)
        newValue = round(metricToChange + change, 2)

        # keeps new value for sensor variable within its scale (e.g. pH within 0-14) 
        while (newValue < metricMin and newValue > metricMax):
            newValue = round(metricToChange + change, 2)

        setattr(self, metric, newValue)


    # GETTERS
    def getData(self):
        data = {
            "plotNum" : self.plot_num,
            "soilTemp" : self.soil_temp,
            "pH" : self.soil_pH,
            "co2" : self.co2_concentration,
            "moisture" : self.soil_moisture,
            "lighting" : self.light_levels
        }

        return data


    # SETTERS
    def collectNewData(self):
        self.__generateChange(random.uniform, 'soil_temp', -2.0, 2.0, -30.0, 30.0)
        self.__generateChange(random.uniform, 'soil_pH', -2.0, 2.0, 0.0, 14.0)
        self.__generateChange(random.uniform,'co2_concentration', -100.0, 100.0, 500.0, 2000.0)
        self.__generateChange(random.uniform, 'soil_moisture', -2.0, 2.0, 0.0, 100.0)
        self.__generateChange(random.randint, 'light_levels', -100, 100, 0.0, 10000)

        self.listen() # repeats collection

    def listen(self):
        sensorThread = threading.Timer(1.0, self.collectNewData)
        sensorThread.start()