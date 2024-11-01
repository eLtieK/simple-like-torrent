import React, { useState } from 'react';
import axios from 'axios';
import './search.css';

const Search = () => {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);
  const [error, setError] = useState(null);
  const handleSearch = async () => {
    if (!query.trim()) {
      setError("Vui lòng nhập từ khóa để tìm kiếm.");
      return;
    }
    try {
      const combinedResults = [];
      try {
        const peerResponse = await axios.get(`http://127.0.0.1:5000/tracker/peer/${query}`);
        if (peerResponse.status === 200 && peerResponse.data) {
          combinedResults.push(peerResponse.data);
        }
      } catch (peerError) {
        if (peerError.response && peerError.response.status === 404) {
          console.warn("Peer không tồn tại");
        } else {
          console.error("Lỗi khi tìm kiếm Peer:", peerError);
        }
      }
      const fileResponse = await axios.get('http://127.0.0.1:5000/tracker/all_file');
      const files = Array.isArray(fileResponse.data) ? fileResponse.data : [];
      const fileResults = files.filter(file =>
        file.file_name && file.file_name.toLowerCase().includes(query.toLowerCase())
      );
      combinedResults.push(...fileResults);

      setResults(combinedResults);

      if (combinedResults.length === 0) {
        setError("Không tìm thấy kết quả nào.");
      } else {
        setError(null);
      }
    } catch (err) {
      setError("Lỗi khi tìm kiếm dữ liệu.");
      console.error("Lỗi khi tìm kiếm:", err);
    }
  };

  return (
    <div className="search-container">
      <h2>Tìm kiếm Peer hoặc File</h2>
      <div className="search-bar">
        <input
          type="text"
          placeholder="Nhập tên Peer hoặc File"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          className="search-input"
        />
        <button onClick={handleSearch} className="search-button">Tìm kiếm</button>
      </div>
      {error && <p className="error-message">{error}</p>}
      <div className="results-container">
        {results.length > 0 && !error ? (
          results.map((item, index) => (
            <div key={index} className="result-item">
              {item.name ? (
                <>
                  <p><strong>Peer Name:</strong> {item.name}</p>
                  {item.ip_address && <p><strong>IP Address:</strong> {item.ip_address}</p>}
                  {item.port && <p><strong>Port:</strong> {item.port}</p>}
                </>
              ) : (
                <>
                  <p><strong>File Name:</strong> {item.file_name}</p>
                  {item.length && <p><strong>File Size:</strong> {item.length} bytes</p>}
                  {item.seeder !== undefined && <p><strong>Seeder:</strong> {item.seeder}</p>}
                  {item.magnet_link && <p><strong>Magnet Link:</strong> {item.magnet_link}</p>}
                </>
              )}
            </div>
          ))
        ) : (
          <p>{error}</p>
        )}
      </div>
    </div>
  );
};

export default Search;
