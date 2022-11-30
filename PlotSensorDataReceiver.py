import random, threading, time, datetime

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

        # STATUS: 0 = OFF / 1 = ON
        # DURATION UNIT: seconds
        self.sprinklerStatus = 0
        self.sprinklerDuration = 0
        self.tempModifierStatus = 0
        self.tempModifierDuration = 0
        self.lightModifierStatus = 1
        self.lightModifierDuration = int(growthRequirements['lightExposureDuration'] * 3600)

        self.requiredMoisture = (float(growthRequirements['waterDepth']) / 8.0) * 100
        self.wateringInterval = int(growthRequirements['wateringInterval'] * 3600)

        self.requiredLightExposure = growthRequirements['lightExposureDuration'] * 3600

        required_pH_range = growthRequirements['pH'].split(' - ')
        self.required_min_pH = float(required_pH_range[0])
        self.required_max_pH = float(required_pH_range[1])
        self.new_pH = 0.0

        required_seedTemp_range = growthRequirements['seedTemperature'].split(' - ')
        required_cropTemp_range = growthRequirements['cropTemperature'].split(' - ')
        self.required_seed_minTemp = float(required_seedTemp_range[0])
        self.required_seed_maxTemp = float(required_seedTemp_range[1])
        self.required_crop_minTemp = float(required_cropTemp_range[0])
        self.required_crop_maxTemp = float(required_cropTemp_range[1])
        self.newTemp = 0.0



        # initializing crop variables with average values
        self.soil_temp = round(random.uniform(25.0, 27.0), 2) # celsius
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
        # self.__generateChange(random.uniform,'co2_concentration', -100.0, 100.0, 500.0, 2000.0)



        currentElapsedTime = int(time.time() - self.timeReceiverStartedCollecting)

        ### SOIL MOISTURE & SOIL PH ###
        if self.sprinklerDuration == 0:
            self.sprinklerStatus = 0

        if self.sprinklerStatus == 0:
            # AUTOMATED GROWTH VARIABLE CONTROL
            if self.soil_pH < self.required_min_pH or self.soil_pH > self.required_max_pH:
                # pH regulation
                self.activateSprinkler(10, self.required_min_pH)

                self.socket.send({'sprinkler':10})
            elif currentElapsedTime % self.wateringInterval == 0 and self.soil_moisture < 1.0:
                # watering interval
                self.activateSprinkler(int(self.requiredMoisture / 12.5), self.required_min_pH)

            # NATURAL FLUCTUATIONS
            if currentElapsedTime % 5 == 0:
                self.__generateChange(random.uniform, 'soil_moisture', -0.05, 0.0, 0.0, 100.0)
                self.__generateChange(random.uniform, 'soil_pH', 0.01, 0.05, 0.0, 14.0)
        elif self.sprinklerStatus == 1 and self.sprinklerDuration > 0:
            # MANUAL GROWTH VARIABLE CONTROL
            newMoisture = self.soil_moisture + 12.5

            # moisture
            if newMoisture < 100.0:
                self.soil_moisture = newMoisture
                self.sprinklerDuration -= 1
            else:
                self.sprinklerDuration = 0

            # pH
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
        if self.tempModifierDuration == 0:
            self.tempModifierStatus = 0

        if self.tempModifierStatus == 0:
            # AUTOMATED GROWTH VARIABLE CONTROL
            if self.soil_temp < self.required_crop_minTemp or self.soil_temp > self.required_crop_maxTemp:
                self.activateTemperatureModifier(30, self.required_crop_minTemp + 1.0)

                self.socket.send({'tempModifier':30})

            # NATURAL FLUCTUATIONS
            if currentElapsedTime % 3 == 0:
                self.__generateChange(random.uniform, 'soil_temp', -0.8, 0.8, -100.0, 100.0)
        elif self.tempModifierStatus == 1 and self.tempModifierDuration > 0:
            # MANUAL GROWTH VARIABLE CONTROL
            tempDifference = abs(self.newTemp - self.soil_temp)
            temp_min_change = 1.0
            temp_max_change = tempDifference

            if tempDifference > 50:
                temp_max_change = tempDifference - 25.0
            elif tempDifference > 40:
                temp_max_change = tempDifference - 20.0
            elif tempDifference > 30:
                temp_max_change = tempDifference - 15.0
            elif tempDifference > 20:
                temp_max_change = tempDifference - 10.0
            elif tempDifference > 10:
                temp_max_change = tempDifference - 5.0

            if (tempDifference - 2.0 > 0):
                temp_min_change = tempDifference - 2.0

            newTemp = random.uniform(temp_min_change, temp_max_change)

            if self.newTemp > self.soil_temp and self.soil_temp + newTemp < 100.0:
                self.soil_temp += newTemp
                self.tempModifierDuration -= 1
            elif self.newTemp < self.soil_temp and self.soil_temp - newTemp > -100.0:
                self.soil_temp -= newTemp
                self.tempModifierDuration -= 1
            else:
                self.tempModifierDuration = 0



        ### LIGHTING ###
        elapsedTimeRelativeTo24hrs = currentElapsedTime % 86400

        if self.lightModifierDuration == 0:
            self.lightModifierStatus = 0

        if elapsedTimeRelativeTo24hrs == 0:
            # after 24 hours have passed, turn lighting back on for the specified duration
            duration = int(self.requiredLightExposure)

            self.activateLightModifier(duration);

            self.socket.send({'lightModifier':duration})

        if self.lightModifierStatus == 0:
            # NATURAL FLUCTUATIONS
            if currentElapsedTime % 5 == 0:
                self.light_levels = random.randint(100, 200)
        elif self.lightModifierStatus == 1:
            if elapsedTimeRelativeTo24hrs == 1:
                # turn on lighting modifier on the first second of the day 
                self.socket.send({'lightModifier': self.lightModifierDuration - 1})

            self.lightModifierDuration -= 1

            # NATURAL FLUCTUATIONS
            if currentElapsedTime % 10 == 0:
                self.light_levels = random.randint(9000, 10000)


        self.listen() # repeats collection


    # GETTERS
    def getData(self):
        data = {
            "plotNum" : self.plot_num,
            "soilTemp" : round(self.soil_temp, 2),
            "pH" : round(self.soil_pH, 2),
            "co2" : round(self.co2_concentration, 2),
            "moisture" : round(self.soil_moisture, 2),
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
        self.tempModifierStatus = 1
        self.tempModifierDuration = duration

        self.newTemp = temp

    def activateLightModifier(self, duration:int):
        self.lightModifierStatus = 1
        self.lightModifierDuration = duration
