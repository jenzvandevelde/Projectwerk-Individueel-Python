import React from 'react';
import { Document, Page, Text, View, StyleSheet, Image, Font } from '@react-pdf/renderer';

// Voeg de Montserrat en Roboto lettertypen toe aan het PDF-document
Font.register({
  family: 'Montserrat',
  fonts: [
    { src: 'https://fonts.gstatic.com/s/montserrat/v15/JTURjIg1_i6t8kCHKm45_bZF3gfD-Px3rCubqg.woff2', fontWeight: 100 },
    { src: 'https://fonts.gstatic.com/s/montserrat/v15/JTURjIg1_i6t8kCHKm45_bZF3gfD-Px3pCubqg.woff2', fontWeight: 200 },
    { src: 'https://fonts.gstatic.com/s/montserrat/v15/JTURjIg1_i6t8kCHKm45_bZF3gfD-Px3vCubqg.woff2', fontWeight: 300 },
    { src: 'https://fonts.gstatic.com/s/montserrat/v15/JTURjIg1_i6t8kCHKm45_bZF3gfD-Px3tCubqg.woff2', fontWeight: 400 },
    { src: 'https://fonts.gstatic.com/s/montserrat/v15/JTURjIg1_i6t8kCHKm45_bZF3gfD-Px3vCubqg.woff2', fontWeight: 500 },
    { src: 'https://fonts.gstatic.com/s/montserrat/v15/JTURjIg1_i6t8kCHKm45_bZF3gfD-Px3sCubqg.woff2', fontWeight: 600 },
  ],
});

Font.register({
  family: 'Roboto',
  fonts: [
    { src: 'https://fonts.gstatic.com/s/roboto/v29/KFOmCnqEu92Fr1Mu4mxK.woff2', fontWeight: 100 },
    { src: 'https://fonts.gstatic.com/s/roboto/v29/KFOmCnqEu92Fr1Mu4WxK.woff2', fontWeight: 300 },
    { src: 'https://fonts.gstatic.com/s/roboto/v29/KFOmCnqEu92Fr1Mu5mxK.woff2', fontWeight: 400 },
    { src: 'https://fonts.gstatic.com/s/roboto/v29/KFOmCnqEu92Fr1Mu7mxK.woff2', fontWeight: 700 },
  ],
});

const FactuurPDF = ({ klantgegevens, geselecteerdeSchijven, recentsteFactuurnummer }) => {
  // Definieer stijlen voor de PDF
  const styles = StyleSheet.create({
    page: {
      width: '210mm',
      height: '297mm',
      margin: 0,
      padding: 0,
      backgroundColor: '#ffffff',
      overflow: 'hidden',
      boxSizing: 'border-box',
      fontFamily: 'Montserrat',
      fontSize: 12,
    },
    invoice: {
      width: '210mm',
      height: '290mm',
      margin: 0,
      marginLeft: 'auto',
      marginRight: 'auto',
      backgroundColor: '#ffffff',
      overflow: 'hidden',
      boxShadow: 'none',
    },
    logorapidpark: {
      width: 100,
      height: 100,
      marginLeft: 50,
      marginTop: 30,
      borderTop: 'none',
    },
    date: {
      marginLeft: 425,
      marginTop: -75,
    },
    invoicenumber: {
      marginLeft: 425,
      marginTop: 15,
    },
    header: {
      fontSize: 20,
      marginBottom: 10,
      fontWeight: 300,
    },
    grayBar: {
      backgroundColor: '#e0e0e0',
      padding: 10,
      marginBottom: 5,
      fontSize: 10,
      maxHeight: 15,
    },
    grayBarFirst: {
      backgroundColor: '#e0e0e0',
      padding: 4,
      marginBottom: 5,
      borderBottom: 'solid 1px black',
      borderTop: 'solid 1px black',
      borderLeft: 'solid 1px black',
      borderRight: 'solid 1px black',
    },
    bedrag: {
      marginLeft: 580,
      marginTop: -27,
      fontWeight: 'bold',
    },
    prijsExtra6: {
      marginTop: -12,
      marginLeft: 575,
    },
    prijsExtra1: {
      marginTop: -12,
      marginLeft: 575,
    },
    prijsExtra2: {
      marginTop: -12,
      marginLeft: 575,
    },
    prijsExtra3: {
      marginTop: -12,
      marginLeft: 575,
    },
    prijsExtra4: {
      marginTop: -12,
      marginLeft: 575,
    },
    prijsExtra5: {
      marginTop: -12,
      marginLeft: 575,
    },
    omschrijving: {
      fontWeight: 'bold',
      marginLeft: 5,
    },
    factuur: {
      marginLeft: 475,
      fontWeight: 'bold',
      fontSize: 25,
      marginTop: -5,
    },
    invoiceInfo: {
      marginBottom: 20,
      display: 'flex',
      justifyContent: 'space-between',
    },
    addresses: {
      marginBottom: 20,
      display: 'flex',
      justifyContent: 'space-between',
    },
    from: {
      width: '48%',
      display: 'inline-block',
      verticalAlign: 'top',
      marginLeft: 50,
      marginRight: -50,
      paddingRight: '2%',
      paddingTop: 25,
    },
    description: {
      marginBottom: 20,
    },
    to: {
      width: '48%',
      display: 'inline-block',
      verticalAlign: 'top',
      marginLeft: 25,
      marginRight: -25,
      paddingTop: 25,
    },
    total: {
      display: 'flex',
      justifyContent: 'space-between',
    },
    left: {
      width: '60%',
      paddingRight: 20,
      boxSizing: 'border-box',
    },
    right: {
      width: '40%',
      boxSizing: 'border-box',
      textAlign: 'right',
    },
    totaal: {
      fontWeight: 'bold',
    },
    footer: {
      marginTop: 20,
      textAlign: 'center',
    },
  });

  return (
    <Document>
      <Page size="A4" style={styles.page}>
        <View style={styles.invoice}>
          <Text style={styles.factuur}>Factuur</Text>
          <Image src="https://jenzvandevelde-images-host.onrender.com/rapidparklogo.png" style={styles.logorapidpark} />
          <Text style={styles.date}>Datum: [DATE]</Text>
          <Text style={styles.invoicenumber}>Factuurnummer: [FACTUURNUMMER]</Text>
          <View style={styles.addresses}>
            <View style={styles.from}>
              <Text>Pontstraat 23</Text>
              <Text>9831 Deurle</Text>
              <Text>Telefoon: 09 333 9000</Text>
              <Text>Email: info@gml-estate.com</Text>
            </View>
            <View style={styles.to}>
              <Text>[NAAM]</Text>
              <Text>[STRAAT] [HUISNUMMER]</Text>
              <Text>[POSTCODE] [STAD]</Text>
              <Text>Telefoon: [TELEFOONNUMMER]</Text>
              <Text>Email: [EMAIL]</Text>
            </View>
          </View>
          <View style={styles.grayBarFirst}>
            <Text style={styles.omschrijving}>Omschrijving</Text>
            <Text style={styles.bedrag}>Bedrag</Text>
          </View>
          <View style={styles.grayBar}>
            [extra1]
            <Text style={styles.prijsExtra1}>[PRIJS_EXTRA1]</Text>
          </View>
          <View style={styles.grayBar}>
            [extra2]
            <Text style={styles.prijsExtra2}>[PRIJS_EXTRA2]</Text>
          </View>
          <View style={styles.grayBar}>
            [extra3]
            <Text style={styles.prijsExtra3}>[PRIJS_EXTRA3]</Text>
          </View>
          <View style={styles.grayBar}>
            [extra4]
            <Text style={styles.prijsExtra4}>[PRIJS_EXTRA4]</Text>
          </View>
          <View style={styles.grayBar}>
            [extra5]
            <Text style={styles.prijsExtra5}>[PRIJS_EXTRA5]</Text>
          </View>
          <View style={styles.grayBar}>
            [extra6]
            <Text style={styles.prijsExtra6}>[PRIJS_EXTRA6]</Text>
          </View>
          <View style={styles.invoiceInfo}>
            <View style={styles.left}>
              <Text>REKENINGNUMMER RAPIDPARK CONSTRUCT BE: 03 0018 9743 5184</Text>
              <Text>Gelieve de factuur te betalen binnen de 15 dagen en de factuurnummer te vermelden bij de betaling</Text>
            </View>
            <View style={styles.right}>
              <Text style={styles.totaal}>TOTAAL: [TOTAAL]</Text>
            </View>
          </View>
          <Text style={styles.footer}>Bij eventuele geschillen zijn de rechtbanken van Gent bevoegd</Text>
        </View>
      </Page>
    </Document>
  );
};

export default FactuurPDF;
