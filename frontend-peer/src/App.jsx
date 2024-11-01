// App.js
import React, { useState, useEffect } from 'react';
import './App.css';
import Navbar from './components/Navbar/Navbar';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Home from './views/pages/Home/Home';
import LoginSignup from './components/LoginSignup/login_signup';
import axios from 'axios';

axios.defaults.withCredentials = true;

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  useEffect(() => {
    const peer_id = document.cookie.split('; ').find(row => row.startsWith('peer_id='));
    setIsLoggedIn(!!peer_id);
  }, []);

  const handleLogout = async () => {
    try {
      const response = await axios.post('http://127.0.0.1:5000/tracker/peer/set_inactive', {}, {
        withCredentials: true,
      });

      if (response.status === 200) {
        document.cookie = 'peer_id=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;';
        setIsLoggedIn(false);
        setTimeout(() => {
          window.location.reload();
        }, 500);
      } else {
        console.error("Failed to logout. Please try again.");
      }
    } catch (error) {
      console.error(error.response ? error.response.data.error : "Failed to logout.");
    }
  };

  return (
    <Router>
      <Navbar isLoggedIn={isLoggedIn} handleLogout={handleLogout} />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/signin" element={<LoginSignup setIsLoggedIn={setIsLoggedIn} />} />
      </Routes>
    </Router>
  );
}

export default App;
