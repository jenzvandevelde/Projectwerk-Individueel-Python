import React from 'react'
import SideNavbar from '../KlantOpzoekenComponenten/SideNavbar'
import SecondHeader from '../KlantOpzoekenComponenten/SecondHeader'
import Header from '../KlantOpzoekenComponenten/Header'
import '../css/klantopzoeken.css'; // Het pad naar je CSS-bestand

import KolomInput from '../KlantOpzoekenComponenten/KolomInput';


const KlantOpzoeken = () => {
  return (
    <div className='factuurbody'>
        <SideNavbar/>
        <Header/>
        <SecondHeader/>
        <KolomInput/>
    </div>
  )
}

export default KlantOpzoeken