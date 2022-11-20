from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class CropGrowthRequirements(db.Model):
    __tablename__ = "growthreq"

    plot_num = db.Column(db.Integer, primary_key = True) 
    days_for_growth = db.Column(db.Integer, default = 0)
    seed_min_temp = db.Column(db.Float, default = 0) # celsius
    seed_max_temp = db.Column(db.Float, default = 0) # celsius
    crop_min_temp = db.Column(db.Float, default = 0) # celsius
    crop_max_temp = db.Column(db.Float, default = 0) # celsius
    min_pH = db.Column(db.Float, default = 0)
    max_pH = db.Column(db.Float, default = 0)
    min_co2 = db.Column(db.Integer, default = 0) # ppm
    max_co2 = db.Column(db.Integer, default = 0) # ppm
    light_exp = db.Column(db.Float, default = 0) # hrs
    water_depth = db.Column(db.Float,default = 0) # inches
    watering_interval = db.Column(db.Float,default = 0) # hrs

    def create(self):
        db.session.add(self)
        db.session.commit()

        return self

    def __init__(self, plot_num, days_for_growth, seed_min_temp, seed_max_temp, crop_min_temp, crop_max_temp,min_pH, max_pH, min_co2, max_co2, light_exp, water_depth, watering_interval):
        self.plot_num = plot_num
        self.days_for_growth = days_for_growth
        self.seed_min_temp = seed_min_temp
        self.seed_max_temp = seed_max_temp
        self.crop_min_temp = crop_min_temp
        self.crop_max_temp = crop_max_temp
        self.min_pH = min_pH
        self.max_pH = max_pH
        self.min_co2 = min_co2
        self.max_co2 = max_co2
        self.light_exp = light_exp
        self.water_depth = water_depth
        self.watering_interval = watering_interval

    def __repr__(self):
        return f"{self.plot_num}"
