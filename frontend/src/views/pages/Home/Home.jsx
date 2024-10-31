import React, { useEffect, useState } from 'react';
import './Home.css';
import Connection from '../../../components/Connections/Connection';
import Upload from '../../../components/Upload/upload';
import Download from '../../../components/Download/download';

const getCookieValue = (name) => {
  const match = document.cookie.match(new RegExp('(^| )' + name + '=([^;]+)'));
  return match ? match[2] : null;
};

const Home = () => {
  const [ipAddress, setIpAddress] = useState(null);
  const [port, setPort] = useState(null);
  const [isConnected, setIsConnected] = useState(false);

  const handleConnectionSuccess = () => {
    setIsConnected(true);
  };

  return (
    <div className="home-container">
      <h1 className="welcome-message">Welcome to the BKtorrent Website</h1>
      <Connection onConnect={handleConnectionSuccess} />
      {isConnected && (
        <>
          <p className="connected-message">Connected to P2P Network</p>
          <p className="connection-status">
            Connected successfully from IP: {ipAddress} on Port: {port}
          </p>
          <Upload isConnected={isConnected} />
          <Download />
        </>
      )}
    </div>
  );
};

export default Home;
