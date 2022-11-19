from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class CropData(db.Model):
    __tablename__ = "cropdata"

    plot_num = db.Column(db.Integer, primary_key = True)
    days_for_growth = db.Column(db.Integer, default = 0)
    crop_temp = db.Column(db.Float, default = 0)
    co2_level = db.Column(db.Float, default = 0)
    seed_temp = db.Column(db.Float, default = 0)
    light_exp = db.Column(db.Float, default = 0)
    water_depth = db.Column(db.Float,default = 0)
    water_interval = db.Column(db.Float,default = 0)

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self
    def __init__(self, plot_num, days_for_growth,crop_temp,co2_level,seed_temp,light_exp,water_depth,water_interval):
        self.plot_num = plot_num
        self.days_for_growth = days_for_growth
        self.crop_temp = crop_temp
        self.co2_level = co2_level
        self.seed_temp = seed_temp
        self.light_exp = light_exp
        self.water_depth = water_depth
        self.water_interval = water_interval

    def __repr__(self):
        return f"{self.plot_num}"
