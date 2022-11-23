import unittest
from PlotSensorDataReceiver import PlotSensorDataReceiver

class TestPlotSensorDataReceiver(unittest.TestCase):
    def test_plotNum(self):
        self.assertRaises(ValueError, PlotSensorDataReceiver, "String") # String
        self.assertRaises(ValueError, PlotSensorDataReceiver, -1) # Neg Int
        self.assertRaises(ValueError, PlotSensorDataReceiver, True) # Boolean