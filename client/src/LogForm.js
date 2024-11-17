import { useState } from "react";
import Navbar from "./Navbar";
import "./LogForm.css";
import axios from "axios"

const LogForm = () => {
    const [formData, setFormData] = useState({
        buildingName: "1",
        latitude: "",
        longitude: "",
        buildingSide: "1",
        time: "",
        observedTemp: "",
        minTemp: "",
        maxTemp: "",
        frame: "1",
        distance: "",
        outdoorTemp: "",
        sunDirection: "1",
        position: "1",
        floor: "1",
        notes: "",
        image: null
    });

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData(prevState => ({
            ...prevState,
            [name]: value
        }));
    };

    const handleImageChange = (e) => {
        const file = e.target.files[0];
        if (file && file.type.startsWith("image/")) {
            setFormData((prevState) => ({
                ...prevState,
                image: file
            }));
        } else {
            alert("Please upload a valid image file.");
        }
    };

    const openImagePopup = (e) => {
        e.preventDefault();
        if (formData.image){
            const imageURL = URL.createObjectURL(formData.image);
            window.open(imageURL, "_blank");
        }
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        const form = new FormData();
        form.append("buildingName", formData.buildingName);
        form.append("latitude", formData.latitude);
        form.append("longitude", formData.longitude);
        form.append("buildingSide", formData.buildingSide);
        form.append("time", formData.time);
        form.append("observedTemp", formData.observedTemp);
        form.append("minTemp", formData.minTemp);
        form.append("maxTemp", formData.maxTemp);
        form.append("frame", formData.frame);
        form.append("distance", formData.distance);
        form.append("outdoorTemp", formData.outdoorTemp);
        form.append("sunDirection", formData.sunDirection);
        form.append("position", formData.position);
        form.append("floor", formData.floor);

        console.log(formData);
        if (formData.image){
            form.append("image", formData.image);
        }

        try{
            await axios.post("http://localhost:5000/log_information", form, {
                headers: {
                    "Content-Type": "multipart/form-data"
                },
            });
            alert("Log Information Submitted Successfully!");

            setFormData({
                buildingName: "1",
                latitude: "",
                longitude: "",
                buildingSide: "1",
                time: "",
                observedTemp: "",
                minTemp: "",
                maxTemp: "",
                frame: "1",
                distance: "",
                outdoorTemp: "",
                sunDirection: "1",
                position: "1",
                floor: "1",
                image: null
            });
        } catch(error){
            alert("Error submitting the form. Please try again.")
        }
    };

    return(
        <div className="logform">
            <Navbar />
            <h2>Log Form</h2>
            <form onSubmit={handleSubmit}>
                {/* Building Name */}
                <div>
                    <label>Building Name:  
                        <select
                            name="buildingName" 
                            value={formData.buildingName} 
                            onChange={handleChange} 
                            required
                        >
                            <option value="1">Cuneo Hall</option>
                            <option value="2">Dumbach Hall</option>
                        </select>
                    </label>
                </div>

                 {/* Latitude */}
                 <div>
                    <label>Latitude:
                        <input
                            type="text"
                            name="latitude"
                            value={formData.latitude}
                            onChange={handleChange}
                            placeholder="Enter Latitude" 
                        />
                    </label>
                </div>

                {/* Longitude */}
                 <div>
                    <label>Latitude:
                        <input
                            type="text"
                            name="longitude"
                            value={formData.longitude}
                            onChange={handleChange}
                            placeholder="Enter Longitude" 
                        />
                    </label>
                </div>

                {/* Building Side */}
                <div>
                    <label>Side of Building:  
                        <select
                            name="buildingSide" 
                            value={formData.buildingSide} 
                            onChange={handleChange} 
                            required
                        >
                            <option value="1">East</option>
                            <option value="2">West</option>
                            <option value="3">North</option>
                            <option value="4">South</option>
                        </select>
                    </label>
                </div>

                {/* Time */}
                <div>
                    <label>Date and Time:
                        <input
                            type="datetime-local"
                            name="time"
                            value={formData.time}
                            onChange={handleChange}
                            required
                        />
                    </label>
                </div>

                {/* Observed Temp */}
                <div>
                    <label>Observed Temperature (°C):
                        <input
                            type="number"
                            name="observedTemp"
                            value={formData.observedTemp}
                            onChange={handleChange}
                            placeholder="Enter temperature in °C"
                            min="-100"
                            max="100"
                            required
                        />
                    </label>
                </div>

                {/* Min Temp */}
                <div>
                    <label>Min Temperature (°C):
                        <input
                            type="number"
                            name="minTemp"
                            value={formData.minTemp}
                            onChange={handleChange}
                            placeholder="Enter temperature in °C"
                            min="-100"
                            max="100"
                            required
                        />
                    </label>
                </div>
                
                {/* Max Temp */}
                <div>
                    <label>Max Temperature (°C):
                        <input
                            type="number"
                            name="maxTemp"
                            value={formData.maxTemp}
                            onChange={handleChange}
                            placeholder="Enter temperature in °C"
                            min="-100"
                            max="100"
                            required
                        />
                    </label>
                </div>

                {/* Frame */}
                <div>
                    <label>Frame Properly?:  
                        <select
                            name="frame" 
                            value={formData.frame} 
                            onChange={handleChange} 
                            required
                        >
                            <option value="1">Yes</option>
                            <option value="2">No</option>
                            <option value="3">Door</option>
                            <option value="4">Open Window</option>
                        </select>
                    </label>
                </div>

                {/* Distance */}
                <div>
                    <label>Distance (m):
                        <input
                            type="number"
                            name="distance"
                            value={formData.distance}
                            onChange={handleChange}
                            placeholder="Enter distance in meters"
                            required
                        />
                    </label>
                </div>

                {/* Outdoor Temp */}
                <div>
                    <label>Outdoor Temperature (°C):
                        <input
                            type="number"
                            name="outdoorTemp"
                            value={formData.outdoorTemp}
                            onChange={handleChange}
                            placeholder="Enter temperature in °C"
                            min="-100"
                            max="100"
                        />
                    </label>
                </div>

                {/* Sun Direction */}
                <div>
                    <label>Sun Direction:  
                        <select
                            name="sunDirection" 
                            value={formData.sunDirection} 
                            onChange={handleChange} 
                            required
                        >
                            <option value="1">East</option>
                            <option value="2">West</option>
                            <option value="3">Dark</option>
                        </select>
                    </label>
                </div>

                {/* Position */}
                <div>
                    <label>Indoor/Outdoor:  
                        <select
                            name="position" 
                            value={formData.position} 
                            onChange={handleChange} 
                            required
                        >
                            <option value="1">Indoor</option>
                            <option value="2">Outdoor</option>
                        </select>
                    </label>
                </div>

                {/* Floor */}
                <div>
                    <label>Floor:  
                        <select
                            name="floor" 
                            value={formData.floor} 
                            onChange={handleChange} 
                            required
                        >
                            <option value="1">Ground Level</option>
                            <option value="2">Second Floor</option>
                            <option value="3">Third Floor</option>
                            <option value="4">Fourth Floor</option>
                        </select>
                    </label>
                </div>

                {/* Notes */}
                <div>
                    <label>Additional Notes:
                        <textarea
                            name="notes"
                            value={formData.notes}
                            onChange={handleChange}
                            placeholder="Enter Notes" 
                        />
                    </label>
                </div>

                {/* Image */}
                <div>
                    <label>Upload Image:</label>
                    <input
                        type="file"
                        name="image"
                        accept="image/*"
                        required
                        onChange={handleImageChange}
                    />
                    {formData.image && (
                        <div>
                            <a
                                href="#"
                                className="image-link"
                                onClick={openImagePopup}
                            >
                                Image Link
                            </a>
                        </div>
                    )}
                </div>

                <div className="submitbutton">
                    <button>Submit</button>
                </div>

            </form>
        </div>
    );
}

export default LogForm;