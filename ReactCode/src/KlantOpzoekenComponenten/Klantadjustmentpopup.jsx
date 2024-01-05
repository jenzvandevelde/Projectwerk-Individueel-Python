import React, { useState } from 'react';
import StylescssPopup from '../css/Popup.module.css';

const Klantadjustmentpopup = ({ klant, onClose }) => {
  // Create state variables for each field to track changes
  const [koperId, setKoperId] = useState(klant.koper_id);
  const [gebouw, setGebouw] = useState(klant.GEBOUW);
  const [prijs, setPrijs] = useState(klant.Prijs);
  const [prijsConstructie, setPrijsConstructie] = useState(klant.Prijs_Constructie);
  const [parking, setParking] = useState(klant.PARKING);
  const [prijsParking, setPrijsParking] = useState(klant.Prijs_Parking);
  const [berging, setBerging] = useState(klant.Berging);
  const [prijsBerging, setPrijsBerging] = useState(klant.Prijs_Berging);
  const [naam, setNaam] = useState(klant.Naam);
  const [straat, setStraat] = useState(klant.Straat);
  const [huisnummer, setHuisnummer] = useState(klant.Huisnummer);
  const [postcode, setPostcode] = useState(klant.Postcode);
  const [stad, setStad] = useState(klant.Stad);
  const [email, setEmail] = useState(klant.Email);
  const [telefoonnummer, setTelefoonnummer] = useState(klant.Telefoonnummer);

  // Create state variable to manage the success message
  const [saveSuccess, setSaveSuccess] = useState(false);

  // Function to handle the "Opslaan" button click
  const handleOpslaanClick = async () => {
    // Create a JSON object with the updated data
    const updatedData = {
      koper_id: koperId,
      GEBOUW: gebouw,
      Prijs: prijs,
      Prijs_Constructie: prijsConstructie,
      PARKING: parking,
      Prijs_Parking: prijsParking,
      Berging: berging,
      Prijs_Berging: prijsBerging,
      Naam: naam,
      Straat: straat,
      Huisnummer: huisnummer,
      Postcode: postcode,
      Stad: stad,
      Email: email,
      Telefoonnummer: telefoonnummer,
    };

    try {
      // Make a PUT request to your API endpoint
      const response = await fetch('http://127.0.0.1:5000/update_customer', {
        method: 'PUT', // Use PUT since you are updating data
        headers: {
          'Content-Type': 'application/json', // Specify the content type as JSON
        },
        body: JSON.stringify(updatedData), // Send the JSON data in the request body
      });

      if (response.ok) {
        // Handle the success response here (e.g., display a success message)
        setSaveSuccess(true); // Set saveSuccess to true
        console.log('Data updated successfully');

        // Reload the page after a successful update
        window.location.reload();
      } else {
        // Handle the error response here (e.g., display an error message)
        console.error('Error updating data');
      }
    } catch (error) {
      // Handle any network or other errors here
      console.error('Error:', error);
    }
  };

  return (
    <div className={StylescssPopup.popupOverlay}>
      <div className={StylescssPopup.popupContainer}>
        <div className={StylescssPopup.closebutton}>
          <button className={StylescssPopup.popupClose} onClick={onClose}>
            X
          </button>
        </div>
        <h2 className={StylescssPopup.popupTitle}>Klantinformatie</h2>
        {saveSuccess && (
          <div className={StylescssPopup.successMessage}>Opslaan gelukt!</div>
        )}
        <div className={StylescssPopup.klantInfo}>
          <div className={StylescssPopup.content}>
            <table className={StylescssPopup.popupTable}>
              <tbody>
                <tr>
                  <th>Koper ID</th>
                  <td>
                    <input
                      type="text"
                      value={koperId}
                      onChange={(e) => setKoperId(e.target.value)}
                    />
                  </td>
                </tr>
                <tr>
                  <th>GEBOUW</th>
                  <td>
                    <input
                      type="text"
                      value={gebouw}
                      onChange={(e) => setGebouw(e.target.value)}
                    />
                  </td>
                </tr>
                <tr>
                  <th>Prijs</th>
                  <td>
                    <input
                      type="text"
                      value={prijs}
                      onChange={(e) => setPrijs(e.target.value)}
                    />
                  </td>
                </tr>
                <tr>
                  <th>Prijs_Constructie</th>
                  <td>
                    <input
                      type="text"
                      value={prijsConstructie}
                      onChange={(e) => setPrijsConstructie(e.target.value)}
                    />
                  </td>
                </tr>
                <tr>
                  <th>PARKING</th>
                  <td>
                    <input
                      type="text"
                      value={parking}
                      onChange={(e) => setParking(e.target.value)}
                    />
                  </td>
                </tr>
                <tr>
                  <th>Prijs_Parking</th>
                  <td>
                    <input
                      type="text"
                      value={prijsParking}
                      onChange={(e) => setPrijsParking(e.target.value)}
                    />
                  </td>
                </tr>
                <tr>
                  <th>Berging</th>
                  <td>
                    <input
                      type="text"
                      value={berging}
                      onChange={(e) => setBerging(e.target.value)}
                    />
                  </td>
                </tr>
                <tr>
                  <th>Prijs_Berging</th>
                  <td>
                    <input
                      type="text"
                      value={prijsBerging}
                      onChange={(e) => setPrijsBerging(e.target.value)}
                    />
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
          <div className={StylescssPopup.content}>
            <table className={StylescssPopup.popupTable}>
              <tbody>
                <tr>
                  <th>Naam</th>
                  <td>
                    <input
                      type="text"
                      value={naam}
                      onChange={(e) => setNaam(e.target.value)}
                    />
                  </td>
                </tr>
                <tr>
                  <th>Straat</th>
                  <td>
                    <input
                      type="text"
                      value={straat}
                      onChange={(e) => setStraat(e.target.value)}
                    />
                  </td>
                </tr>
                <tr>
                  <th>Huisnummer</th>
                  <td>
                    <input
                      type="text"
                      value={huisnummer}
                      onChange={(e) => setHuisnummer(e.target.value)}
                    />
                  </td>
                </tr>
                <tr>
                  <th>Postcode</th>
                  <td>
                    <input
                      type="text"
                      value={postcode}
                      onChange={(e) => setPostcode(e.target.value)}
                    />
                  </td>
                </tr>
                <tr>
                  <th>Stad</th>
                  <td>
                    <input
                      type="text"
                      value={stad}
                      onChange={(e) => setStad(e.target.value)}
                    />
                  </td>
                </tr>
                <tr>
                  <th>Email</th>
                  <td>
                    <input
                      type="text"
                      value={email}
                      onChange={(e) => setEmail(e.target.value)}
                    />
                  </td>
                </tr>
                <tr>
                  <th>Telefoonnummer</th>
                  <td>
                    <input
                      type="text"
                      value={telefoonnummer}
                      onChange={(e) => setTelefoonnummer(e.target.value)}
                    />
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
          <div className={StylescssPopup.actionButtonContainer}>
            <button className={StylescssPopup.actionButton} onClick={handleOpslaanClick}>
              Opslaan
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Klantadjustmentpopup;
