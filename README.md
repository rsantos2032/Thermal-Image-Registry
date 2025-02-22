# Loyola Thermal Image Project

Hello World

## Project Setup

This project utilizes Docker and Docker Compose to manage both the frontend (client) and backend (API) services. Docker Desktop is recommended for local machines to run the project without issue.

### Integration of API and Client

- **API Service**: The backend is hosted in the `api` service, which is built from the Dockerfile located in the `./api` directory. It exposes port `5000`, and uses volumes to bind the local `api` directory and its subdirectories (`database`, `uploads`) to the container's file system. This allows the containerized backend to directly interact with local files for database storage and image uploads.
- **Client Service**: The frontend is hosted in the `client` service, which is built from the Dockerfile in the `./client` directory. It exposes port `3000` and includes volumes to allow the frontend code to sync with the container. This ensures that any changes made to the frontend code are reflected inside the container during development.
- **Service Dependencies**:  The `client` service is configured to depend on the `api` service, ensuring that the frontend waits for the backend to be fully operational before it starts. This eliminates race conditions in the startup process.

### Running the Project
To set up and run the entire project, Docker Compose is used. The only commands needed are:
1. **Building the containers**: \
From the root directory run:
    ```bash
    docker-compose build
    ```
2. **Starting the containers**: \
After building, start the containers with:
    ```bash
    docker-compose up
    ```
    If you wish to run the services in the background, add the `-d` flag:
    ```bash
    docker-compose up -d
    ```

The services may take a few minutes to get build. Once that is done, the client will be accessible at `http://localhost:3000` and the API will be accessible at `http://localhost:5000`. Note `localhost` will be the IP address used if running on your local machine. `http://localhost:5000` should just return API documentation, but should indicate the API service is running.

The way the project was hosted online for demoing was through DigitalOcean. An Ubunut DigitalOcean droplet was created. The code was then downloaded into the droplet via git, and the service was ran from there after `docker` and `docker-compose` was installed. Note that the `.env` file IP address needs to be the IP address of the droplet and not `localhost`.

## Client (Frontend)

This frontend client application interacts with the backend API to manage and display thermal log data and images. It provides the following functionality for users:

### Features:

#### 1. Log Form Submission:
- Users can submit new thermal log data, including details such as building name, coordinates, temperature readings and additional notes.
- (OPTIONAL) Users can upload images associated with the log data.

#### 2. View Logs:
- Displays a table of all available logs retrieved from the API.
- Users can view individual thermal images associated with each log.
- Allows users to delete logs and images directly from the interface.
- If a user did not upload an image for their log yet, they may do so here.
- Provides options to export log data in CSV format and images in a ZIP file.

### Environment Setup:

#### `npm install`

To run this application, `Node.js` is required. If project is downloaded from Github, the `/node_modules/` folder may not be present in the `/client` directory. If this is the case, please run `npm install` from **WITHIN** the `/client/` folder. To navigate to the `client/` directory and run `npm install` in one command from the main project directory, use the following bash script:

```bash
cd client/ && npm install
```

#### `.env`

For backend connection to work, the project IP address must be adjusted in the `.env` file. If no `.env` file is present, copy and paste the URI from the provided `.env.example` and create a new `.env` file in the same directory. To test the application on your local machine. Change the `REACT_APP_API_URL=http://IP_ADDRESS:5000` to `REACT_APP_API_URL=http://localhost:5000`.

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

## Migrations

This directory contains the necessary scripts for migrating log information and images to the database, as well as for resetting the database for testing purposes.

### Migration Script: `migrations.py`

The `migrations.py` script is designed to upload log information and images into the database. It supports optional arguments to specify log files and image directories to be migrated.

#### Usage:

To run the migration script and upload log information and images, execute the following command from the project root directory:

```bash
python migrations/migrations.py
```

#### Arguments:

- `-l` or `--logfile`: Specify the path to a new log file to be migrated: Example: 
    ```bash
    python migrations/migrations.py -l /path/to/dir/log_information_november.csv
    ```
- `-i` or `-imagedirectory`: Specify the path to the directory containing images to be migrated. Example:
    ```bash
    python migrations/migrations.py -i /path/to/dir/images
    ```

#### Behavior:

1. By default, the script will check the `migrations/` directory for `.csv` files and image folders containing `"_Hall"` in the name.
2. If the `-l` argument is provided, the specified log file will be added to the migration process.
3. If the `-i` argument is provided, the specified image directory will be included for migration.
4. Log files are processed using pandas, and the data is inserted into the `log_information` table in the SQLite database.
5. Image files are copied from the specified directories to the `api/uploads/` directory.

### Deletion Script: `deletion.py`

The `deletion.py` script is used for resetting the database and deleting all image files from the uploads directory. It is intended for testing purposes.

#### Usage:

To reset the database and remove images, run the following command:

```bash
python migrations/deletion.py
```

### Behavior:

1. The script will drop the `log_information` table from the SQLite database, effectively resetting it.
2. The script will also remove all files in the `api/uploads/` directory, ensuring a clean slate for testing purposes.

**WARNING**: This operation is destructive and should be used carefully, as it removes both log data and images from the system. Please ensure a copy of the images and log information is stored before running this script.
