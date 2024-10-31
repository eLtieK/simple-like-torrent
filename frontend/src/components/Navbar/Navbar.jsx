import React from 'react';
import { Nav, NavLink, NavMenu, Bar, NavBtn, NavBtnLink } from './NavbarEle';

const Navbar = ({ isLoggedIn, handleLogout }) => {
  return (
    <Nav>
      <NavLink to="/" exact>
        <h1>Logo</h1>
      </NavLink>
      <Bar />
      <NavMenu>
        <NavLink 
          to="/about" 
          activeStyle={{ fontWeight: 'bold', color: 'red' }}
        >
          About
        </NavLink>
        <NavLink 
          to="/services" 
          activeStyle={{ fontWeight: 'bold', color: 'red' }}
        >
          Services
        </NavLink>
        <NavLink 
          to="/contact-us" 
          activeStyle={{ fontWeight: 'bold', color: 'red' }}
        >
          Contact us
        </NavLink>
      </NavMenu>
      {isLoggedIn ? (
        <NavBtn>
          <button onClick={handleLogout} className="nav-btn-logout">
            Log Out
          </button>
        </NavBtn>
      ) : (
        <NavBtn>
          <NavBtnLink to="/signin">Sign In</NavBtnLink>
        </NavBtn>
      )}
    </Nav>
  );
};

export default Navbar;
