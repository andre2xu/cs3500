import sys
sys.path.append('../')

import flask_unittest

from flask import Flask

class TestPlotSensorDataReceiver(flask_unittest.AppClientTestCase):
    def create_app(self):
        return Flask(__name__)