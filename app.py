import os, mimetypes
from flask import Flask, request, render_template,redirect,url_for
from Models import db, CropData



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



@app.route('/')
def index():
    return render_template('index.html')

@app.route("/api/addCrop", methods=["POST"])
def addCrop():
    plotNum = request.form['addPlotNum']
    harvestCountdown = request.form['addHarvestCountdown']
    seedMinTemp = request.form['addSeedTemperatureV1']
    seedMaxTemp = request.form['addSeedTemperatureV2']
    cropMinTemp = request.form['addCropTemperatureV1']
    cropMaxTemp = request.form['addCropTemperatureV2']
    minpH = request.form['addpHV1']
    maxpH = request.form['addpHV2']
    minCO2 = request.form['addCO2V1']
    maxCO2 = request.form['addCO2V2']
    lightExposureDuration = request.form['addLightDuration']
    waterDepth = request.form['addWaterDepth']
    wateringInterval = request.form['addWateringInterval']

    plotData = CropData.query.filter_by(plot_num=plotNum).first()

    if (plotData == None):
        pass # add plot data to database

    return redirect(url_for('index'))

@app.route('/api/deleteCrop/<plotNum>', methods=['GET'])
def deleteCrop(plotNum):
    plot = CropData.query.filter_by(plot_num=plotNum).first()

    if plot:
        db.session.delete(plot)
        db.session.commit()
    else:
        print(f"Plot number {plotNum} does not exist")

    return redirect(url_for("index"))



if __name__ == "__main__":
    app.run(debug=True)