import styled from 'styled-components';
import { NavLink as Link } from 'react-router-dom'; 
import { FaBars } from 'react-icons/fa';

export const Nav = styled.nav`
    background: #000;
    height: 80px;
    display: flex;
    justify-content: space-between;
    padding: 0.5rem calc((100vw - 1000px) / 2);
    z-index: 10;

`

export const NavLink = styled(Link)`
    color: #fff;
    display: flex;
    align-items: center;
    text-decoration: none;
    padding: 0 1rem;
    height: 100%;
    cursor: pointer;

    &.active {
        color: #15cdfc;
    }

`

export const Bar = styled(FaBars)`
    display: none;
    color: #fff;
    @media screen and (max-width: 768px) {
        display: block;
        position: absolute;
        top: 0;
        right: 0;
        transform: translate(-100%, 75%);
        font-size: 1.8rem;
        cursor: pointer;
    }

`  


export const NavMenu = styled.div`
    display: flex;
    align-items: center;
    margin-right: -24px;
    
    @media screen and (max-width: 768px) {
        display: none;
    }
    
`

export const NavBtn = styled.nav`
    display: flex;
    align-items: center;
    margin-right: 24px;
    
    @media screen and (max-width: 768px) {
        display: none;
    }

    .nav-btn-logout {
  background-color: #4c00b4; /* Màu giống với Sign In */
  color: white;
  font-weight: bold;
  padding: 10px 20px;
  border-radius: 25px; /* Radius giống Sign In */
  text-decoration: none;
  border: none;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.nav-btn-logout:hover {
  background-color: #3700b3;
}

`;


export const NavBtnLink = styled(Link)`
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: #4c00b4;
  color: white;
  font-weight: bold;
  padding: 10px 20px;
  border-radius: 25px;
  text-decoration: none; /* Loại bỏ dấu gạch chân */
  transition: background-color 0.3s ease;

  &:hover {
    background-color: #3700b3;
  }
`;


