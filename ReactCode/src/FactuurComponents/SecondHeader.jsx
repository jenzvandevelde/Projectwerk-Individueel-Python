import React from 'react';

const SecondHeader = () => {
  const openDropboxPage = () => {
    // Open de Dropbox-pagina in een nieuw browservenster/tabblad
    window.open('https://www.dropbox.com/home/Facturen', '_blank');
  };

  return (
    <div className="shopping">
      <div className="container mt-4">
        <div className="row">
          <div className="col-lg-5 klanten">
            <p className="Klantenopzoeken">Facturen Opvragen</p>
          </div>
          <div className="col-lg-6 klanten">
            <button className="Klantentoevoegen brede-knop" onClick={openDropboxPage}>Open Dropbox
            </button>
          </div>
          <div className="col-lg-1 right-sidebar"></div>
        </div>
      </div>
    </div>
  );
}

export default SecondHeader;
