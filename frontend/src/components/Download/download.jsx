import React, { useState } from 'react';
import axios from 'axios';
import './download.css';

const Download = () => {
  const [magnetLink, setMagnetLink] = useState('');
  const [message, setMessage] = useState('');

  const handleDownload = async () => {
    if (!magnetLink) {
      setMessage("Please enter a magnet link to download.");
      return;
    }

    try {
      const response = await axios.post(`http://127.0.0.1:5000/tracker/downloading/${encodeURIComponent(magnetLink)}`);
      setMessage(response.data.message);
    } catch (error) {
      setMessage(error.response?.data?.error || "Failed to download file.");
    }
  };

  return (
    <div className="download-container">
      <h2>Download File</h2>
      <input
        type="text"
        placeholder="Enter magnet link"
        value={magnetLink}
        onChange={(e) => setMagnetLink(e.target.value)}
        className="download-input"
      />
      <button onClick={handleDownload} className="download-button">Download</button>
      {message && <p className="download-message">{message}</p>}
    </div>
  );
};

export default Download;
