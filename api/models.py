from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class LogInformation(db.Model):
    __tablename__ = 'log_information'

    photo_id = db.Column(db.String(6), primary_key=True)
    building_name = db.Column(db.String(12))
    latitude = db.Column(db.Text)
    longitude = db.Column(db.Text)
    building_side = db.Column(db.String(5))
    time = db.Column(db.DateTime)
    observed_temp = db.Column(db.Numeric)
    min_temp = db.Column(db.Numeric)
    max_temp = db.Column(db.Numeric)
    frame = db.Column(db.String(12))
    distance = db.Column(db.Numeric)
    outdoor_temp = db.Column(db.Numeric)
    sun_direction = db.Column(db.String(12))
    position = db.Column(db.String(8))
    floor = db.Column(db.Text)
    notes = db.Column(db.Text)

    def __repr__(self):
        return f'<LogInformation {self.photo_id}>'