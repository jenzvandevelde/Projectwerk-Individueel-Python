import React, { useState, useEffect } from 'react';
import Searchbalk from './Searchbalk';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faFilePdf } from '@fortawesome/free-regular-svg-icons';

const KolomInput = () => {
  const [facturen, setFacturen] = useState([]);
  const [zoekTerm, setZoekTerm] = useState('');
  const [gefilterdeFacturen, setGefilterdeFacturen] = useState([]);

  useEffect(() => {
    const fetchFacturenData = async () => {
      try {
        let apiUrl = 'http://127.0.0.1:5000/kopers/alle_facturen';

        const response = await fetch(apiUrl);
        const data = await response.json();

        setFacturen(data);
      } catch (error) {
        console.error("Er ging iets mis met het ophalen van factuurgegevens", error);
      }
    };

    fetchFacturenData();
  }, []);

  useEffect(() => {
    // Filter de facturen op basis van zoekterm
    const filteredFacturen = facturen.filter((factuur) => {
      return (
        factuur.Gebouwnaam.toLowerCase().includes(zoekTerm.toLowerCase()) ||
        factuur.Klantnaam.toLowerCase().includes(zoekTerm.toLowerCase()) ||
        factuur.factuurnummer.includes(zoekTerm) ||
        factuur.koper_id.toString().includes(zoekTerm.toLowerCase()) ||
        factuur.schijf_id.toString().includes(zoekTerm.toLowerCase())
      );
    });

    setGefilterdeFacturen(filteredFacturen);
  }, [zoekTerm, facturen]);

  const openPdfInNewTab = (factuur) => {
    // Construct the URL for opening the PDF with parameters
    const apiUrl = `http://127.0.0.1:5000/open_factuur?factuurnummer=${encodeURIComponent(factuur.factuurnummer)}&klantnaam=${encodeURIComponent(factuur.Klantnaam)}`;
    
    // Open the PDF in a new tab or window
    const pdfWindow = window.open(apiUrl, '_blank');
    
    // Check if the window was successfully opened
    if (pdfWindow) {
      // You can optionally focus the new window/tab
      pdfWindow.focus();
    } else {
      // Handle the case where the window could not be opened (e.g., blocked by pop-up blocker)
      console.error('Kan PDF niet openen. Controleer of pop-upblokkering is uitgeschakeld.');
    }
};

  
  return (
    <div>
      <Searchbalk onSearch={setZoekTerm} />
      <div className="texttopper">
        <div className="container mt-4">
          <div className="row">
            <div className="col-lg-1 Gebouw">
              <p className="Gebouw">Gebouw</p>
            </div>
            <div className="col-lg-3 Naam">
              <p className="Naam">Naam</p>
            </div>
            <div className="col-lg-2 Factuurnummer">
              <p className="Factuurnummer">Factuurnummer</p>
            </div>
            <div className="col-lg-2 Koperid">
              <p className="koper_id">Koper ID</p>
            </div>
            <div className="col-lg-3 Schijfnummer">
              <p className="Schijf_id">Schijf</p>
            </div>
          </div>
        </div>
      </div>
      <div className="klanten-container">
        {gefilterdeFacturen.length > 0 ? (
          gefilterdeFacturen.map((factuur) => (
            <div className="GreyBox" key={factuur.id}>
              <div className="container mt-4">
                <div className="row">
                  <div className="col-lg-1 SelecteKoper">
                    
                  </div>
                  <div className="col-lg-1 Gebouw">
                    <p className="Gebouwnummer">{factuur.Gebouwnaam}</p>
                  </div>
                  <div className="col-lg-3 Name">
                    <p className="UserName">{factuur.Klantnaam}</p>
                  </div>
                  <div className="col-lg-3 Factuurnummer">
                    <p className="Factuurnummerkoper">{factuur.factuurnummer}</p>
                  </div>
                  <div className="col-lg-2 Koperid">
                    <p className="Userid">{factuur.koper_id}</p>
                  </div>
                  <div className="col-lg-1 Schijfid">
                    <p className="Schijfid">{factuur.schijf_id}</p>
                  </div>
                  <div className="col-lg-1" onClick={() => openPdfInNewTab(factuur)}>
                    <div className="pdf-button">
                      <FontAwesomeIcon icon={faFilePdf} className="pdf-icon" />
                    </div>
                  </div>
                </div>
              </div>
            </div>
          ))
        ) : (
          <p className='geenfacturen'>Geen facturen gevonden</p>
        )}
      </div>
    </div>
  );
};

export default KolomInput;
