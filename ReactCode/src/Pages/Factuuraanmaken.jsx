import React from 'react'
import Header from '../FactuurComponents/Header'
import SideNavbar from '../FactuurComponents/SideNavbar'
import SecondHeader from '../FactuurComponents/SecondHeader'
import '../css/style.css'; // Het pad naar je CSS-bestand
import '../css/stylefacturen.css'; // Het pad naar je CSS-bestand

import Searchbalk from '../FactuurComponents/Searchbalk';
import KolomInput from '../FactuurComponents/KolomInput';



const Factuuraanmaken = () => {
  return (
    <div className='factuurbody'>
        
        <Header/>
        <SideNavbar/>
        <SecondHeader/>
        <KolomInput/>

    </div>
  )
}

export default Factuuraanmaken