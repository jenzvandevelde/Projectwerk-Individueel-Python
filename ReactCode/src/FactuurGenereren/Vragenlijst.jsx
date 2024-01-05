import React, { useState, useEffect } from 'react';
import { createRoot } from 'react-dom/client';

import CircularProgress from "@material-ui/core/CircularProgress";

const Searchbalk = ({ onSearch }) => {
  const [zoekTerm, setZoekTerm] = useState('');

  const handleSearch = () => {
    onSearch(zoekTerm);
  };

  return (
    <div className="Searchbalk Searchbalk-factuur">
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
            Zoek
          </button>
        </div>
      </div>
    </div>
  );
};

const Vragenlijst = () => {
  const [klantgegevens, setKlantgegevens] = useState(null);
  const [klantGevonden, setKlantGevonden] = useState(false);
  const [geselecteerdeSchijven, setGeselecteerdeSchijven] = useState([]);
  const [factuurnummer, setFactuurnummer] = useState(''); // Voeg factuurnummer state toe
  const [schijven, setSchijven] = useState([]);
  const [recentsteFactuurnummer, setRecentsteFactuurnummer] = useState('');
  const [factuurAangemaakt, setFactuurAangemaakt] = useState(false);
  const [timer, setTimer] = useState(null);
  const [recentsteFactuurnummerLoaded, setRecentsteFactuurnummerLoaded] = useState(false);

  const zoekKlant = async (zoekterm) => {
    try {
      const response = await fetch(`http://127.0.0.1:5000/kopers/zoek_klanten?naam=${zoekterm}`);
      if (!response.ok) {
        throw new Error('Kan klantgegevens niet ophalen');
      }
      const data = await response.json();
      if (data.length > 0) {
        setKlantgegevens(data[0]);
        setKlantGevonden(true);
      } else {
        setKlantgegevens(null);
        setKlantGevonden(false);
      }
    } catch (error) {
      console.error('Fout bij het ophalen van klantgegevens:', error);
    }
  };

  useEffect(() => {
    zoekKlant('');
  }, []);

  const handleFactuurMaken = async () => {
    try {
      const response = await fetch('http://127.0.0.1:5000/facturen/maak_factuur', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          schijven: geselecteerdeSchijven,
          factuurnummer: factuurnummer, // Gebruik het ingevulde factuurnummer
          naam: klantgegevens ? klantgegevens.Naam : '',
        }),
      });

      if (response.ok) {
        console.log('Factuur succesvol aangemaakt');
        setFactuurAangemaakt(true);
        const refreshTimer = setTimeout(() => {
          window.location.reload();
        }, 3000);
        setTimer(refreshTimer);
      } else {
        throw new Error('Fout bij het maken van de factuur');
      }
    } catch (error) {
      console.error('Fout bij het maken van de factuur:', error);
    }
  };

  useEffect(() => {
    return () => {
      if (timer) {
        clearTimeout(timer);
      }
    };
  }, [timer]);

  useEffect(() => {
    async function fetchSchijven() {
      try {
        const response = await fetch('http://127.0.0.1:5000/kopers/alle_schijven');
        const data = await response.json();
        setSchijven(data);
      } catch (error) {
        console.error('Er is een fout opgetreden bij het ophalen van de schijven:', error);
      }
    }

    fetchSchijven();
  }, []);

  useEffect(() => {
    async function fetchRecentsteFactuurnummer() {
      try {
        const response = await fetch('http://127.0.0.1:5000/recentste_factuurnummer');
        if (!response.ok) {
          throw  new Error('Fout bij het ophalen van het recentste factuurnummer');
        }
        const data = await response.json();
        setRecentsteFactuurnummer(data.recentste_factuurnummer);
      } catch (error) {
        console.error('Fout bij het ophalen van het recentste factuurnummer:', error);
      }
    }

    fetchRecentsteFactuurnummer();
  }, []);

  return (
    <div>
      {factuurAangemaakt && (
        <div className="alert alert-success" role="alert">
          Factuur succesvol aangemaakt! Deze pagina wordt na 3 seconden vernieuwd.
        </div>
      )}
      <Searchbalk onSearch={zoekKlant} />
      <div className="container-klantgegevens">
        {klantGevonden ? (
          <div className="row">
            <div className="col-md-6 klantshowup">
              <p className="klantgegevens">Klantgegevens</p>
              
              <div id="klantgegevens">
                <p>
                  <strong>Naam:</strong> {klantgegevens ? klantgegevens.Naam : ''}
                </p>
                <p>
                  <strong>Gebouw:</strong> {klantgegevens ? klantgegevens.GEBOUW : ''}
                </p>
                <p>
                  <strong>Straat:</strong> {klantgegevens ? klantgegevens.Straat : ''}
                </p>
                <p>
                  <strong>Huisnummer:</strong> {klantgegevens ? klantgegevens.Huisnummer : ''}
                </p>
              </div>
            </div>
            <div className="col-md-6 klantshowup">
              <p className="klantgegevens">Klantgegevens</p>
              <div id="klantgegevens">
                <p>
                  <strong>Postcode:</strong> {klantgegevens ? klantgegevens.Postcode : ''}
                </p>
                <p>
                  <strong>Stad:</strong> {klantgegevens ? klantgegevens.Stad : ''}
                </p>
                <p>
                  <strong>Email:</strong> {klantgegevens ? klantgegevens.Email : ''}
                </p>
                <p>
                  <strong>Telefoonnummer:</strong> {klantgegevens ? klantgegevens.Telefoonnummer : ''}
                </p>
              </div>
            </div>
          </div>
        ) : null}
      </div>

      <div className="container">
        <div className="row">
          <div className="col-md-6">
            <form id="vragenForm">
              <div className="vraag">
                <label htmlFor="schijven">Welke schijven wilt u toevoegen?</label>
                <div id="schijven">
                  <div className="scrollable-checkboxes">
                    {schijven.map((schijf) => (
                      <div key={schijf.schijf_id} className="checkbox-item">
                        <input type="checkbox" id={`schijf${schijf.schijf_id}`} name="schijf" value={schijf.schijf_id} onChange={(e) => {
                          if (e.target.checked) {
                            setGeselecteerdeSchijven([...geselecteerdeSchijven, schijf.schijf_id]);
                          } else {
                            setGeselecteerdeSchijven(geselecteerdeSchijven.filter((id) => id !== schijf.schijf_id));
                          }
                        }} />
                        <label htmlFor={`schijf${schijf.schijf_id}`}>{schijf.naam}</label>
                        <p className="schijf-omschrijving">{schijf.Omschrijving}</p>
                        <span className="opmerking">{schijf.Opmerking}</span>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            </form>
          </div>
          <div className="col-md-6 factuurnummer">
            <div className="vraag1">
              <label htmlFor="recentsteFactuur">Het recentste factuurnummer is:
                <span id="recentsteFactuur">{recentsteFactuurnummer}</span>
              </label>
            </div>
            <div className="vraag2">
              <label htmlFor="factuurNummer">Voer uw factuurnummer in:</label>
              <input type="text" id="factuurNummer" name="factuurNummer" value={factuurnummer} onChange={(e) => setFactuurnummer(e.target.value)} />
            </div>
          </div>
        </div>
      </div>
      <div className="container buttons">
        <div className="row">
          <div className="col-md-6">
            <button className="btn FactuurMaken" onClick={handleFactuurMaken}>
              Factuur Maken
            </button>
          </div>
        </div>
      </div>

      
    </div>
  );
};

export default Vragenlijst;
