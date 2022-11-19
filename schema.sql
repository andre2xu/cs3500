DROP TABLE IF EXISTS cropdata;

CREATE TABLE cropdata (
    plot_num INTEGER PRIMARY KEY,
    days_for_growth INTEGER DEFAULT 0,
    crop_temp FLOAT DEFAULT 0,
    co2_level FLOAT DEFAULT 0,
    seed_temp FLOAT DEFAULT 0,
    light_exp FLOAT DEFAULT 0,
    water_depth FLOAT DEFAULT 0,
    water_interval FLOAT DEFAULT 0

);
