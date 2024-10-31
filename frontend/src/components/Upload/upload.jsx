import React, { useState } from 'react';
import axios from 'axios';
import './upload.css';



axios.defaults.withCredentials = true;
const Upload = ({ isConnected }) => {
  const [file, setFile] = useState(null);
  const [message, setMessage] = useState('');

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleUpload = async () => {
    if (!isConnected) {
      setMessage("You need to be connected to upload files.");
      return;
    }

    if (!file) {
      setMessage("Please select a file to upload.");
      return;
    }

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await axios.post('http://127.0.0.1:5000/tracker/uploading', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
        withCredentials: true, 
      });

      setMessage(response.data.message || "File uploaded successfully.");
    } catch (error) {
      setMessage(error.response?.data?.error || "Failed to upload file.");
    }
  };

  return (
    <div className="upload-container">
      <h2>Upload File</h2>
      <input type="file" onChange={handleFileChange} />
      <button onClick={handleUpload} className="upload-button">Upload</button>
      {message && <p className="upload-message">{message}</p>}
    </div>
  );
};

export default Upload;
