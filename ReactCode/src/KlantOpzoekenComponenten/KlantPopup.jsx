import React from 'react';

const KlantPopup = ({ klant, onClose }) => {
  return (
    <div className="popup-overlay">
      <div className="popup-container">
        <button className="popup-close" onClick={onClose}>X</button>
        <h2>Klantinformatie</h2>
        <div className="klant-info">
          <div className="content">
            <table>
              <tbody>
                {/* First set of rows */}
                <tr>
                  <th>Koper ID</th>
                  <td>{klant.koper_id}</td>
                </tr>
                <tr>
                  <th>GEBOUW</th>
                  <td>{klant.GEBOUW}</td>
                </tr>
                <tr>
                  <th>Prijs</th>
                  <td>{klant.Prijs}</td>
                </tr>
                <tr>
                  <th>Prijs_Constructie</th>
                  <td>{klant.Prijs_Constructie}</td>
                </tr>
                <tr>
                  <th>PARKING</th>
                  <td>{klant.PARKING}</td>
                </tr>
                <tr>
                  <th>Prijs_Parking</th>
                  <td>{klant.Prijs_Parking}</td>
                </tr>
                <tr>
                  <th>Berging</th>
                  <td>{klant.Berging}</td>
                </tr>
                <tr>
                  <th>Prijs_Berging</th>
                  <td>{klant.Prijs_Berging}</td>
                </tr>
              </tbody>
            </table>
          </div>
          <div className="content">
            <table>
              <tbody>
                {/* Second set of rows */}
                <tr>
                  <th>Naam</th>
                  <td>{klant.Naam}</td>
                </tr>
                <tr>
                  <th>Straat</th>
                  <td>{klant.Straat}</td>
                </tr>
                <tr>
                  <th>Huisnummer</th>
                  <td>{klant.Huisnummer}</td>
                </tr>
                <tr>
                  <th>Postcode</th>
                  <td>{klant.Postcode}</td>
                </tr>
                <tr>
                  <th>Stad</th>
                  <td>{klant.Stad}</td>
                </tr>
                <tr>
                  <th>Email</th>
                  <td>{klant.Email}</td>
                </tr>
                <tr>
                  <th>Telefoonnummer</th>
                  <td>{klant.Telefoonnummer}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  );
};

export default KlantPopup;
