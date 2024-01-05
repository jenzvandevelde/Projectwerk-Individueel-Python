import React, { useState } from 'react';
import StylescssCreateklant from '../css/Createklant.module.css';

const CreateNewKlant = () => {
  const initialFormData = {
    koperId: '',
    gebouw: '',
    prijs: '',
    prijsConstructie: '',
    parking: '',
    prijsParking: '',
    berging: '',
    prijsBerging: '',
    naam: '',
    straat: '',
    huisnummer: '',
    postcode: '',
    stad: '',
    email: '',
    telefoonnummer: '',
  };

  const [formData, setFormData] = useState(initialFormData);
  const [saveSuccess, setSaveSuccess] = useState(false);
  const [error, setError] = useState(null);

  const handleFieldChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  const handleOpslaanClick = async () => {
    try {
      // Validation
      if (!formData.email || !formData.email.includes('@')) {
        setError ('Vul een geldig mail adres in');
        setSaveSuccess(false);
        return;
      }

      // Create the JSON object with the specific keys
      const newCustomerData = {
        "Berging": formData.berging,
        "Email": formData.email,
        "GEBOUW": formData.gebouw,
        "Huisnummer": formData.huisnummer,
        "Naam": formData.naam,
        "PARKING": formData.parking,
        "Postcode": formData.postcode,
        "Prijs": formData.prijs,
        "Prijs_Berging": formData.prijsBerging,
        "Prijs_Constructie": formData.prijsConstructie,
        "Prijs_Parking": formData.prijsParking,
        "Stad": formData.stad,
        "Straat": formData.straat,
        "Telefoonnummer": formData.telefoonnummer
      };

      // Make a POST request to your API endpoint
      const response = await fetch('http://127.0.0.1:5000/create_customer', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(newCustomerData),
      });

      if (response.ok) {
        setSaveSuccess(true);
        setError(null);
        setFormData(initialFormData); // Reset form fields

        // Automatically remove the success message after 5 seconds
        setTimeout(() => {
          setSaveSuccess(false);
        }, 5000);
      } else {
        const data = await response.json();
        setError(data.error || 'Error creating customer');
        setSaveSuccess(false);
      }
    } catch (error) {
      setError('Network error');
      setSaveSuccess(false);
    }
  };


  return (
    <div className={StylescssCreateklant.createklantForm}>
      <h2 className={StylescssCreateklant.popupTitle}>Klantinformatie</h2>
      {saveSuccess && (
        <div className={StylescssCreateklant.successMessage}>
          Klant aangemaakt!{' '}
        </div>
      )}
      {error && <div className={StylescssCreateklant.errorMessage}>{error}</div>}
      <div className={StylescssCreateklant.klantInfo}>
        <div className={StylescssCreateklant.content}>
          <table className={StylescssCreateklant.popupTable}>
            <tbody>
              <tr>
                <th>GEBOUW</th>
                <td>
                  <input
                    type="text"
                    name="gebouw"
                    value={formData.gebouw}
                    onChange={handleFieldChange}
                  />
                </td>
              </tr>
              <tr>
                <th>Prijs</th>
                <td>
                  <input
                    type="text"
                    name="prijs"
                    value={formData.prijs}
                    onChange={handleFieldChange}
                  />
                </td>
              </tr>
              <tr>
                <th>Prijs_Constructie</th>
                <td>
                  <input
                    type="text"
                    name="prijsConstructie"
                    value={formData.prijsConstructie}
                    onChange={handleFieldChange}
                  />
                </td>
              </tr>
              <tr>
                <th>PARKING</th>
                <td>
                  <input
                    type="text"
                    name="parking"
                    value={formData.parking}
                    onChange={handleFieldChange}
                  />
                </td>
              </tr>
              <tr>
                <th>Prijs_Parking</th>
                <td>
                  <input
                    type="text"
                    name="prijsParking"
                    value={formData.prijsParking}
                    onChange={handleFieldChange}
                  />
                </td>
              </tr>
              <tr>
                <th>Berging</th>
                <td>
                  <input
                    type="text"
                    name="berging"
                    value={formData.berging}
                    onChange={handleFieldChange}
                  />
                </td>
              </tr>
              <tr>
                <th>Prijs_Berging</th>
                <td>
                  <input
                    type="text"
                    name="prijsBerging"
                    value={formData.prijsBerging}
                    onChange={handleFieldChange}
                  />
                </td>
              </tr>
            </tbody>
          </table>
        </div>
        <div className={StylescssCreateklant.content}>
          <table className={StylescssCreateklant.popupTable}>
            <tbody>
              <tr>
                <th>Naam</th>
                <td>
                  <input
                    type="text"
                    name="naam"
                    value={formData.naam}
                    onChange={handleFieldChange}
                  />
                </td>
              </tr>
              <tr>
                <th>Straat</th>
                <td>
                  <input
                    type="text"
                    name="straat"
                    value={formData.straat}
                    onChange={handleFieldChange}
                  />
                </td>
              </tr>
              <tr>
                <th>Huisnummer</th>
                <td>
                  <input
                    type="text"
                    name="huisnummer"
                    value={formData.huisnummer}
                    onChange={handleFieldChange}
                  />
                </td>
              </tr>
              <tr>
                <th>Postcode</th>
                <td>
                  <input
                    type="text"
                    name="postcode"
                    value={formData.postcode}
                    onChange={handleFieldChange}
                  />
                </td>
              </tr>
              <tr>
                <th>Stad</th>
                <td>
                  <input
                    type="text"
                    name="stad"
                    value={formData.stad}
                    onChange={handleFieldChange}
                  />
                </td>
              </tr>
              <tr>
                <th>Email</th>
                <td>
                  <input
                    type="text"
                    name="email"
                    value={formData.email}
                    onChange={handleFieldChange}
                  />
                </td>
              </tr>
              <tr>
                <th>Telefoonnummer</th>
                <td>
                  <input
                    type="text"
                    name="telefoonnummer"
                    value={formData.telefoonnummer}
                    onChange={handleFieldChange}
                  />
                </td>
              </tr>
            </tbody>
          </table>
        </div>
        <div className={StylescssCreateklant.actionButtonContainer}>
          <button className={StylescssCreateklant.actionButton} onClick={handleOpslaanClick}>
            Opslaan
          </button>
        </div>
      </div>
    </div>
  );
};

export default CreateNewKlant;
