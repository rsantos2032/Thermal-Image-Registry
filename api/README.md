## API (Backend)

This API provides functionality for managing log information and associated images for building temperature monitoring. It allows you to:

- Add new log information along with images.
- Retrieve log information.
- Delete log entries and associated images.
- Download logs and images as CSV or ZIP files.

In additon the API contains application logic and utilities such as:
- Unique ID generation.
- Database and image storage.
- Database Model information.

### Environment Setup:

To run this application, you need the following:
1. Python 3.x
2. Flask
3. SQLAlchemy
4. Flask-CORS

Most of the environment setup will be done by docker upon container creation.

### Endpoints

#### 1. `/log_information` (GET)
- **Description**: Retrieves all log information from the database.
- **Response**: A list of logs with details such as photo ID, building name, latitude, longitude, and observed temperature.
- **Example Response**:
  ```json
  [
    {
      "photo_id": "CH01",
      "building_name": "Cuneo Hall",
      "latitude": "N 41°59'58.6959",
      "longitude": "W 87°39'26.68310",
      "building_side": "North",
      "time": "2024-10-01 02:29:00 PM",
      "observed_temp": 25.0,
      "min_temp": 22.0,
      "max_temp": 28.0,
      "frame": "Door",
      "distance": 10,
      "outdoor_temp": 18.8,
      "sun_direction": "West",
      "position": "Outdoor",
      "floor": "Ground Level",
      "notes": "Insect on window when image was taken"
    }
  ]

#### 2. `/log_information` (POST)
- **Description**: Adds a new log entry to the database along with an optional image.
- **Parameters** (Form Data):
    - `buildingName`: The name of the building
    - `latitude`: Latitude coordinates of user position when image was taken
    - `longitude`: Longitude coordinates of user position when image was taken
    - `time`: The time of the observation (`YYYY-MM-DDTHH:MM` format)
    - `observedTemp`: The observed temperature from the IR camera
    - `minTemp`: The minimum temperature of image captured from IR camera
    - `maxTemp`: The maximum temperature of image captured from IR camera
    - `frame`: Window/Door framing; Yes/No if window was framed properly when image was taken
    - `distance`: Distance recorded on IR camera settings
    - `outdoorTemp`: Outdoor Temperature (from weather app)
    - `sunDirection`: Direction of sun when image was taken.
    - `position`: Whether user took image indoors or outdoors
    - `floor`: The floor the window/door image was taken from
    - `notes`: Additional notes
- **Response** A success message confirming the log has been added.

#### 3. `/log_information/<photo_id>` (DELETE)
- **Description**: Deletes the log entry and associated image (if found) by the `photo_id`.
- **Parameters**:
    - `photo_id`: The ID of the log and photo entry to be deleted.
- **Response**: A success message or an error message if the log is not found.

#### 4. `/download_csv` (GET)

- **Description**:  Downloads a CSV file containing all the log entries.
- **Response**: A CSV file containing the log information.

#### 5. `download_images` (GET)

- **Description**: Downloads a ZIP file containing all uploaded images.
- **Response**: A ZIP file containing all images.

#### 6. `upload_image` (POST)

- **Description**: Uploads a new image for a specific photo ID.
- **Parameters** (Form Data):
    - `photo_id`: The photo ID for which the image is being uploaded.
    - `image`: The image file to upload
- **Response**: A success message confirming the image upload.

#### 7. `/uploads/<filename>` (GET)
- **Description**: Serves the uploaded image based on the filename.
- **Parameters**:
    - `filname`: The name of the file to retrieve (the photo ID).
- **Response**: The image file.

### Application Logic

#### 1. `generate_id(building_name)`
- **Description**: Generates a unique photo ID based on the building's name and the latest photo ID in the database for that building.
- **Input** `building_name` (string) - The name of the building
- **Output** `new_id` (string) - A newly generated unique photo ID.

#### 2. `get_image(photo_id)`
- **Description**: Retrieves the image path fora  given `photo_id`.
- **Input** `photo_id` (string) - The photo ID of the log entry.
- **Output**: A URL to the image file or `None` if no image is found.

### Models

#### `Log Information` Model

The `Log Information` Model represents a single log entry, including thermal image data and associated metadata.

| Column Name        | Type        | Description |
|--------------------|-------------|-------------|
| `photo_id`         | String(6)   | Primary key; unique identifier for the log. |
| `building_name`    | Text        | The name of the building where the log was recorded. |
| `latitude`         | Text        | Latitude coordinates of the user position when the image was taken. |
| `longitude`        | Text        | Longitude coordinates of the user position when the image was taken. |
| `building_side`    | String(5)   | Side of the building (e.g., North, South). |
| `time`             | DateTime    | The time of the observation in `YYYY-MM-DDTHH:MM` format. |
| `observed_temp`    | Numeric     | The observed temperature from the IR camera. |
| `min_temp`         | Numeric     | The minimum temperature of the image captured by the IR camera. |
| `max_temp`         | Numeric     | The maximum temperature of the image captured by the IR camera. |
| `frame`            | String(12)  | Window/Door framing; Yes/No if window was framed properly when the image was taken. |
| `distance`         | Numeric     | Distance recorded on IR camera settings. |
| `outdoor_temp`     | Numeric     | Outdoor temperature (from weather app) at the time of observation. |
| `sun_direction`    | String(12)  | Direction of the sun when the image was taken. |
| `position`         | String(8)   | Whether the image was taken indoors or outdoors. |
| `floor`            | Text        | The floor the window/door image was taken from. |
| `notes`            | Text        | Additional notes. |

### Database
- **Database File**: `app.db` located under `api/database/` is the SQLite database used for this project where log information is stored.
- **Image Directory**: All uploaded thermal images are stored in the `api/uploads/` directory.