import os

from flask import Flask, jsonify, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from models import db, LogInformation

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = '/app/uploads'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////app/database/app.db'

db.init_app(app)

with app.app_context():
    db.create_all()
    
@app.route('/')
def index():
    return redirect(url_for('get_log_information'))

@app.route('/log_information', methods=['POST'])
def add_log_information():
    return
    
@app.route('/log_information', methods=['GET'])
def get_log_information():
    all_logs = LogInformation.query.all()
    logs_list = []
    
    for log in all_logs:
        logs_list.append({
            'photo_id': log.photo_id,
            'building_name': log.building_name,
            'latitude': log.latitude,
            'longitude': log.longitude,
            'building_side': log.building_side,
            'time': log.time.isoformat() if log.time else None,
            'observed_temp': float(log.observed_temp) if log.observed_temp is not None else None,
            'min_temp': float(log.min_temp) if log.min_temp is not None else None,
            'max_temp': float(log.max_temp) if log.max_temp is not None else None,
            'frame': log.frame,
            'distance': float(log.distance) if log.distance is not None else None,
            'outdoor_temp': float(log.outdoor_temp) if log.outdoor_temp is not None else None,
            'sun_direction': log.sun_direction,
            'position': log.position,
            'floor': log.floor,
        })

    return jsonify(logs_list)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)