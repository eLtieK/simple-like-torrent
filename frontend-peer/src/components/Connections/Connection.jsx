import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './Connection.css';

const Connection = ({ onConnect, isLoggedIn }) => {
  const [status, setStatus] = useState('');

  const getCookie = (name) => {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
    return null;
  };

  useEffect(() => {
    if (!isLoggedIn) {
      setStatus("Disconnected");
    }
  }, [isLoggedIn]);

  const handleConnect = async () => {
    const peerId = getCookie('peer_id');

    if (!peerId) {
      setStatus("Please log in to initiate the connection.");
      return;
    }

    try {
      const peerInfoResponse = await axios.get(`http://127.0.0.1:5000/peer/info`, {
        params: { peer_id: peerId }
      });
      const { ip_address, port } = peerInfoResponse.data;

      // const response = await axios.post(`http://127.0.0.1:5000/peer/start_peer`, {
      //   ip_address,
      //   port,
      // });
      
      setStatus(`Connected successfully from IP: ${ip_address} on Port: ${port}`);
      
      if (onConnect) onConnect();

    } catch (error) {
      setStatus(error.response?.data?.error || "Failed to connect to the P2P network.");
    }
  };

  return (
    <div className="connection-container">
      <button className="connection-button" onClick={handleConnect}>Connect to P2P Network</button>
      {status && <p className="connection-status">{status}</p>}
    </div>
  );
};

export default Connection;
