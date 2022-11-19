import os
from flask import Flask, render_template
from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemySchema

STATIC_FOLDER = os.path.dirname(__file__) + '/static/'

app = Flask(
    import_name=__name__,
    template_folder=STATIC_FOLDER + 'html',
    static_folder=STATIC_FOLDER
)


@app.route('/')
def index():
    return render_template('index.html')

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost:3306/cropdata'

db = SQLAlchemy(app)

class CropData(db.Model):
    __tablename__ = "cropData"
    patch_id = db.Column(db.Integer, primary_key = True)
    days_for_growth = db.Column(db.Integer)
    crop_temp = db.Column(db.Float)
    co2_level = db.Column(db.Float)
    seed_temp = db.Column(db.Float)
    light_exp = db.Column(db.Float)
    water_depth = db.Column(db.Float)
    water_interval = db.Column(db.Float)

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self
    def __init__(self, title, description):
        self.title = title
        self.description = description

    def __repr__(self):
        return f"{self.id}"

with app.app_context():
    db.create_all()

class DBSchema(SQLAlchemySchema):
    class Meta(SQLAlchemySchema.Meta):
        model = CropData
        sqla_session = db.session
    patch_id = fields.Number(dump_only=True)
    days_for_growth = fields.Float(required=True)
    seed_temp = fields.Float(required=True)
    crop_temp = fields.Float(required=True)
    co2_level = fields.Float(required=True)
    light_exp = fields.Float(required=True)
    water_depth = fields.Float(required=True)
    water_interval = fields.Float(required=True)

    # patch_id = db.Column(db.Integer, primary_key=True)
    # soil_temp = db.Column(db.Float, unique=False, nullable=False)
    # air_temp = db.Column(db.Float, unique=False, nullable=False)
    # soil_PH = db.Column(db.Integer, unique=False, nullable=False)
    # soil_temp = db.Column(db.Long, unique=False, nullable=False)
    # soil_moisture = db.Column(db.Double, unique=False, nullable=False)
    # light_level = db.Column(db.Integer, unique=False, nullable=False)
#from form to validation to DB
#delete from PK
#pass context
#check for plant id and update
#create routing functions
#get from db


@app.route("/api/v1/cropdata", methods=["POST"])
def create_cropdata():
    data = request.get_json()
    cropdata_schema = DBSchema()
    cropdata = cropdata_schema.load(data)
    result = cropdata_schema.dump(cropdata.create())
    return make_response(jsonify({"todo": result}), 200)
@app.route('/api/v1/cropdata', methods=['GET'])
def db_index():
   get_cropdatas = CropData.query.all()
   cropdata_schema = DBSchema(many=True)
   cropdatas = cropdata_schema.dump(get_cropdatas)
   return make_response(jsonify({"cropdatas": cropdatas}))
@app.route('/api/v1/cropdata/<id>', methods=['GET'])
def get_cropdata_by_id(id):
   get_cropdata = CropData.query.get(id)
   cropdata_schema = DBSchema()
   cropdata = cropdata_schema.dump(get_cropdata)
   return make_response(jsonify({"cropdata": cropdata}))

@app.route('/api/v1/cropdata/<id>', methods=['PUT'])
def update_cropdata_by_id(id):
   data = request.get_json()
   get_cropdata = CropData.query.get(id)
   if data.get('days_for_growth'):
       get_cropdata.days_for_growth = data['days_for_growth']
   if data.get('seed_temp'):
       get_cropdata.seed_temp = data['seed_temp']
   if data.get('crop_temp'):
       get_cropdata.crop_temp = data['crop_temp']
   if data.get('co2_level'):
       get_cropdata.co2_level = data['co2_level']
   if data.get('light_exp'):
       get_cropdata.light_exp = data['light_exp']
   if data.get('water_depth'):
       get_cropdata.water_depth = data['water_depth']
   if data.get('water_interval'):
       get_cropdata.water_interval = data['water_interval']

   db.session.add(get_cropdata)
   db.session.commit()
   cropdata_schema = DBSchema(only=["patch_id", "days_for_growth", "seed_temp","crop_temp","co2_level","light_exp","water_depth","water_interval"])
   cropdata = cropdata_schema.dump(get_cropdata)

   return make_response(jsonify({"cropdata": cropdata}))


@app.route('/api/v1/cropdata/<id>', methods=['DELETE'])
def delete_cropdata_by_id(id):
   get_cropdata = CropData.query.get(id)
   db.session.delete(get_cropdata)
   db.session.commit()
   return make_response("", 204)
if __name__ == "__main__":
    app.run(debug=True)
