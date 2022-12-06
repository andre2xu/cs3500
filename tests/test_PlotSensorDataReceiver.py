import flask_unittest, sys

sys.path.append('../')

from flask import Flask
from PlotSensorDataReceiver import PlotSensorDataReceiver
from flask_socketio import SocketIO

class TestPlotSensorDataReceiver(flask_unittest.AppClientTestCase):
    def create_app(self):
        app = Flask(__name__)
        return app

    def setUp(self, app, client):
        with app.app_context():
            self.socket = SocketIO(app)

        self.growthRequirements = {
            'harvestDate': '2022-12-01',
            'daysForSeedGrowth': 1,
            'daysForCropGrowth': 1,
            'seedTemperature': f'25.0 - 28.0',
            'cropTemperature': f'25.0 - 28.0',
            'pH': f'6 - 8',
            'co2Concentration': f'500 - 800',
            'lightExposureDuration': 1.0,
            'waterDepth': 1.0,
            'wateringInterval': 1.0
        }

        self.receiver = PlotSensorDataReceiver(0, self.growthRequirements, self.socket)

    def tearDown(self, app, client):
        del self.receiver

    def test_sensorData(self, app, client):
        data = self.receiver.getData()

        self.assertEqual(type(data), dict)
        self.assertEqual(['plotNum', 'soilTemp', 'pH', 'co2', 'moisture', 'lighting'], list(data.keys()))



if __name__ == '__main__':
    flask_unittest.main()