import os, mimetypes
from flask import Flask, request, render_template
from Models import db, CropGrowthRequirements
from sqlalchemy import select, update
from PlotSensorDataReceiver import PlotSensorDataReceiver
from flask_socketio import SocketIO


mimetypes.add_type('application/javascript', '.js')
STATIC_FOLDER = os.path.dirname(__file__) + '/static/'
db_path = os.path.abspath("database.db")



app = Flask(
    import_name=__name__,
    template_folder=STATIC_FOLDER + 'html',
    static_folder=STATIC_FOLDER
)
app.config['SECRET_KEY'] = 'secret'
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{db_path}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

socket = SocketIO(app)



db.init_app(app)
with app.app_context():
    db.create_all()

def validateGrowthRequirements(plotNum, harvestCountdown, seedMinTemp, seedMaxTemp, cropMinTemp, cropMaxTemp, minpH, maxpH, minCO2, maxCO2, lightExposureDuration, waterDepth, wateringInterval):
    isValidData = True

    if plotNum < 0 or plotNum > 10: 
        isValidData = False
    if  harvestCountdown < 1:
        isValidData = False
    if seedMinTemp < -100 or seedMaxTemp > 100 or seedMinTemp > seedMaxTemp:
        isValidData = False
    if cropMinTemp < -100 or cropMaxTemp > 100 or cropMinTemp > cropMaxTemp:
        isValidData = False 
    if minpH < 0 or maxpH > 14 or minpH > maxpH:
        isValidData = False
    if minCO2 < 1 or maxCO2 > 1500 or minCO2 > maxCO2:
        isValidData = False
    if lightExposureDuration < 1:
        isValidData = False
    if waterDepth < 1:
        isValidData = False
    if wateringInterval < 1:
        isValidData = False

    if isValidData:
        return {
            'plot_num':plotNum,
            'days_for_growth':harvestCountdown,
            'seed_min_temp':seedMinTemp,
            'seed_max_temp':seedMaxTemp,
            'crop_min_temp':cropMinTemp,
            'crop_max_temp':cropMaxTemp,
            'min_pH':minpH,
            'max_pH':maxpH,
            'min_co2':minCO2,
            'max_co2':maxCO2,
            'light_exp':lightExposureDuration,
            'water_depth':waterDepth,
            'watering_interval':wateringInterval
        }
    else:
        return None



SENSOR_DATA_GENERATORS = {}

@app.route('/')
def index():
    activePlots = getActivePlots()
    num_of_plots = len(activePlots)

    if num_of_plots > 0 and len(SENSOR_DATA_GENERATORS) == 0:
        for i in range(num_of_plots):
            plotNum = activePlots[i]

            sensorDataGenerator = PlotSensorDataReceiver(plotNum, getGrowthRequirements(plotNum), socket)
            sensorDataGenerator.startListening()
            sensorDataGenerator.listen()

            SENSOR_DATA_GENERATORS[plotNum] = sensorDataGenerator

    return render_template('index.html')

@app.route("/db/activePlots", methods=["GET"])
def getActivePlots():
    activePlots = '';

    # SELECT plot_num FROM growthreq
    queryResult = db.session.execute(select(CropGrowthRequirements.plot_num))
    plotsArray = queryResult.fetchall()
    num_of_active_plots = len(plotsArray)

    if (num_of_active_plots > 0):
        for i in range(num_of_active_plots):
            activePlots += str(plotsArray[i][0]);

    return activePlots

@app.route("/db/growthRequirements/<plotNum>", methods=["GET"])
def getGrowthRequirements(plotNum):
    queryResult = db.session.execute(select(['*']).where(CropGrowthRequirements.plot_num == plotNum))
    growthRequirements = queryResult.fetchone()

    response = ''

    if growthRequirements != None:
        response = {
            'harvestDate': growthRequirements[1],
            'days': growthRequirements[2],
            'seedTemperature': f'{growthRequirements[3]} - {growthRequirements[4]}',
            'cropTemperature': f'{growthRequirements[5]} - {growthRequirements[6]}',
            'pH': f'{growthRequirements[7]} - {growthRequirements[8]}',
            'co2Concentration': f'{growthRequirements[9]} - {growthRequirements[10]}',
            'lightExposureDuration': growthRequirements[11],
            'waterDepth': growthRequirements[12],
            'wateringInterval': growthRequirements[13]
        }

    return response

@app.route("/api/sensorData/<plotNum>", methods=["GET"])
def getSensorData(plotNum):
    if plotNum in SENSOR_DATA_GENERATORS:
        return SENSOR_DATA_GENERATORS[plotNum].getData()

    return ''

@app.route("/api/switchHandler", methods=["POST"])
def handleSwitch():
    switchData = request.get_json()

    componentsToTurnOn = ''
    plotNum = switchData['plotNum']

    if plotNum in SENSOR_DATA_GENERATORS:
        component = switchData['component']
        receiverInstance = SENSOR_DATA_GENERATORS[plotNum]
        duration = int(switchData['activationDuration'])

        if component == 'sprinkler':
            receiverInstance.activateSprinkler(duration, float(switchData['pH']))
            componentsToTurnOn += 's'
        elif component == 'temperatureModifier':
            receiverInstance.activateTemperatureModifier(duration, float(switchData['temperature']))
            componentsToTurnOn += 't'
        elif component == 'lightingModifier':
            receiverInstance.activateLightModifier(duration)
            componentsToTurnOn += 'l'
        elif component == 'co2Modifier':
            receiverInstance.activateCO2Modifier(duration, int(switchData['ppm']))
            componentsToTurnOn += 'c'

    return componentsToTurnOn

@app.route("/api/addCrop", methods=["POST"])
def addCrop():
    response = ''

    plotNum = request.form['plotNum']
    harvestCountdown = request.form['harvestCountdown']
    seedMinTemp = request.form['seedTemperatureV1']
    seedMaxTemp = request.form['seedTemperatureV2']
    cropMinTemp = request.form['cropTemperatureV1']
    cropMaxTemp = request.form['cropTemperatureV2']
    minpH = request.form['pHV1']
    maxpH = request.form['pHV2']
    minCO2 = request.form['CO2V1']
    maxCO2 = request.form['CO2V2']
    lightExposureDuration = request.form['lightDuration']
    waterDepth = request.form['waterDepth']
    wateringInterval = request.form['wateringInterval']

    # SELECT plot_num FROM growthreq WHERE plot_num = x
    queryResult = db.session.execute(select(CropGrowthRequirements.plot_num).where(CropGrowthRequirements.plot_num == plotNum))

    if (queryResult.fetchone() == None):
        validatedData = validateGrowthRequirements(int(plotNum), int(harvestCountdown), float(seedMinTemp), float(seedMaxTemp), float(cropMinTemp), float(cropMaxTemp), float(minpH), float(maxpH), int(minCO2), int(maxCO2), float(lightExposureDuration), float(waterDepth), float(wateringInterval))

        if type(validatedData) is dict: 
            newGrowthRequirements = CropGrowthRequirements(**validatedData)

            db.session.add(newGrowthRequirements)
            db.session.commit()

            response = plotNum

            # activates sensors for plot
            sensorDataGenerator = PlotSensorDataReceiver(plotNum, newGrowthRequirements, socket)
            sensorDataGenerator.startListening()
            sensorDataGenerator.listen()
            SENSOR_DATA_GENERATORS[plotNum] = sensorDataGenerator

    return response

@app.route("/api/editCrop", methods=["POST"])
def editCrop():
    plotNum = request.form['plotNum']
    harvestCountdown = request.form['harvestCountdown']
    seedMinTemp = request.form['seedTemperatureV1']
    seedMaxTemp = request.form['seedTemperatureV2']
    cropMinTemp = request.form['cropTemperatureV1']
    cropMaxTemp = request.form['cropTemperatureV2']
    minpH = request.form['pHV1']
    maxpH = request.form['pHV2']
    minCO2 = request.form['CO2V1']
    maxCO2 = request.form['CO2V2']
    lightExposureDuration = request.form['lightDuration']
    waterDepth = request.form['waterDepth']
    wateringInterval = request.form['wateringInterval']

    # SELECT plot_num FROM growthreq WHERE plot_num = x
    queryResult = db.session.execute(select(CropGrowthRequirements.plot_num).where(CropGrowthRequirements.plot_num == plotNum))

    if (queryResult.fetchone() != None):
        validatedData = validateGrowthRequirements(int(plotNum), int(harvestCountdown), float(seedMinTemp), float(seedMaxTemp), float(cropMinTemp), float(cropMaxTemp), float(minpH), float(maxpH), int(minCO2), int(maxCO2), float(lightExposureDuration), float(waterDepth), float(wateringInterval))

        if type(validatedData) is dict:
            updateQuery = update(CropGrowthRequirements).where(CropGrowthRequirements.plot_num == plotNum).values(**validatedData)

            db.session.execute(updateQuery)
            db.session.commit()

    return ''

@app.route('/api/deleteCrop/<plotNum>', methods=['GET'])
def deleteCrop(plotNum):
    CropGrowthRequirements.query.filter_by(plot_num=plotNum).delete()
    db.session.commit()

    SENSOR_DATA_GENERATORS[plotNum].stopListening()

    if plotNum in SENSOR_DATA_GENERATORS:
        del SENSOR_DATA_GENERATORS[plotNum]

    return ''



if __name__ == "__main__":
    socket.run(app, debug=True)