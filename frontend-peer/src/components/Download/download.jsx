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
      const peerId = document.cookie
        .split('; ')
        .find(row => row.startsWith('peer_id='))
        ?.split('=')[1];
      if (!peerId) {
        setMessage("Bạn cần phải đăng nhập trước khi kết nối tới peer.");
        return;
      }
      const response = await axios.post(
        `http://127.0.0.1:5000/tracker/downloading/${magnetLink}`,
        {}, 
        {
          headers: {
            "Content-Type": "application/json",
          },
          withCredentials: true, 
        }
      );

      if (response.status === 200) {
        setMessage("Đã tải file thành công và được lưu ở ổ đĩa C thư mục Downloads.");
      } else {
        setMessage("Failed to download file.");
      }
    } catch (error) {
      setMessage("Failed to download file.");
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
