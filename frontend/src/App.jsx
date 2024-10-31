import React, { useState, useEffect } from 'react';
import './App.css';
import Navbar from './components/Navbar/Navbar';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Home from './views/pages/Home/Home';
import LoginSignup from './components/LoginSignup/login_signup';

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  useEffect(() => {
    // Kiểm tra trạng thái đăng nhập dựa vào cookie
    const peer_id = document.cookie.split('; ').find(row => row.startsWith('peer_id='));
    setIsLoggedIn(!!peer_id);
  }, []);

  const handleLogout = () => {
    // Xóa cookie peer_id và cập nhật trạng thái đăng nhập
    document.cookie = "peer_id=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
    setIsLoggedIn(false);
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
