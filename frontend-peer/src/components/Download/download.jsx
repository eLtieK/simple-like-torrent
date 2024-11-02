import React, { useState } from 'react';
import axios from 'axios';
import './download.css';

const Download = () => {
  const [magnetLink, setMagnetLink] = useState('');
  const [message, setMessage] = useState('');

  const handleDownload = async () => {
    if (!magnetLink) {
      setMessage("Vui lòng nhập magnet link để tải xuống.");
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
          withCredentials: true
        }
      );

      if (response.status === 200) {
        const { pieces, file_name } = response.data;
        const decodedPieces = pieces.map(piece => Uint8Array.from(atob(piece), c => c.charCodeAt(0)));
        const combinedBlob = new Blob(decodedPieces);
        const downloadUrl = window.URL.createObjectURL(combinedBlob);
        const link = document.createElement('a');
        link.href = downloadUrl;
        link.setAttribute('download', file_name);
        document.body.appendChild(link);
        link.click();
        link.remove();

        setMessage("File đã sẵn sàng để tải về.");
      } else {
        setMessage("Không thể tải file.");
      }
    } catch (error) {
      setMessage("Không thể tải file.");
    }
  };

  return (
    <div className="download-container">
      <h2>Download File</h2>
      <input
        type="text"
        placeholder="Nhập magnet link"
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
