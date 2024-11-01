import React, { useState } from 'react';
import './Home.css';
import Connection from '../../../components/Connections/Connection';
import Upload from '../../../components/Upload/upload';
import Download from '../../../components/Download/download';


const Home = () => {

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
          <Upload isConnected={isConnected} />
          <Download />
        </>
      )}
    </div>
  );
};

export default Home;
