# navigate to tests folder and use the following command to run tests: python -m unittest test_XYZ.py

import sys, sqlalchemy.exc, flask_unittest

sys.path.append('../')

from Models import CropGrowthRequirements, db
from flask import Flask
from sqlalchemy import select

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
            days_for_crop_growth=10,
            days_for_seed_growth=40,
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
            CropGrowthRequirements.query.delete() # Deletes all rows
            db.session.commit()

    def test_selectAll(self, app, client):
        with app.app_context():
            crops = db.session.execute(select(['*']).where(CropGrowthRequirements.plot_num >= 1)).fetchall()
            for crop in crops:
                self.assertAlmostEquals(crop[1], 1)
                self.assertGreaterEqual(crop[1], 0)
                self.assertAlmostEquals(crop[2], 10)
                self.assertGreaterEqual(crop[2], -30)
                self.assertLessEqual(crop[2], 200)
                self.assertAlmostEquals(crop[3], 60)
                self.assertGreaterEqual(crop[3], -30)
                self.assertLessEqual(crop[3], 200)
                self.assertAlmostEquals(crop[4], 10)
                self.assertGreaterEqual(crop[4], -30)
                self.assertLessEqual(crop[4], 200)
                self.assertAlmostEquals(crop[5], 60)
                self.assertGreaterEqual(crop[5], -30)
                self.assertLessEqual(crop[5], 200)
                self.assertAlmostEquals(crop[6], 7)
                self.assertGreaterEqual(crop[6], 0)
                self.assertLessEqual(crop[6], 14)
                self.assertAlmostEquals(crop[7], 7)
                self.assertGreaterEqual(crop[7], 0)
                self.assertLessEqual(crop[7], 14)
                self.assertAlmostEquals(crop[8], 900)
                self.assertGreaterEqual(crop[8], 600)
                self.assertLessEqual(crop[8], 1500)
                self.assertAlmostEquals(crop[9], 900)
                self.assertGreaterEqual(crop[9], 600)
                self.assertLessEqual(crop[9], 1500)
                self.assertAlmostEquals(crop[10], 50)
                self.assertGreaterEqual(crop[10], 0)
                self.assertLessEqual(crop[10], 100)
                self.assertAlmostEquals(crop[11], 2)
                self.assertGreaterEqual(crop[11], 0)
                self.assertLessEqual(crop[11], 6)
                self.assertAlmostEquals(crop[12], 6)
                self.assertGreaterEqual(crop[12, 0.5])
                self.assertLessEqual(crop[12], 48)

    def test_insert(self, app, client):
        with app.app_context():
            data = {
                'plot_num': 1,
                'harvest_date': 0,
                'days_for_crop_growth': 12,
                'days_for_seed_growth' : 10,
                'seed_min_temp': 10,
                'seed_max_temp': 60,
                'crop_min_temp': 10,
                'crop_max_temp': 70,
                'min_pH': 6,
                'max_pH': 9,
                'min_co2': 800,
                'max_co2': 1000,
                'light_exp': 100,
                'water_depth': 1,
                'watering_interval': 12
            }
            db.session.add(CropGrowthRequirements(data['plot_num'], data['days_for_crop_growth'],data['days_for_seed_growth'], data['seed_min_temp'], data['seed_max_temp'], data['crop_min_temp'], data['crop_max_temp'], data['min_pH'], data['max_pH'], data['min_co2'], data['max_co2'], data['light_exp'], data['water_depth'], data['watering_interval']))
            db.session.commit()
            check = db.session.execute(select(['*']).where(CropGrowthRequirements.plot_num == data['plot_num'])).fetchall()
            data_list = list(data.values())
            for i in range(15):
                if i != 1: #TODO: test harvest_date
                    self.assertAlmostEqual(check[0][i], data_list[i]) # Iterate through the database checking if the data was inserted correctly.

    def test_delete(self, app, client):
        with app.app_context():
            CropGrowthRequirements.query.filter_by(plot_num=1).delete()
            db.session.commit()
            with self.assertRaises(sqlalchemy.exc.OperationalError): #tests if sqlalchemy raises exception, meaning table does not exist anymore
                db.session.execute(select(['*'])).fetchall()



if __name__ == '__main__':
    flask_unittest.main()