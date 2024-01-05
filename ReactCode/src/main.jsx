import React from 'react';
import ReactDOM from 'react-dom';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import KlantOpzoeken from './Pages/KlantOpzoeken';
import Factuuraanmaken from './Pages/Factuuraanmaken';
import './index.css';
import Factuurgenereren from './Pages/Factuurgenereren';
import Createklant from './Pages/Createklant';

const AppRouter = () => (
  <BrowserRouter>
    <Routes>
    <Route path="/" element={<KlantOpzoeken />} />

      <Route path="KlantOpzoeken" element={<KlantOpzoeken />} />
      <Route path="/factuurgenereren" element={<Factuuraanmaken />} />
      <Route path="/factuuraanmaken" element={<Factuurgenereren />} />
      <Route path="/Createklant" element={<Createklant />} />


      {/* Voeg hier andere routes toe voor je andere pagina's */}
    </Routes>
  </BrowserRouter>
);

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <AppRouter />
  </React.StrictMode>
);
