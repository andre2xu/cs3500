import unittest
from Models import CropGrowthRequirements

class TestModels(unittest.TestCase):

    def setUp(self):
        plot_num=12
        harvest_date = 2022-11-22
        days_for_growth = 12
        seed_min_temp = 20
        seed_max_temp = 50
        crop_min_temp = 30
        crop_max_temp = 50
        min_pH = 6
        max_pH = 7
        min_co2 = 600
        max_co2 = 1000
        light_exp = 100
        water_depth = 1
        watering_interval = 6
        self.crop = CropGrowthRequirements(plot_num, harvest_date, days_for_growth, seed_min_temp, seed_max_temp, crop_min_temp, crop_max_temp, min_pH, max_pH, min_co2, max_co2, light_exp, water_depth, watering_interval)

    def test_plotNum_negative(self):
        plot_num = -1
        self.crop.plot_num = -1
        self.assertAlmostEqual(self.crop.plot_num, -1)