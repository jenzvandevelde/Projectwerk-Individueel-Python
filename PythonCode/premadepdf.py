import json
import pdfkit
from datetime import datetime
import locale
import os
import pyodbc

# Stel locale-instellingen in voor getalnotatie
locale.setlocale(locale.LC_ALL, 'nl_NL.UTF-8')  # Gebruik de Nederlandse notatie

# Configuratie voor SQL Server-verbinding
# Vervang de onderstaande verbindingssnaren door je eigen gegevens
server = '78.22.195.15,1433'
database = 'python'
username = 'Sa'
password = 'Mylo1621'

connection_string_sql_server = f"DRIVER=ODBC Driver 17 for SQL Server;SERVER={server};DATABASE={database};UID={username};PWD={password}"
connection_sql_server = pyodbc.connect(connection_string_sql_server)
cursor_sql_server = connection_sql_server.cursor()

# Specificeer het pad naar wkhtmltopdf
pdfkit_config = pdfkit.configuration(wkhtmltopdf=r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe')

# JSON-data met de gegeven gegevens
input_json = '''
{
  "schijven": [1],
  "factuurnummer": "36",
  "naam": "Van Havere - De Smedt"
}
'''

# JSON-data omzetten naar een Python-dictionary
factuur_data = json.loads(input_json)

def formatteer_bedrag(bedrag):
    return locale.format_string("%.2f", bedrag, grouping=True)

def haal_klantgegevens_op_en_genereer_pdf(factuur_data, cursor_sql_server):
    try:
        naam = factuur_data["naam"]  # Haal de naam als een string op
        schijfnummers = factuur_data["schijven"]
        factuurnummer = factuur_data["factuurnummer"]

        # Haal klantgegevens op uit de database op basis van de opgegeven naam
        query = "SELECT * FROM kopers WHERE naam = ?"
        cursor_sql_server.execute(query, (naam,))
        resultaat = cursor_sql_server.fetchone()

        if resultaat:
            klantgegevens = {
                "naam": resultaat[8],  # Index 1 bevat de klantnaam
                "straat": resultaat[9],
                "huisnummer": resultaat[10],
                "postcode": resultaat[11],
                "stad": resultaat[12],
                "email": resultaat[13],
                "telefoonnummer": resultaat[14],
                "prijs": float(resultaat[3])  # Haal de prijs uit de kolom "Prijs_Constructie"
            }

            current_date = datetime.now().strftime('%d/%m/%Y')

            # Lees de inhoud van het externe HTML-bestand
            with open("testing.html", "r") as html_file:
                html_sjabloon = html_file.read()

            # Hier wordt de naam van de factuur gegenereerd met factuurnummer en klantnaam
            factuur_naam = f"{factuurnummer} - {klantgegevens['naam']}"

            # Genereer de PDF met de naam in het formaat "factuurnummer - klantnaam.pdf"
            pdf_naam = os.path.join(r"C:\Users\jensvandevelde\Desktop\Pythonprogram\Facturen", f"{factuur_naam}.pdf")

            # Vervang de placeholders in het HTML-sjabloon door de klantgegevens
            for variabele, waarde in klantgegevens.items():
                placeholder = f"[{variabele.upper()}]"
                html_sjabloon = html_sjabloon.replace(placeholder, str(waarde))

            # Vervang ook de factuurnummer-placeholder door het factuurnummer
            html_sjabloon = html_sjabloon.replace("[FACTUURNUMMER]", factuurnummer)
            html_sjabloon = html_sjabloon.replace("[DATE]", current_date)

            # Leegmaken van alle schijf placeholders
            for i in range(1, 11):
                html_sjabloon = html_sjabloon.replace(f"[SCHIJF{i}]", "")
                html_sjabloon = html_sjabloon.replace(f"[PRIJS{i}]", "")

            # Voeg schijfgegevens toe aan de HTML-sjabloon voor de geselecteerde schijven
            huidige_extra_index = 1
            schijf_count = len(schijfnummers)

            for schijf in schijfnummers:
                opmerking_query = "SELECT Percentage, Opmerking FROM Schijven WHERE schijf_id = ?"
                cursor_sql_server.execute(opmerking_query, (schijf,))
                opmerking_result = cursor_sql_server.fetchone()

                if opmerking_result:
                    percentage_db, opmerking = opmerking_result
                    prijs = klantgegevens["prijs"] * (percentage_db / 100.0)

                    # Voeg het euroteken (€) toe aan het prijsbedrag
                    prijs_met_euroteken = f"€ {formatteer_bedrag(prijs)}"

                    # Vervang de omschrijving en prijs placeholders voor de huidige schijf
                    html_sjabloon = html_sjabloon.replace(f"[extra{huidige_extra_index}]", str(opmerking))
                    html_sjabloon = html_sjabloon.replace(f"[PRIJS_EXTRA{huidige_extra_index}]", prijs_met_euroteken)

                    # Update de index voor de volgende extra
                    huidige_extra_index += 1

            # Als er minder dan 5 schijven zijn, maak de rest van de extras leeg
            for i in range(7):
                if i >= schijf_count:
                    html_sjabloon = html_sjabloon.replace(f"[extra{i}]", "")
                    html_sjabloon = html_sjabloon.replace(f"[PRIJS_EXTRA{i}]", "")

            # Bereken de prijzen en vul de juiste schijf in
            subtotaal = 0.0
            for schijf in schijfnummers:
                opmerking_query = "SELECT Percentage FROM Schijven WHERE schijf_id = ?"
                cursor_sql_server.execute(opmerking_query, (schijf,))
                percentage_db = cursor_sql_server.fetchone()[0]
                prijs = klantgegevens["prijs"] * (percentage_db / 100.0)
                subtotaal += prijs
                html_sjabloon = html_sjabloon.replace(f"[SCHIJF{schijf}]", f"Schijf {schijf}")
                html_sjabloon = html_sjabloon.replace(f"[PRIJS{schijf}]", formatteer_bedrag(prijs))

            btw_percentage = 0.21
            btw = subtotaal * btw_percentage
            totaal = subtotaal + btw

            # Voeg het euroteken (€) toe aan de SUBTOTAAL, BTW en TOTAAL bedragen
            subtotaal_omschrijving = f"€ {formatteer_bedrag(subtotaal)}"
            btw_omschrijving = f"€ {formatteer_bedrag(btw)}"
            totaal_omschrijving = f"€ {formatteer_bedrag(totaal)}"

            # Vervang de subtotaal, btw en totaal placeholders
            html_sjabloon = html_sjabloon.replace("[SUBTOTAAL]", subtotaal_omschrijving)
            html_sjabloon = html_sjabloon.replace("[BTW]", btw_omschrijving)
            html_sjabloon = html_sjabloon.replace("[TOTAAL]", totaal_omschrijving)

             # Genereer de PDF met de juiste naam
            pdfkit.from_string(html_sjabloon, pdf_naam, configuration=pdfkit_config)

            print(f"De PDF '{pdf_naam}' is succesvol aangemaakt.")

        else:
            print("Er zijn geen klanten gevonden met de opgegeven naam.")
    except Exception as e:
        print(f"Fout bij het genereren van de factuur: {str(e)}")
    finally:
        connection_sql_server.close()

if __name__ == "__main__":
    haal_klantgegevens_op_en_genereer_pdf(factuur_data, cursor_sql_server)
