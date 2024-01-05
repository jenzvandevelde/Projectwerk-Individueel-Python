import React, { useState, useEffect } from 'react';
import Searchbalk from './Searchbalk';
import KlantPopup from './KlantPopup';
import Klantadjustmentpopup from './Klantadjustmentpopup'; // Import Klantadjustmentpopup

import '../css/Popup.css';

import CircularProgress from '@material-ui/core/CircularProgress';

const KolomInput = () => {
  const [klanten, setKlanten] = useState([]);
  const [zoekTerm, setZoekTerm] = useState('');
  const [gekozenKlant, setGekozenKlant] = useState(null);
  const [gekozenKlantAdjustment, setGekozenKlantAdjustment] = useState(null); // New state variable for Klantadjustmentpopup
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchKlantenData = async () => {
      try {
        let apiUrl = 'http://127.0.0.1:5000/kopers/alle_klanten';

        if (zoekTerm !== '') {
          apiUrl = `http://127.0.0.1:5000/kopers/zoek_klanten?naam=${zoekTerm}`;
        }

        const response = await fetch(apiUrl);
        const data = await response.json();
        setKlanten(data);
        setLoading(false);
      } catch (error) {
        console.error("Er ging iets mis met het ophalen van klantgegevens", error);
      }
    };

    fetchKlantenData();
  }, [zoekTerm]);

  const openKlantPopup = (klant) => {
    setGekozenKlant(klant);
  };

  const closeKlantPopup = () => {
    setGekozenKlant(null);
  };
  const openKlantadjustmentpopup = (klant) => {
    setGekozenKlantAdjustment(klant);
  };

  const closeKlantadjustmentpopup = () => {
    setGekozenKlantAdjustment(null);
  };

  return (
    <div>
      <Searchbalk onSearch={setZoekTerm} />
      <div className="texttopper">
        <div className="container mt-4">
          <div className="row">
            <div className="col-lg-1 ID">
              <p className="ID">ID</p>
            </div>
            <div className="col-lg-1 Gebouw">
              <p className="Unit">Unit</p>
            </div>
            <div className="col-lg-3 Naam">
              <p className="Name">Naam</p>
            </div>
            <div className="col-lg-4 Email">
              <p className="Mail">Email</p>
            </div>
            <div className="col-lg-1 Telefoonnummer">
              <p className="Phonenumber">Telefoonnummer</p>
            </div>
            <div className="col-lg-1 Moreinfo">
              <p className="Moreinfo"></p>
            </div>
            <div className="col-lg-1 Adjust">
              <p className="Adjust"></p>
            </div>
          </div>
        </div>
      </div>
      <div className="klanten-container">
        {loading ? (
          <div className="loading-container">
            <CircularProgress
              size={24}
              color="#344A63"
            />
            <p className="Loading">Loading</p>
          </div>
        ) : zoekTerm === '' ? (
          klanten.map((klant) => (
            <div className="GreyBox" key={klant.KlantID}>
              <div className="container mt-4">
                <div className="row">
                  <div className="col-lg-1 KlantID">
                    <p className="UserID">{klant.koper_id}</p>
                  </div>
                  <div className="col-lg-1 Gebouw">
                    <p className="Unitnumber">{klant.GEBOUW}</p>
                  </div>
                  <div className="col-lg-3 Name">
                    <p className="UserName">{klant.Naam}</p>
                  </div>
                  <div className="col-lg-4 Email email-container">
                    <a href={`mailto:${klant.Email}`}>{klant.Email}</a>
                  </div>
                  <div className="col-lg-1 telefoonnummer">
                    <a href={`tel:${klant.Telefoonnummer}`}>{klant.Telefoonnummer}</a>
                  </div>
                  <div className="col-lg-1 Symbol button2">
                    <svg
                      fill="none"
                      stroke="currentColor"
                      strokeWidth="1.5"
                      viewBox="0 0 70 70"
                      xmlns="http://www.w3.org/2000/svg"
                      aria-hidden="true"
                      onClick={() => openKlantPopup(klant)}
                    >
                      <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        d="M15.75 6a3.75 3.75 0 11-7.5 0 3.75 3.75 0 017.5 0zM4.501 20.118a7.5 7.5 0 0114.998 0A17.933 17.933 0 0112 21.75c-2.676 0-5.216-.584-7.499-1.632z"
                      ></path>
                    </svg>
                  </div>
                  <div className="col-lg-1 Symbol button3">
                    <svg
                      fill="none"
                      stroke="currentColor"
                      strokeWidth="1.5"
                      viewBox="0 0 70 70"
                      xmlns="http://www.w3.org/2000/svg"
                      aria-hidden="true"
                      onClick={() => openKlantadjustmentpopup(klant)}
                    >
                      <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        d="M10.5 6h9.75M10.5 6a1.5 1.5 0 11-3 0m3 0a1.5 1.5 0 10-3 0M3.75 6H7.5m3 12h9.75m-9.75 0a1.5 1.5 0 01-3 0m3 0a1.5 1.5 0 00-3 0m-3.75 0H7.5m9-6h3.75m-3.75 0a1.5 1.5 0 01-3 0m3 0a1.5 1.5 0 00-3 0m-9.75 0h9.75"
                      ></path>
                    </svg>
                  </div>
                  <div className="col-lg-1">
                    {/* Lege kolom voor witte ruimte rechts */}
                  </div>
                </div>
              </div>
            </div>
          ))
        ) : (
          <p className='noresults'>Geen klanten gevonden</p>
        )}
      </div>
      {gekozenKlant && (
        <KlantPopup klant={gekozenKlant} onClose={closeKlantPopup} />
      )}
      {gekozenKlantAdjustment && (
        <Klantadjustmentpopup klant={gekozenKlantAdjustment} onClose={closeKlantadjustmentpopup} />
      )}
    </div>
  );
};

export default KolomInput;
