import React from 'react';
import ListPeer from "../../../components/ListPeer/ListPeer";
import ListFile from "../../../components/ListFile/ListFile";
import './Home.css';
import Search from '../../../components/Search/search';

const Home = () => {
  return (
    <>  
        <h1>Welcome to Tracker Home</h1>
        <Search/>
        <div className="home-container">
            <ListPeer />
            <ListFile />
        </div>
    </>
  );
}

export default Home;
