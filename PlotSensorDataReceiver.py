import random, threading, time

class PlotSensorDataReceiver:
    """
    NOTE:
    - crops are inside of 8" pots
    - 1" of water = 1 second of sprinkler = 12.5% of moisture
    - system can supply 1" of water in 1 second, so it takes 8s to fully fill a plot
    """


    def __init__(self, plotNum, growthRequirements:dict, socket):
        self.socket = socket

        self.plot_num = int(plotNum)
        self.threadingIsActive = False
        self.timeReceiverStartedCollecting = time.time()

        self.sprinklerStatus = 0 # 0 = OFF / 1 = ON
        self.sprinklerDuration = 0 # seconds
        self.tempModifierStatus = 0 # 0 = OFF / 1 = ON
        self.tempModifierDuration = 0 # seconds

        self.requiredMoisture = (float(growthRequirements['waterDepth']) / 8.0) * 100
        required_pH_range = growthRequirements['pH'].split(' - ')
        required_seedTemp_range = growthRequirements['seedTemperature'].split(' - ')
        required_cropTemp_range = growthRequirements['cropTemperature'].split(' - ')

        self.wateringInterval = int(growthRequirements['wateringInterval'] * 3600)

        self.required_min_pH = float(required_pH_range[0])
        self.required_max_pH = float(required_pH_range[1])
        self.new_pH = 0.0

        self.required_seed_minTemp = float(required_seedTemp_range[0])
        self.required_seed_maxTemp = float(required_seedTemp_range[1])
        self.required_crop_minTemp = float(required_cropTemp_range[0])
        self.required_crop_maxTemp = float(required_cropTemp_range[1])



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
        # self.__generateChange(random.uniform,'co2_concentration', -100.0, 100.0, 500.0, 2000.0)
        # self.__generateChange(random.randint, 'light_levels', -100, 100, 0.0, 10000)



        ### SOIL MOISTURE & SOIL PH ###
        if self.sprinklerDuration == 0:
            self.sprinklerStatus = 0 # turns off sprinkler

        currentElapsedTime = int(time.time() - self.timeReceiverStartedCollecting)

        if self.sprinklerStatus == 0:
            if self.soil_pH < self.required_min_pH or self.soil_pH > self.required_max_pH:
                # handles pH regulation (**is prioritized over moisture requirement; sprinkler is turned on for a long duration to ensure the minimum pH requirement is reached)
                self.activateSprinkler(10, self.required_min_pH)
                self.socket.send({'sprinkler':10})
            elif currentElapsedTime % self.wateringInterval == 0 and self.soil_moisture < 1.0:
                # handles watering interval
                self.activateSprinkler(int(self.requiredMoisture / 12.5), self.required_min_pH)

        if self.sprinklerStatus == 0 and currentElapsedTime % 5 == 0:
            # makes soil moisture fluctuate by 0% to 0.05% every 5 seconds
            self.__generateChange(random.uniform, 'soil_moisture', -0.05, 0.0, 0.0, 100.0)

            # makes pH fluctuate by 0.01 to 0.05 every 5 seconds
            self.__generateChange(random.uniform, 'soil_pH', 0.01, 0.05, 0.0, 14.0)

        elif self.sprinklerStatus == 1 and self.sprinklerDuration > 0:
            newMoisture = self.soil_moisture + 12.5

            # changes moisture
            if newMoisture < 100.0:
                self.soil_moisture = newMoisture
                self.sprinklerDuration -= 1
            else:
                self.sprinklerDuration = 0

            # changes pH
            pH_difference = abs(self.new_pH - self.soil_pH)
            pH_min_change = 1.0

            if (pH_difference - 2.0 > 0):
                pH_min_change = pH_difference - 2.0

            new_pH = random.uniform(pH_min_change, pH_difference)

            if self.new_pH > self.soil_pH and self.soil_pH + new_pH < 14.0:
                self.soil_pH += new_pH
            elif self.new_pH < self.soil_pH and self.soil_pH - new_pH > 0.0:
                self.soil_pH -= new_pH



        ### SOIL TEMPERATURE ###


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

    def activateSprinkler(self, duration:int, pH):
        self.sprinklerStatus = 1
        self.sprinklerDuration = duration

        self.new_pH = pH

    def activateTemperatureModifier(self, duration:int, temp):
        print(duration)
        print(temp)
