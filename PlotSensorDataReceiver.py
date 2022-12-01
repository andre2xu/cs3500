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
        self.co2ModifierStatus = 0
        self.co2ModifierDuration = 0

        self.requiredDaysForSeedGrowth = growthRequirements['daysForSeedGrowth']
        self.requiredDaysForCropGrowth = growthRequirements['daysForCropGrowth']
        self.growthStage = 'seed'
        self.totalSecondsRequiredForSeedGrowth = self.requiredDaysForSeedGrowth * 86400 # total seconds for seed growth

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

        required_co2_range = growthRequirements['co2Concentration'].split(' - ')
        self.required_min_co2 = int(required_co2_range[0])
        self.required_max_co2 = int(required_co2_range[1])
        self.newCO2Concentration = 0



        # initializing crop variables with average values
        self.soil_temp = round(random.uniform(25.0, 27.0), 2) # celsius
        self.soil_pH = round(random.uniform(6.0, 7.0), 2) # pH scale
        self.co2_concentration = random.randint(1000, 1600) # ppm
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
        currentElapsedTime = int(time.time() - self.timeReceiverStartedCollecting)
        systemIsDoingComparison = currentElapsedTime % 30 == 0

        ### SOIL MOISTURE & SOIL PH ###
        if self.sprinklerDuration == 0:
            self.sprinklerStatus = 0

        if self.sprinklerStatus == 0:
            # AUTOMATED GROWTH VARIABLE CONTROL
            if systemIsDoingComparison and self.soil_moisture < 87.5 and (self.soil_pH < self.required_min_pH or self.soil_pH > self.required_max_pH):
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
        if currentElapsedTime - self.totalSecondsRequiredForSeedGrowth == 0:
            self.growthStage = 'crop'

        if self.tempModifierStatus == 0:
            # AUTOMATED GROWTH VARIABLE CONTROL
            if systemIsDoingComparison:
                if self.growthStage == 'seed' and (self.soil_temp < self.required_seed_minTemp or self.soil_temp > self.required_seed_maxTemp):
                    self.activateTemperatureModifier(30, self.required_seed_minTemp + 1.0)

                    self.socket.send({'tempModifier':30})
                elif self.growthStage == 'crop' and (self.soil_temp < self.required_crop_minTemp or self.soil_temp > self.required_crop_maxTemp):
                    self.activateTemperatureModifier(30, self.required_crop_minTemp + 1.0)

                    self.socket.send({'tempModifier':30})

            # NATURAL FLUCTUATIONS
            if currentElapsedTime % 10 == 0:
                self.__generateChange(random.uniform, 'soil_temp', -0.8, 0.8, -100.0, 100.0)
        elif self.tempModifierStatus == 1 and self.tempModifierDuration > 0:
            # MANUAL GROWTH VARIABLE CONTROL
            tempDifference = abs(self.newTemp - self.soil_temp)
            temp_min_change = 0.0
            temp_max_change = 0.0

            if tempDifference > 80.0:
                temp_max_change = 70.0
                temp_min_change = 60.0
            elif tempDifference > 60.0:
                temp_max_change = 50.0
                temp_min_change = 40.0
            elif tempDifference > 40.0:
                temp_max_change = 30.0
                temp_min_change = 20.0
            elif tempDifference > 20.0:
                temp_max_change = 10.0
                temp_min_change = 5.0
            else:
                temp_max_change = 5.0
                temp_min_change = 1.0

            newTemp = random.uniform(temp_min_change, temp_max_change)

            if self.newTemp > self.soil_temp and self.soil_temp + newTemp < 100.0:
                self.soil_temp += newTemp
                self.tempModifierDuration -= 1
            elif self.newTemp < self.soil_temp and self.soil_temp - newTemp > -100.0:
                self.soil_temp -= newTemp
                self.tempModifierDuration -= 1
            else:
                self.tempModifierDuration -= 1



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



        ### CO2 CONCENTRATION ###
        if self.co2ModifierDuration == 0:
            self.co2ModifierStatus = 0

        if self.co2ModifierStatus == 0:
            # AUTOMATED GROWTH VARIABLE CONTROL
            if systemIsDoingComparison and self.co2_concentration < self.required_min_co2 or self.co2_concentration > self.required_max_co2:
                self.activateCO2Modifier(10, self.required_max_co2)

                self.socket.send({'co2Modifier':10})

            # NATURAL FLUCTUATIONS
            if currentElapsedTime % 10 == 0:
                self.__generateChange(random.randint,'co2_concentration', -50, 50, 800, 2000)
        elif self.co2ModifierStatus == 1 and self.co2ModifierDuration > 0:
            # MANUAL GROWTH VARIABLE CONTROL
            co2Difference = abs(self.newCO2Concentration - self.co2_concentration)
            co2_min_change = 1
            co2_max_change = 2000

            if co2Difference > 1000:
                co2_max_change = 900
                co2_min_change = 800
            elif co2Difference > 800:
                co2_max_change = 700
                co2_min_change = 600
            elif co2Difference > 600:
                co2_max_change = 500
                co2_min_change = 400
            elif co2Difference > 400:
                co2_max_change = 300
                co2_min_change = 200
            elif co2Difference > 200:
                co2_max_change = 100
                co2_min_change = 80
            elif co2Difference > 50:
                co2_max_change = 40
                co2_min_change = 30
            elif co2Difference > 25:
                co2_max_change = 20
                co2_min_change = 10
            else:
                co2_max_change = 10
                co2_min_change = 1

            newCO2 = random.randint(co2_min_change, co2_max_change)

            if self.newCO2Concentration > self.co2_concentration and self.co2_concentration + newCO2 < 2000:
                self.co2_concentration += newCO2
                self.co2ModifierDuration -= 1
            elif self.newCO2Concentration < self.co2_concentration and self.co2_concentration - newCO2 > 0:
                self.co2_concentration -= newCO2
                self.co2ModifierDuration -= 1
            else:
                self.co2ModifierDuration = 0



        self.listen() # repeats collection


    # GETTERS
    def getData(self):
        data = {
            "plotNum" : self.plot_num,
            "soilTemp" : round(self.soil_temp, 2),
            "pH" : round(self.soil_pH, 2),
            "co2" : self.co2_concentration,
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

    def updateGrowthRequirements(self, newGrowthRequirements:dict):
        self.requiredDaysForSeedGrowth = newGrowthRequirements['daysForSeedGrowth']
        self.requiredDaysForCropGrowth = newGrowthRequirements['daysForCropGrowth']
        self.totalSecondsRequiredForSeedGrowth = newGrowthRequirements['daysForSeedGrowth'] * 86400

        self.requiredMoisture = (float(newGrowthRequirements['waterDepth']) / 8.0) * 100
        self.wateringInterval = int(newGrowthRequirements['wateringInterval'] * 3600)

        self.requiredLightExposure = newGrowthRequirements['lightExposureDuration'] * 3600

        required_pH_range = newGrowthRequirements['pH'].split(' - ')
        self.required_min_pH = float(required_pH_range[0])
        self.required_max_pH = float(required_pH_range[1])
        self.new_pH = 0.0

        required_seedTemp_range = newGrowthRequirements['seedTemperature'].split(' - ')
        required_cropTemp_range = newGrowthRequirements['cropTemperature'].split(' - ')
        self.required_seed_minTemp = float(required_seedTemp_range[0])
        self.required_seed_maxTemp = float(required_seedTemp_range[1])
        self.required_crop_minTemp = float(required_cropTemp_range[0])
        self.required_crop_maxTemp = float(required_cropTemp_range[1])

        required_co2_range = newGrowthRequirements['co2Concentration'].split(' - ')
        self.required_min_co2 = int(required_co2_range[0])
        self.required_max_co2 = int(required_co2_range[1])

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

    def activateCO2Modifier(self, duration:int, ppm):
        self.co2ModifierStatus = 1
        self.co2ModifierDuration = duration

        self.newCO2Concentration = ppm
