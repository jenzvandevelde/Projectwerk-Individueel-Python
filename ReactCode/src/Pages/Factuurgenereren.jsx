import React from 'react'
import SideNavbar from '../FactuurGenereren/SideNavbar'
import Header from '../FactuurGenereren/Header'
import Vragenlijst from '../FactuurGenereren/Vragenlijst'
import '../assets/Factuurgenereren.css'
import Searchbalk from '../KlantOpzoekenComponenten/Searchbalk'
import Knoppen from '../FactuurGenereren/Knoppen'

const Factuurgenereren = () => {
  return (
    <div className='factuurbody'>
        <SideNavbar/>
        <Header/>
        <Vragenlijst/>
    </div>
  )
}

export default Factuurgenereren