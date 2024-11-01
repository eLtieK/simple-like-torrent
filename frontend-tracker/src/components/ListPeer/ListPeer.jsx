import React, { useEffect, useState } from 'react';
import axios from 'axios';
import "./ListPeer.css";

const ListPeer = () => {
  const [peers, setPeers] = useState([]);
  const [totalCount, setTotalCount] = useState(0);
  const [error, setError] = useState(null);
  const [currentPage, setCurrentPage] = useState(1);
  const peersPerPage = 3; 
  const fetchPeers = async () => {
    try {
      const response = await axios.get('http://127.0.0.1:5000/tracker/all_peer');
      setPeers(response.data.peers || []);
      setTotalCount(response.data.total_count || 0); 
      setError(null);
    } catch (error) {
      setError("Không thể lấy danh sách Peer.");
      console.error("Lỗi khi lấy danh sách Peer:", error);
    }
  };
  useEffect(() => {
    fetchPeers();
  }, []);
  const indexOfLastPeer = currentPage * peersPerPage;
  const indexOfFirstPeer = indexOfLastPeer - peersPerPage;
  const currentPeers = peers.slice(indexOfFirstPeer, indexOfLastPeer);
  const paginate = (pageNumber) => setCurrentPage(pageNumber);
  const handlePrevPage = () => {
    if (currentPage > 1) {
      setCurrentPage(currentPage - 1);
    }
  };
  const handleNextPage = () => {
    if (currentPage < Math.ceil(totalCount / peersPerPage)) {
      setCurrentPage(currentPage + 1);
    }
  };
  const handleLastPage = () => {
    setCurrentPage(Math.ceil(totalCount / peersPerPage));
  };
  const pageNumbers = [];
  for (let i = 1; i <= Math.ceil(totalCount / peersPerPage); i++) {
    pageNumbers.push(i);
  }

  return (
    <div className="peer-list-container">
      <h2>Danh Sách Peer</h2>
      {error && <p className="error-message">{error}</p>}
      <div className='button-and-info'>
        <button onClick={fetchPeers} className="reload-button">Cập nhật dữ liệu</button> 
        <p>Tổng số Peer: {totalCount}</p> 
      </div>
      <ul className="peer-list">
        {currentPeers.map((peer, index) => (
          <li key={index} className="peer-item">
            <p><strong>Tên:</strong> {peer.name}</p>
            <p><strong>Địa chỉ IP:</strong> {peer.ip_address}</p>
            <p><strong>Cổng:</strong> {peer.port}</p>
          </li>
        ))}
      </ul>
      <div className="pagination">
        <button onClick={handlePrevPage} className="nav-button">Trang Trước</button>
        {pageNumbers.map((number) => (
          <button
            key={number}
            onClick={() => paginate(number)}
            className={number === currentPage ? "active" : ""}
          >
            {number}
          </button>
        ))}
        <button onClick={handleNextPage} className="nav-button">Trang Sau</button>
        <button onClick={handleLastPage} className="nav-button">Trang Cuối</button>
      </div>
    </div>
  );
}

export default ListPeer;
