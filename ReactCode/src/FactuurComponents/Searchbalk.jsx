import React, { useState } from 'react';

const Searchbalk = ({ onSearch }) => {
  const [zoekTerm, setZoekTerm] = useState('');

  const handleSearch = () => {
    onSearch(zoekTerm);
  };

  return (
    <div className="Searchbalk">
      <div className="input-group mb-3">
        <input
          type="text"
          className="form-control searchTerm"
          placeholder="Zoek klant op naam"
          value={zoekTerm}
          onChange={(e) => setZoekTerm(e.target.value)}
        />
        <div className="input-group-append">
          <button
            type="button"
            className="btn btn-primary searchButton"
            onClick={handleSearch}
          >
            <i className="search">Zoek</i> 
          </button>
        </div>
      </div>
    </div>
  );
};

export default Searchbalk;
