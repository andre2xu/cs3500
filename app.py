import os, mimetypes
from flask import Flask, request,render_template,redirect,url_for
from Models import db,CropData
from init_db import create_db


STATIC_FOLDER = os.path.dirname(__file__) + '/static/'

mimetypes.add_type('application/javascript', '.js')
create_db()
db_path = os.path.abspath("database.db")
app = Flask(
    import_name=__name__,
    template_folder=STATIC_FOLDER + 'html',
    static_folder=STATIC_FOLDER
)



@app.route('/')
def index():
    return render_template('index.html')



app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{db_path}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db.init_app(app)
with app.app_context():
    db.create_all()


@app.route("/api/addCrop/<id>", methods=["GET","POST"])
def addCrop(id):
    plot = CropData.query.filter_by(plot_num = id).first()
    if plot:
        db.session.delete(plot)
        db.session.commit()
        days_for_growth = request.form["days_for_growth"]
        seed_temp = request.form["seed_temp"]
        crop_temp = request.form["crop_temp"]
        co2_level = request.form["co2_level"]
        light_exp = request.form["light_exp"]
        water_depth = request.form["water_depth"]
        water_interval = request.form["water_interval"]
        plot = CropData(plot_num=id,seed_temp=seed_temp,days_for_growth=days_for_growth,crop_temp=crop_temp,co2_level=co2_level,light_exp=light_exp,water_depth=water_depth,water_interval=water_interval)
        db.session.add(plot)
        db.session.commit()
        return redirect(url_for('index'))
    else:
        return f"Plot number {id} does not exist"
@app.route('/api/deleteCrop/<plotNum>', methods=['GET'])
def deleteCrop(plotNum):
    plot = CropData.query.filter_by(plot_num=plotNum).first()
    if plot:
        db.session.delete(plot)
        db.session.commit()
        return redirect(url_for("index"))
    else:
        return f"Plot number <plotNum> does not exist"

if __name__ == "__main__":
    app.run(debug=True)