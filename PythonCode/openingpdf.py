import os

def open_pdf_by_number_and_name():
    # Vraag om het factuurnummer en de klantnaam
    factuurnummer = input("Voer het factuurnummer in: ")
    klantnaam = input("Voer de klantnaam in: ")

    # Genereer de bestandsnaam op basis van factuurnummer en klantnaam
    pdf_filename = f"{factuurnummer} - {klantnaam}.pdf"
    pdf_path = os.path.join("C:\\Users\\jensvandevelde\\Desktop\\Pythonprogram\\Facturen", pdf_filename)

    # Controleer of het PDF-bestand bestaat
    if os.path.exists(pdf_path):
        try:
            # Plaats het PDF-pad tussen dubbele aanhalingstekens om spaties te behandelen
            os.system(f'"{pdf_path}"')
            print(f"PDF-bestand '{pdf_filename}' is geopend.")
        except Exception as e:
            print(f"Fout bij het openen van het PDF-bestand: {e}")
    else:
        print(f"PDF-bestand '{pdf_filename}' niet gevonden.")

if __name__ == "__main__":
    open_pdf_by_number_and_name()
