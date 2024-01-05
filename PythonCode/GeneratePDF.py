import pdfkit
from datetime import datetime
import locale
import os
import pyodbc
from database_config import connection_string_azure_sql_edge


# Stel locale-instellingen in voor getalnotatie
locale.setlocale(locale.LC_ALL, 'nl_NL.UTF-8')  # Gebruik de Nederlandse notatie

# Configuratie voor SQL Server-verbinding
# Connect to the SQL Server database using the provided connection string from database_config.py
connection = pyodbc.connect(connection_string_azure_sql_edge)
cursor = connection.cursor()


# Specificeer het pad naar wkhtmltopdf
pdfkit_config = pdfkit.configuration(
    wkhtmltopdf=r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe')



def vraag_schijf_nummers():
    schijfnummers = []
    while True:
        schijf_toevoegen = input("Wilt u een schijf toevoegen? (ja/nee): ").lower()
        if schijf_toevoegen == 'ja':
            schijf_nummer = int(input("Voer het schijfnummer in (1 t/m 10): "))
            if 1 <= schijf_nummer <= 10:
                schijfnummers.append(schijf_nummer)
            else:
                print("Ongeldig schijfnummer. Voer een schijfnummer tussen 1 en 10 in.")
        elif schijf_toevoegen == 'nee':
            break
    return schijfnummers

def haal_schijf_informatie_op(schijfnummers, cursor_sql_server):
    selected_schijven = {}
    for nummer in schijfnummers:
        query = "SELECT Percentage FROM Schijven WHERE schijf_id = ?"
        cursor_sql_server.execute(query, (nummer,))
        resultaat = cursor_sql_server.fetchone()
        if resultaat:
            selected_schijven[nummer] = resultaat[0]
        else:
            print(f"Geen informatie gevonden voor schijf {nummer}.")
    return selected_schijven

def formatteer_bedrag(bedrag):
    return locale.format_string("%.2f", bedrag, grouping=True)

def sla_factuur_op_in_database(factuurnummer, koper_id, schijf_id_list, cursor_sql_server, connection_sql_server):
    try:
        for schijf_id in schijf_id_list:
            insert_query = "INSERT INTO facturen (factuurnummer, koper_id, schijf_id) VALUES (?, ?, ?)"
            cursor_sql_server.execute(insert_query, (factuurnummer, koper_id, schijf_id))
        
        connection_sql_server.commit()
        print("Factuur succesvol opgeslagen in de database.")
    except pyodbc.Error as err_sql_server:
        print(f"Fout bij het opslaan van de factuur in de database: {err_sql_server}")

def genereer_factuurnummer(cursor_sql_server):
    try:
        while True:
            cursor_sql_server.execute("SELECT MAX(factuurnummer) FROM facturen")
            laatste_factuurnummer = cursor_sql_server.fetchone()[0]

            if laatste_factuurnummer is not None:
                print(f"Het laatst gebruikte factuurnummer is: {laatste_factuurnummer}")
                nieuw_factuurnummer = input("Voer het nieuwe factuurnummer in: ")

                # Controleer of het ingevoerde factuurnummer al bestaat in de database
                cursor_sql_server.execute("SELECT factuurnummer FROM facturen WHERE factuurnummer = ?", (nieuw_factuurnummer,))
                bestaat_al = cursor_sql_server.fetchone()

                if not bestaat_al:
                    return nieuw_factuurnummer
                else:
                    print("Dit factuurnummer bestaat al. Kies een ander factuurnummer.")
            else:
                nieuw_factuurnummer = input("Voer het factuurnummer in: ")
                return nieuw_factuurnummer
    except pyodbc.Error as err_sql_server:
        print(f"Fout bij het ophalen van het laatste factuurnummer: {err_sql_server}")

def haal_klantgegevens_op_en_genereer_pdf(partial_naam, selected_schijven, cursor_sql_server):
    try:
        query = "SELECT * FROM kopers WHERE LOWER(Naam) LIKE LOWER(?)"
        cursor_sql_server.execute(query, ("%" + partial_naam + "%",))
        resultaat = cursor_sql_server.fetchone()

        if resultaat:
            klantgegevens = {
                "naam": resultaat[8],  # Index 8 bevat de klantnaam
                "straat": resultaat[9],
                "huisnummer": resultaat[10],
                "postcode": resultaat[11],
                "stad": resultaat[12],
                "email": resultaat[13],
                "telefoonnummer": resultaat[14],
                "prijs": float(resultaat[3])  # Haal de prijs uit de kolom "Prijs_Constructie"
            }

            current_date = datetime.now().strftime('%d/%m/%Y')

            # Gebruik de functie om een factuurnummer te genereren of in te voeren
            factuurnummer = genereer_factuurnummer(cursor_sql_server)

            # Lees de inhoud van het externe HTML-bestand
            with open("testing.html", "r") as html_file:
                html_sjabloon = html_file.read()

            # Hier wordt de naam van de factuur gegenereerd met factuurnummer en klantnaam
            factuur_naam = f"{factuurnummer} - {klantgegevens['naam']}"

            # Genereer de PDF met de naam in het formaat "factuurnummer - klantnaam.pdf"
            pdf_naam = os.path.join(r"C:\Users\jensvandevelde\Desktop\pythoncode\Projectwerk-Individueel-Python\Facturen", f"{factuur_naam}.pdf")

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
            schijf_count = len(selected_schijven)

            for schijf, percentage in selected_schijven.items():
                opmerking_query = "SELECT Percentage, Opmerking FROM Schijven WHERE schijf_id = ?"
                cursor_sql_server.execute(opmerking_query, (schijf,))
                opmerking_result = cursor_sql_server.fetchone()

                if opmerking_result:
                    percentage_db, opmerking = opmerking_result
                    prijs = klantgegevens["prijs"] * (percentage / 100.0)

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
            for schijf, percentage in selected_schijven.items():
                prijs = klantgegevens["prijs"] * (percentage / 100.0)
                subtotaal += prijs
                html_sjabloon = html_sjabloon.replace(f"[SCHIJF{schijf}]", f"Schijf {schijf}")
                html_sjabloon = html_sjabloon.replace(f"[PRIJS{schijf}]", formatteer_bedrag(prijs))

            btw_percentage = float(input("Voer het BTW-percentage in: ")) / 100
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

            # Sla de factuur op in de database
            sla_factuur_op_in_database(factuurnummer, resultaat[0], list(selected_schijven.keys()), cursor_sql_server, connection_sql_server)
        else:
            print("Er zijn geen klanten gevonden met de opgegeven naam.")
    except pyodbc.Error as err_sql_server:
        print(f"Er is een fout opgetreden bij het verbinden met SQL Server: {err_sql_server}")

# Hoofdprogramma
partial_naam = input("Voer een deel van de naam in van de klant die u zoekt: ")
schijfnummers = vraag_schijf_nummers()

try:
    # Configuratie voor SQL Server-verbinding
    # Connect to the SQL Server database using the provided connection string from database_config.py
    connection_sql_server = pyodbc.connect(connection_string_azure_sql_edge)
    cursor_sql_server = connection_sql_server.cursor()

    # Voer de rest van je code hier uit

    selected_schijven = haal_schijf_informatie_op(schijfnummers, cursor_sql_server)

    # Voordat je de loop begint, lees de inhoud van het HTML-sjabloonbestand
    with open("testing.html", "r") as sjabloon_bestand:
        html_sjabloon = sjabloon_bestand.read()

    # Als er slechts één schijf is geselecteerd, verberg de extra placeholders
    if len(selected_schijven) == 1:
        for i in range(7):
            html_sjabloon = html_sjabloon.replace(f"[extra{i}]", "")
            html_sjabloon = html_sjabloon.replace(f"[PRIJS_EXTRA{i}]", "")

    # Nu kun je html_sjabloon gebruiken zoals eerder in je code
    haal_klantgegevens_op_en_genereer_pdf(partial_naam, selected_schijven, cursor_sql_server)

except pyodbc.Error as err_sql_server:
    print(f"Fout bij het verbinden met SQL Server: {err_sql_server}")
finally:
    if 'connection_sql_server' in locals():
        # Close the SQL Server database connection
        cursor_sql_server.close()
        connection_sql_server.close()