import os
import re
import constants
import csv
import io
import time
import zipfile

from flask import Flask, Response, jsonify, make_response, send_from_directory, send_file, request
from flask_cors import CORS
from models import db, LogInformation
from werkzeug.utils import secure_filename
from datetime import datetime

app = Flask(__name__)
CORS(app)

@app.after_request
def after_request(response):
  response.headers.add("Access-Control-Allow-Origin", "*")
  response.headers.add("Access-Control-Allow-Headers", "Content-Type,Authorization")
  response.headers.add("Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS")
  return response


app.config["UPLOAD_FOLDER"] = "/app/uploads"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////app/database/app.db"
app.config["ALLOWED_EXTENSIONS"]= { "png", "jpg", "jpeg" }

db.init_app(app)

with app.app_context():
    db.create_all()
    
def allowed_file(filename : str):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in app.config["ALLOWED_EXTENSIONS"]

def generate_id(building_name : str) -> str:
    abbv = "DH" if building_name == "Dumbach Hall" else "CH"
    recent_log = LogInformation.query.filter(
        LogInformation.photo_id.like(f"{abbv}%")
    ).order_by(LogInformation.photo_id.desc()).limit(1).one()

    pattern = r"[A-Z]"
    new_id = (int)(re.sub(pattern, "", recent_log.photo_id)) + 1
    new_id = f"{abbv}{(str)(new_id)}"
    return new_id

def get_image(photo_id : str) -> str:
    image_path = os.path.join(app.config["UPLOAD_FOLDER"], photo_id)
    for ext in app.config["ALLOWED_EXTENSIONS"]:
        temp_path = f"{image_path}.{ext}"
        if (os.path.exists(temp_path)):
            return f"/uploads/{photo_id}.{ext}"
        
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)

@app.route("/download_csv")
def download_csv():
    logs = LogInformation.query.all()
    
    si = io.StringIO()

    csv_writer = csv.writer(si)

    csv_writer.writerow([
        "Photo ID", "Building Name", "Latitude", "Longitude", "Side of Building", 
        "Date and Time", "Observed Temp", "Min Temp", "Max Temp", "Framed Properly?", 
        "Distance", "Outdoor Temp", "Sun Direction", "Indoor/Outdoor", "Floor"
    ])

    for log in logs:
        dt_obj = datetime.strptime(log.time.isoformat(), '%Y-%m-%dT%H:%M:%S')
        formatted_datetime = dt_obj.strftime('%Y-%m-%d %I:%M:%S %p')
        csv_writer.writerow([
            log.photo_id, log.building_name, log.latitude, log.longitude, log.building_side,
            formatted_datetime, log.observed_temp, log.min_temp, log.max_temp, log.frame,
            log.distance, log.outdoor_temp, log.sun_direction, log.position, log.floor
        ])
    output = make_response(si.getvalue())
    output.headers["Content-Disposition"] = "attachment; filename=log_information.csv"
    output.headers["Content-type"] = "text/csv"
    return output

# @app.route("/download_images")
# def download_images():
#     time_str = time.strftime("%Y%m%d-%H%M%S")
#     filename = "thermal_images.zip".format(time_str)
#     memory_file = io.BytesIO
#     with zipfile.ZipFile(memory_file, "w", zipfile.ZIP_DEFLATED) as zipf:
        
 
        
    
@app.route("/log_information", methods=["POST"])
def add_log_information():
    if "image" not in request.files:
        return jsonify({"error": "Image Not Found"}), 400
    image_file = request.files["image"]
    
    if image_file and allowed_file(image_file.filename):
        filename = secure_filename(image_file.filename)
        
        building_name = request.form["buildingName"]
        new_id = generate_id(building_name)
        file_extension = filename.rsplit(".", 1)[1].lower()
        image_path = os.path.join(app.config["UPLOAD_FOLDER"], f"{new_id}.{file_extension}")
        image_file.save(image_path)
        
        dt_obj = datetime.strptime(request.form["time"], '%Y-%m-%dT%H:%M')
        
        log_info = LogInformation(
            photo_id = new_id,
            building_name = constants.BUILDING_NAME[request.form["buildingName"]],
            latitude = request.form["latitude"],
            longitude = request.form["longitude"],
            building_side = constants.BUILDING_SIDE[request.form["buildingSide"]],
            time = dt_obj,
            observed_temp = request.form["observedTemp"],
            min_temp = request.form["minTemp"],
            max_temp = request.form["maxTemp"],
            frame = constants.FRAME[request.form["frame"]],
            distance = request.form["distance"],
            outdoor_temp = request.form["outdoorTemp"],
            sun_direction = constants.SUN_DIRECTION[request.form["sunDirection"]],
            position = constants.POSITION[request.form["position"]],
            floor = constants.FLOOR[request.form["floor"]],
            notes = request.form["notes"]
        )

        db.session.add(log_info)
        db.session.commit()
        
        return jsonify({"message": "Log information added successfully!"}), 201
    return jsonify({"error": "Invalid file type"}), 400
    
@app.route("/log_information", methods=["GET"])
def get_log_information():
    logs = LogInformation.query.all()
    logs_list = []
    
    for log in logs:
        dt_obj = datetime.strptime(log.time.isoformat(), '%Y-%m-%dT%H:%M:%S')
        formatted_datetime = dt_obj.strftime('%Y-%m-%d %I:%M:%S %p')
        
        logs_list.append({
            "photo_id": log.photo_id,
            "building_name": log.building_name,
            "latitude": log.latitude,
            "longitude": log.longitude,
            "building_side": log.building_side,
            "time": formatted_datetime,
            "observed_temp": float(log.observed_temp) if log.observed_temp is not None else None,
            "min_temp": float(log.min_temp) if log.min_temp is not None else None,
            "max_temp": float(log.max_temp) if log.max_temp is not None else None,
            "frame": log.frame,
            "distance": float(log.distance) if log.distance is not None else None,
            "outdoor_temp": float(log.outdoor_temp) if log.outdoor_temp is not None else None,
            "sun_direction": log.sun_direction,
            "position": log.position,
            "floor": log.floor,
            "image_path": get_image(log.photo_id)
        })
    
    return jsonify(logs_list)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)