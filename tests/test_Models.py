import sys
sys.path.append('../')

import flask_unittest

from Models import CropGrowthRequirements, db
from flask import Flask

class TestModels(flask_unittest.AppClientTestCase):
    def create_app(self):
        app = Flask(__name__)
        app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///database.db"
        db.init_app(app)

        with app.app_context():
            db.create_all()

        return app

    def setUp(self, app, client):
        self.sample1 = CropGrowthRequirements(
            plot_num=0,
            days_for_growth=12,
            seed_min_temp=20,
            seed_max_temp=50,
            crop_min_temp=30,
            crop_max_temp=50,
            min_pH=6,
            max_pH=7,
            min_co2=600,
            max_co2=1000,
            light_exp=100,
            water_depth=1,
            watering_interval=6
        )

        with app.app_context():
            db.session.add(self.sample1)
            db.session.commit()

    def tearDown(self, app, client):
        with app.app_context():
            CropGrowthRequirements.query.delete() # deletes all rows
            db.session.commit()

    def test_selectAll(self, app, client):
        pass

    def test_insert(self, app, client):
        pass

    def test_delete(self, app, client):
        pass