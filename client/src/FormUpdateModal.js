import React, { useState } from "react";
import axios from "axios";
import "./FormUpdateModal.css";

const FormUpdateModal = ({ isOpen, onClose, photoId, onUploadSuccess }) => {
    const [imageFile, setImageFile] = useState(null);

    const handleImageChange = (e) => {
        setImageFile(e.target.files[0]);
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (!imageFile) {
            alert("Please select an image to upload.");
            return;
        }

        const formData = new FormData();
        formData.append("image", imageFile);
        formData.append("photo_id", photoId);

        try {
            const appURL = process.env.REACT_APP_API_URL;
            await axios.post(`${appURL}/upload_image`, formData, {
                headers: { "Content-Type": "multipart/form-data" },
            });
            alert("Image uploaded successfully!");
            onUploadSuccess();
            onClose();
        } catch (error) {
            console.error("Error uploading image:", error);
            alert("Failed to upload image. Please try again.");
        }
    };

    if (!isOpen) return null;

    return (
        <div className="modal-overlay">
            <div className="modal-content">
                <h2>Upload Image for {photoId}</h2>
                <form onSubmit={handleSubmit}>
                    <input type="file" accept="image/*" onChange={handleImageChange} />
                    <div className="modal-buttons">
                        <button type="submit">Upload</button>
                        <button type="button" onClick={onClose}>Close</button>
                    </div>
                </form>
            </div>
        </div>
    );
};

export default FormUpdateModal;