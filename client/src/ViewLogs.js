import React, { useEffect, useState } from "react";
import Navbar from "./Navbar";
import "./ViewLogs.css"
import axios from "axios";

const ViewLogs = () => {
    const [logs, setLogs] = useState([]);

    useEffect(() => {
        const fetchLogs = async () => {
            try {
                const response = await axios.get("http://localhost:5000/log_information");
                setLogs(response.data);
            } catch (error) {
                console.error("Error fetching log data:", error);
                alert("Failed to load log information");
            }
        }

        fetchLogs();
    }, []);

    const handleExportCSV = async (e) => {
        e.preventDefault();
        try {
            const response = await axios.get("http://localhost:5000/download_csv", {
                responseType: "blob"
            });
            
            const blob = response.data;
            const link = document.createElement("a");
            link.href = URL.createObjectURL(blob);
            link.download = "log_information.csv";
            link.click();
        } catch (error) {
            console.error("There was an error getting the data", error);
            alert("Error downlading CSV file.");
        }
    };

    const openImagePopup = (e, imagePath) => {
        e.preventDefault();
        const imageURL = `http://localhost:5000${imagePath}`;
        window.open(imageURL, "_blank");
    };


    return (
        <div className="viewlogs">
            <Navbar />
            <h2>Log and Image Registry</h2>
            <div className="table-container">
                <table className="logs-table">
                    <thead>
                    <tr>
                        <th>Photo ID</th>
                        <th>Building Name</th>
                        <th>Latitude</th>
                        <th>Longitude</th>
                        <th>Side of Building</th>
                        <th>Date and Time</th>
                        <th>Observed Temperature (°C)</th>
                        <th>Min Temperature (°C)</th>
                        <th>Max Temperature (°C)</th>
                        <th>Framed Properly?</th>
                        <th>Distance (m)</th>
                        <th>Outdoor Temperature (°C)</th>
                        <th>Sun Direction</th>
                        <th>Indoor/Outdoor</th>
                        <th>Floor</th>
                        <th>Image</th>
                    </tr>
                    </thead>
                    <tbody>
                    {logs.map((log) => (
                        <tr key={log.photo_id}>
                            <td>{log.photo_id}</td>
                            <td>{log.building_name}</td>
                            <td>{log.latitude}</td>
                            <td>{log.longitude}</td>
                            <td>{log.building_side}</td>
                            <td>{log.time}</td>
                            <td>{log.observed_temp}</td>
                            <td>{log.min_temp}</td>
                            <td>{log.max_temp}</td>
                            <td>{log.frame}</td>
                            <td>{log.distance}</td>
                            <td>{log.outdoor_temp}</td>
                            <td>{log.sun_direction}</td>
                            <td>{log.position}</td>
                            <td>{log.floor}</td>
                            <td>
                                <a href="#" onClick={(e) => openImagePopup(e, log.image_path)}>
                                    View Image
                                </a>
                            </td>
                        </tr>
                    ))}
                    </tbody>
                </table>
            </div>
            <div className="exportbuttons">
                <button onClick={handleExportCSV}>Export CSV</button>
                <button>Export Images</button>
            </div>
        </div>
    );
};

export default ViewLogs;