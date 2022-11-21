import os, mimetypes
from flask import Flask, request, render_template
from Models import db, CropGrowthRequirements
from sqlalchemy import select, update
from PlotSensorDataReceiver import PlotSensorDataReceiver


mimetypes.add_type('application/javascript', '.js')
STATIC_FOLDER = os.path.dirname(__file__) + '/static/'
db_path = os.path.abspath("database.db")



app = Flask(
    import_name=__name__,
    template_folder=STATIC_FOLDER + 'html',
    static_folder=STATIC_FOLDER
)
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{db_path}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True



db.init_app(app)
with app.app_context():
    db.create_all()

def validateGrowthRequirements(plotNum, harvestCountdown, seedMinTemp, seedMaxTemp, cropMinTemp, cropMaxTemp, minpH, maxpH, minCO2, maxCO2, lightExposureDuration, waterDepth, wateringInterval):
    isValidData = True

    # validate all here (make sure to put them back into the same variables). If ONE of the parameters has an incorrect value, change isValidData to False. NOTE: I already changed them into integers and floats.



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



SENSOR_DATA_GENERATORS = []

@app.route('/')
def index():
    activePlots = getActivePlots()
    num_of_plots = len(activePlots)

    if num_of_plots > 0:
        for i in range(num_of_plots):
            sensorDataGenerator = PlotSensorDataReceiver(int(activePlots[i]))
            sensorDataGenerator.listen()

            SENSOR_DATA_GENERATORS.append(sensorDataGenerator)

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
            'days': growthRequirements[1],
            'seedTemperature': f'{growthRequirements[2]} - {growthRequirements[3]}',
            'cropTemperature': f'{growthRequirements[4]} - {growthRequirements[5]}',
            'pH': f'{growthRequirements[6]} - {growthRequirements[7]}',
            'co2Concentration': f'{growthRequirements[8]} - {growthRequirements[9]}',
            'lightExposureDuration': growthRequirements[10],
            'waterDepth': growthRequirements[11],
            'wateringInterval': growthRequirements[12]
        }

    return response

@app.route("/api/sensorData/<plotNum>", methods=["GET"])
def getSensorData(plotNum):
    plotNum = int(plotNum)

    if plotNum >= 0 and plotNum <= len(SENSOR_DATA_GENERATORS) - 1:
        return SENSOR_DATA_GENERATORS[plotNum].getData()

    return ''

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

    return ''



if __name__ == "__main__":
    app.run(debug=True)