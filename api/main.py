import os
import re
import constants

from flask import Flask, jsonify, redirect, url_for, request
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
        LogInformation.photo_id.like(abbv+"%")
    ).order_by(LogInformation.photo_id.desc()).limit(1).one()

    pattern = r"[A-Z]"
    new_id = (int)(re.sub(pattern, "", recent_log.photo_id)) + 1
    new_id = abbv + (str)(new_id)
    return new_id
    
@app.route("/log_information", methods=["POST"])
def add_log_information():
    # print(request)
    if "image" not in request.files:
        return jsonify({"error": "Image Not Found"}), 400
    image_file = request.files["image"]
    
    if image_file and allowed_file(image_file.filename):
        filename = secure_filename(image_file.filename)
        
        building_name = request.form["buildingName"]
        new_id = generate_id(building_name)
        file_extension = filename.rsplit(".", 1)[1].lower()
        image_path = os.path.join(app.config["UPLOAD_FOLDER"], new_id + "." + file_extension)
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
    
@app.route("/")
def index():
    return redirect(url_for("get_glog_information"))

# @app.route("/log_information", methods=["POST"])
# def add_log_information():
#     return
    
@app.route("/glog_information", methods=["GET"])
def g():
    # all_logs = LogInformation.query.all()
    # logs_list = []
    
    # for log in all_logs:
    #     logs_list.append({
    #         "photo_id": log.photo_id,
    #         "building_name": log.building_name,
    #         "latitude": log.latitude,
    #         "longitude": log.longitude,
    #         "building_side": log.building_side,
    #         "time": log.time.isoformat() if log.time else None,
    #         "observed_temp": float(log.observed_temp) if log.observed_temp is not None else None,
    #         "min_temp": float(log.min_temp) if log.min_temp is not None else None,
    #         "max_temp": float(log.max_temp) if log.max_temp is not None else None,
    #         "frame": log.frame,
    #         "distance": float(log.distance) if log.distance is not None else None,
    #         "outdoor_temp": float(log.outdoor_temp) if log.outdoor_temp is not None else None,
    #         "sun_direction": log.sun_direction,
    #         "position": log.position,
    #         "floor": log.floor,
    #     })


    return "HELLO"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)