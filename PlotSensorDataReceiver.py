import random, threading, time

class PlotSensorDataReceiver:
    """
    NOTE:
    - crops are inside of 8" pots
    - 1" of water = 1 second of sprinkler = 12.5% of moisture
    - system can supply 1" of water in 1 second, so it takes 8s to fully fill a plot
    """


    def __init__(self, plotNum, growthRequirements:dict):
        self.plot_num = int(plotNum)
        self.threadingIsActive = False
        self.timeReceiverStartedCollecting = time.time()

        self.sprinklerStatus = 0 # 0 = OFF / 1 = ON
        self.sprinklerDuration = 0 # seconds

        self.requiredMoisture = (float(growthRequirements['waterDepth']) / 8.0) * 100
        self.wateringInterval = int(growthRequirements['wateringInterval'] * 3600)



        # initializing crop variables with average values
        self.soil_temp = round(random.uniform(6.0, 8.0), 2) # celsius
        self.soil_pH = round(random.uniform(6.0, 7.0), 2) # pH scale
        self.co2_concentration = round(random.uniform(400.0, 500.0), 2) # ppm
        self.soil_moisture = round(random.uniform(8.0, 10.0), 2) # %
        self.light_levels = random.randint(9000, 10000) # lux

    def __str__(self):
        return f"Sensor data for Plot {self.plot_num}"



    # PRIVATE
    def __generateChange(self, randomFunc, metric, changeMin, changeMax, metricMin, metricMax):

        metricToChange = getattr(self, metric)
        change = randomFunc(changeMin, changeMax)
        newValue = round(metricToChange + change, 2)

        # Keeps new value for sensor variable within its scale (e.g. pH within 0-14)
        while (newValue < metricMin or newValue > metricMax):
            change = randomFunc(changeMin, changeMax)
            newValue = round(metricToChange + change, 2)

        setattr(self, metric, newValue)

    def __collectNewData(self):
        # generates changes to variables based on constraints
        # self.__generateChange(random.uniform, 'soil_temp', -0.8, 0.8, -30.0, 30.0)
        # self.__generateChange(random.uniform, 'soil_pH', -0.5, 0.5, 0.0, 14.0)
        # self.__generateChange(random.uniform,'co2_concentration', -100.0, 100.0, 500.0, 2000.0)
        # self.__generateChange(random.randint, 'light_levels', -100, 100, 0.0, 10000)



        ### SOIL MOISTURE & SOIL PH ###
        if self.sprinklerDuration == 0:
            self.sprinklerStatus = 0 # turns off sprinkler

        currentElapsedTime = int(time.time() - self.timeReceiverStartedCollecting)

        # handles watering interval
        if self.sprinklerStatus == 0 and currentElapsedTime % self.wateringInterval == 0 and self.soil_moisture < 1.0:
            self.activateSprinkler(int(self.requiredMoisture / 12.5))

        if self.sprinklerStatus == 0 and currentElapsedTime % 5 == 0:
            # decreases soil moisture by 0% to 0.05% every 5 seconds
            self.__generateChange(random.uniform, 'soil_moisture', -0.05, 0.0, 0.0, 100.0)
        elif self.sprinklerStatus == 1 and self.sprinklerDuration > 0:
            newMoisture = self.soil_moisture + 12.5

            if newMoisture < 100.0:
                # NOTE: receivers collect new data every second (see above to understand why this info is important)
                self.soil_moisture = newMoisture
                self.sprinklerDuration -= 1
            else:
                self.sprinklerDuration = 0



        self.listen() # repeats collection


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
    def startListening(self):
        self.threadingIsActive = True

    def stopListening(self):
        self.threadingIsActive = False

    def listen(self):
        if (self.threadingIsActive):
            sensorThread = threading.Timer(1.0, self.__collectNewData)
            sensorThread.start()

    def activateSprinkler(self, duration:int):
        self.sprinklerStatus = 1
        self.sprinklerDuration = duration
