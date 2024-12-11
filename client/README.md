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