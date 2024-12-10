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
from werkzeug.exceptions import BadRequest
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
    abbv = ''.join([s[0] for s in building_name.split()]).upper()
    logs = LogInformation.query.filter(
        LogInformation.photo_id.like(f"{abbv}%")
    ).order_by(LogInformation.photo_id.desc()).limit(1).all()
    
    id = logs[0].photo_id if logs else 1
    pattern = r"[A-Z]"
    if id != 1:
        id = (int)(re.sub(pattern, "", id)) + 1
    new_id = f"{abbv}{(str)(id)}"
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
        "Distance", "Outdoor Temp", "Sun Direction", "Indoor/Outdoor", "Floor", "Notes"
    ])

    for log in logs:
        dt_obj = datetime.strptime(log.time.isoformat(), '%Y-%m-%dT%H:%M:%S')
        formatted_datetime = dt_obj.strftime('%Y-%m-%d %I:%M:%S %p')
        csv_writer.writerow([
            log.photo_id, log.building_name, log.latitude, log.longitude, log.building_side,
            formatted_datetime, log.observed_temp, log.min_temp, log.max_temp, log.frame,
            log.distance, log.outdoor_temp, log.sun_direction, log.position, log.floor, log.notes
        ])
    output = make_response(si.getvalue())
    output.headers["Content-Disposition"] = "attachment; filename=log_information.csv"
    output.headers["Content-type"] = "text/csv"
    return output

@app.route("/download_images")
def download_images():
    time_str = time.strftime("%Y%m%d-%H%M%S")
    filename = "thermal_images_{}.zip".format(time_str)
    uploads_path = app.config["UPLOAD_FOLDER"]
    memory_file = io.BytesIO()
    with zipfile.ZipFile(memory_file, "w", zipfile.ZIP_DEFLATED) as zipf:
        for file in os.listdir(uploads_path):
            full_path = os.path.join(uploads_path, file)
            zipf.write(full_path, file)
            
    memory_file.seek(0)
    return send_file(
        memory_file,
        as_attachment=True,
        download_name=filename,
        mimetype='application/zip'
    )
         
@app.route("/log_information", methods=["POST"])
def add_log_information():
    try:
        required_fields = [
            "buildingName", "time", "observedTemp", "minTemp", "maxTemp",
            "distance", "position", "outdoorTemp"
        ]
        for field in required_fields:
            if field not in request.form:
                raise BadRequest(f"Missing required field: {field}")

        building_name = request.form["buildingName"]
        new_id = generate_id(building_name)
        try:
            dt_obj = datetime.strptime(request.form["time"], '%Y-%m-%dT%H:%M')
        except ValueError:
            raise BadRequest("Invalid time format. Use 'YYYY-MM-DDTHH:MM'.")

        log_info = LogInformation(
            photo_id=new_id,
            building_name=building_name,
            latitude=request.form["latitude"],
            longitude=request.form["longitude"],
            building_side=constants.BUILDING_SIDE[request.form["buildingSide"]],
            time=dt_obj,
            observed_temp=request.form["observedTemp"],
            min_temp=request.form["minTemp"],
            max_temp=request.form["maxTemp"],
            frame=constants.FRAME[request.form["frame"]],
            distance=request.form["distance"],
            outdoor_temp=request.form["outdoorTemp"],
            sun_direction=constants.SUN_DIRECTION[request.form["sunDirection"]],
            position=constants.POSITION[request.form["position"]],
            floor=constants.FLOOR[request.form["floor"]],
            notes=request.form.get("notes", "")
        )

        db.session.add(log_info)
        db.session.commit()

        if "image" in request.files and request.files["image"]:
            image_file = request.files["image"]
            if not allowed_file(image_file.filename):
                raise BadRequest("Invalid image file type.")
            filename = secure_filename(image_file.filename)
            file_extension = filename.rsplit(".", 1)[1].lower()
            image_path = os.path.join(app.config["UPLOAD_FOLDER"], f"{new_id}.{file_extension}")
            image_file.save(image_path)

        return jsonify({"message": "Log information added successfully!"}), 201

    except BadRequest as e:
        return jsonify({"error": str(e)}), 400

    except Exception as e:
        db.session.rollback() # Rollback DB if needed.
        return jsonify({"error": "An error occurred while processing the request.", "details": str(e)}), 500
    
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
            "notes": log.notes,
            "image_path": get_image(log.photo_id)
        })
    
    return jsonify(logs_list)

@app.route("/log_information/<photo_id>", methods=["DELETE"])
def delete_log_information(photo_id):
    log = LogInformation.query.filter_by(photo_id=photo_id).first()
    if not log:
        return jsonify({"error": "Log not found"}), 404

    image_path = os.path.join(app.config["UPLOAD_FOLDER"], photo_id)
    image_deleted = False
    for ext in app.config["ALLOWED_EXTENSIONS"]:
        temp_path = f"{image_path}.{ext}"
        if os.path.exists(temp_path):
            os.remove(temp_path)
            image_deleted = True
            break

    db.session.delete(log)
    db.session.commit()
    message = "Log deleted successfully!"
    if image_deleted:
        message += " Associated image also deleted."
    return jsonify({"message": message}), 200

@app.route("/upload_image", methods=["POST"])
def upload_image():
    photo_id = request.form.get("photo_id")
    image_file = request.files.get("image")

    if not photo_id or not image_file:
        return jsonify({"error": "Photo ID and image are required"}), 400

    filename = secure_filename(f"{photo_id}.jpg")
    image_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    image_file.save(image_path)

    return jsonify({"message": "Image uploaded successfully!"}), 200

@app.route('/')
def index():
    # TODO: Add Documentation HTML or Markdown here
    return

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
