import axios from "axios";
import React, { useEffect, useState } from "react";
import FormUpdateModal from "./FormUpdateModal";
import Navbar from "./Navbar";
import "./ViewLogs.css";
import XButton from "./red-x-icon.svg"

const ViewLogs = () => {
    const [logs, setLogs] = useState([]);
    const [isModalOpen, setIsModalOpen] = useState(false);
    const [selectedPhotoId, setSelectedPhotoId] = useState("");

    const fetchLogs = async () => {
        try {
            const appURL = process.env.REACT_APP_API_URL;
            const response = await axios.get(`${appURL}/log_information`);
            setLogs(response.data);
        } catch (error) {
            console.error("Error fetching log data:", error);
            alert("Failed to load log information");
        }
    }

    useEffect(() => {
        fetchLogs();
    }, []);

    const openModal = (photoId) => {
        setSelectedPhotoId(photoId);
        setIsModalOpen(true);
    };

    const closeModal = () => {
        setIsModalOpen(false);
        setSelectedPhotoId("");
    };

    const handleExportCSV = async (e) => {
        e.preventDefault();
        try {
	        const appURL = process.env.REACT_APP_API_URL;
            const response = await axios.get(`${appURL}/download_csv`, {
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

    const handleDelete = async (photoId) => {
        if (!window.confirm("Are you sure you want to delete this log?")) {
            return;
        }

        try {
            const appURL = process.env.REACT_APP_API_URL;
            await axios.delete(`${appURL}/log_information/${photoId}`);
            alert("Log deleted successfully!");

            setLogs((prevLogs) => prevLogs.filter((log) => log.photo_id !== photoId));
        } catch (error) {
            console.error("Error deleting the log:", error);
            alert("Failed to delete the log. Please try again.");
        }
    };

    const handleExportImages = async (e) => {
        e.preventDefault();
        try {
            const appURL = process.env.REACT_APP_API_URL;
            const response = await axios.get(`${appURL}/download_images`, {
                responseType: "blob"
            });
    
            const blob = response.data;
            const link = document.createElement("a");
            link.href = URL.createObjectURL(blob);
            link.download = "thermal_images.zip";
            link.click();
            URL.revokeObjectURL(link.href);
        } catch (error) {
            console.error("There was an error downloading the images", error);
            alert("Error downloading image ZIP file.");
        }
    };

    const openImagePopup = (e, imagePath) => {
        e.preventDefault();
	    const appURL = process.env.REACT_APP_API_URL;
        const imageURL = `${appURL}${imagePath}`;
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
	    		        <th>Notes</th>
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
			                <td>{log.notes}</td>
                            <td>
                                {log.image_path ? (
                                    <a href="#" onClick={(e) => openImagePopup(e, log.image_path)}>
                                        View Image
                                    </a>
                                ) : (
                                    <a href="#" onClick={() => openModal(log.photo_id)}>
                                        Add Image
                                    </a>
                                )}
                            </td>
                            <td>
                                <button 
                                    onClick={() => handleDelete(log.photo_id)}
                                    className="delete-button">
                                    <img src={XButton} alt="Delete" />
                                </button>
                            </td>
                        </tr>
                    ))}
                    </tbody>
                </table>
            </div>
            <FormUpdateModal
                isOpen={isModalOpen}
                onClose={closeModal}
                photoId={selectedPhotoId}
                onUploadSuccess={fetchLogs}
            />
            <div className="exportbuttons">
                <button onClick={handleExportCSV}>Export CSV</button>
                <button onClick={handleExportImages}>Export Images</button>
            </div>
        </div>
    );
};

export default ViewLogs;
