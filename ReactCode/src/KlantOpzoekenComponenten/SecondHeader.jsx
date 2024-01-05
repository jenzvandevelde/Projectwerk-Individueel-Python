import React from 'react';
import { Link } from 'react-router-dom';

const SecondHeader = () => {
  return (
    <div className="shopping">
      <div className="container mt-4">
        <div className="row">
          <div className="col-lg-5 klanten">
            <p className="Klantenopzoeken">Klanten opzoeken</p>
          </div>
          <div className="col-lg-6 klanten">
            <Link to="/createklant" className="Klantentoevoegen">
              + klanten toevoegen
            </Link>
          </div>
          <div className="col-lg-1 right-sidebar"></div>
        </div>
      </div>
    </div>
  );
}

export default SecondHeader;
