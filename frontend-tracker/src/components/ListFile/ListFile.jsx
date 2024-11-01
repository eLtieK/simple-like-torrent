import React, { useEffect, useState } from 'react';
import axios from 'axios';
import "./ListFile.css";

const ListFile = () => {
  const [files, setFiles] = useState([]);
  const [totalCount, setTotalCount] = useState(0);
  const [error, setError] = useState(null);
  const [currentPage, setCurrentPage] = useState(1);
  const filesPerPage = 3; 
  const fetchFiles = async () => {
    try {
      const response = await axios.get('http://127.0.0.1:5000/tracker/all_file');
      setFiles(response.data || []);
      setTotalCount(response.data.length || 0);
      setError(null);
    } catch (error) {
      setError("Không thể lấy danh sách tệp.");
      console.error("Lỗi khi lấy danh sách tệp:", error);
    }
  };
  useEffect(() => {
    fetchFiles();
  }, []);
  const indexOfLastFile = currentPage * filesPerPage;
  const indexOfFirstFile = indexOfLastFile - filesPerPage;
  const currentFiles = files.slice(indexOfFirstFile, indexOfLastFile);
  const paginate = (pageNumber) => setCurrentPage(pageNumber);
  const handlePrevPage = () => {
    if (currentPage > 1) {
      setCurrentPage(currentPage - 1);
    }
  };
  const handleNextPage = () => {
    if (currentPage < Math.ceil(totalCount / filesPerPage)) {
      setCurrentPage(currentPage + 1);
    }
  };
  const handleLastPage = () => {
    setCurrentPage(Math.ceil(totalCount / filesPerPage));
  };
  const pageNumbers = [];
  for (let i = 1; i <= Math.ceil(totalCount / filesPerPage); i++) {
    pageNumbers.push(i);
  }

  return (
    <div className="file-list-container">
      <h2>Danh Sách Tệp</h2>
      {error && <p className="error-message">{error}</p>}
      <div className='button-and-info'>
        <button onClick={fetchFiles} className="reload-button">Cập nhật dữ liệu</button> 
        <p>Tổng số tệp: {totalCount}</p> 
      </div>     
      <ul className="file-list">
        {currentFiles.map((file, index) => (
          <li key={index} className="file-item">
            <p><strong>Tên tệp:</strong> {file.file_name}</p>
            <p><strong>Kích thước:</strong> {file.length} bytes</p>
            <p><strong>Số lượng Seeder:</strong> {file.seeder}</p>
            <p><strong>Magnet Link:</strong> {file.magnet_link}</p> 
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
};

export default ListFile;
