import pdfkit
from datetime import datetime
import locale
import os
import pyodbc
from flask import Flask, jsonify, request, send_file
from flask_restx import Api, Resource, fields
from flask_cors import CORS
import subprocess
from flask_restx import Api, Resource, fields
from flask import request, jsonify


app = Flask(__name__)
CORS(app)  # Voeg CORS-configuratie toe

api = Api(app)
# Stel locale-instellingen in voor getalnotatie
locale.setlocale(locale.LC_ALL, 'nl_NL.UTF-8')

# Configuratie voor SQL Server-verbinding
server = '78.22.195.15,1433'
database = 'python'
username = 'Sa'
password = 'Mylo1621'
connection_string_sql_server = f"DRIVER=ODBC Driver 17 for SQL Server;SERVER={server};DATABASE={database};UID={username};PWD={password}"

# Specificeer het pad naar wkhtmltopdf
pdfkit_config = pdfkit.configuration(wkhtmltopdf=r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe')

def formatteer_bedrag(bedrag):
    return locale.format_string("%.2f", bedrag, grouping=True)

run_script_model = api.model('RunScriptModel', {
    'execute_script': fields.Boolean(description='Boolean indicating whether to execute the script or not.')
})
def get_db_connection():
    try:
        connection = pyodbc.connect(connection_string_sql_server)
        return connection
    except Exception as e:
        print(f"Fout bij het verbinden met de database: {str(e)}")
        return None

def sla_factuur_op_in_database(factuurnummer, koper_id, schijf_id_list, cursor_sql_server, connection_sql_server):
    try:
        for schijf_id in schijf_id_list:
            insert_query = "INSERT INTO facturen (factuurnummer, koper_id, schijf_id) VALUES (?, ?, ?)"
            cursor_sql_server.execute(insert_query, (factuurnummer, koper_id, schijf_id))
        
        connection_sql_server.commit()
        print("Factuur succesvol opgeslagen in de database.")
    except pyodbc.Error as err_sql_server:
        print(f"Fout bij het opslaan van de factuur in de database: {err_sql_server}")

def haal_klantgegevens_op_en_genereer_pdf(factuur_data):
    connection_sql_server = pyodbc.connect(connection_string_sql_server)
    cursor_sql_server = connection_sql_server.cursor()
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

            # Lees de inhoud van het externe HTML-bestand (vervang 'testing.html' door je eigen HTML-bestand)
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

            # Vervang selected_schijven door schijfnummers in de volgende regel
            sla_factuur_op_in_database(factuurnummer, resultaat[0], schijfnummers, cursor_sql_server, connection_sql_server)


            

        else:
            print("Er zijn geen klanten gevonden met de opgegeven naam.")
    except Exception as e:
        print(f"Fout bij het genereren van de factuur: {str(e)}")
    finally:
        cursor_sql_server.close()
        connection_sql_server.close()
        


# API model
factuur_ns = api.namespace('facturen', description='Factuur operaties')
factuur_model = api.model('FactuurModel', {
    'schijven': fields.List(fields.Integer, description='Schijfnummers', required=True),
    'factuurnummer': fields.String(description='Factuurnummer', required=True),
    'naam': fields.String(description='Klantnaam', required=True)
})

@factuur_ns.route('/maak_factuur')
class MaakFactuur(Resource):
    @api.expect(factuur_model)
    @api.doc(description='Maak een nieuwe factuur')
    def post(self):
        data = api.payload
        haal_klantgegevens_op_en_genereer_pdf(data)
        return jsonify({"status": "succes", "message": "Factuur succesvol verwerkt"})

# Define the namespace for kopers operations
ns = api.namespace('kopers', description='Kopers operaties')

@ns.route('/alle_klanten')
class AlleKlanten(Resource):
    def get(self):
        alle_klanten = []
        connection = get_db_connection()

        if connection is not None:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM kopers")

            # Fetch rows as dictionaries using the pyodbc.Row factory
            rows = cursor.fetchall()
            columns = [column[0] for column in cursor.description]
            for row in rows:
                alle_klanten.append(dict(zip(columns, row)))

            cursor.close()
            connection.close()
        else:
            return jsonify({"error": "Kan geen verbinding maken met de database"}), 500

        return jsonify(alle_klanten)


@ns.route('/zoek_klanten')
class ZoekKlanten(Resource):
    @api.doc(params={'naam': 'Naam van de klant'})
    def get(self):
        naam_query = request.args.get('naam')
        resultaten = []
        connection = get_db_connection()

        if connection is not None:
            cursor = connection.cursor()
            query = """
            SELECT * FROM kopers WHERE Naam LIKE ?
            """
            cursor.execute(query, (f"%{naam_query}%",))

            # Fetch rows as dictionaries using the pyodbc.Row factory
            rows = cursor.fetchall()
            columns = [column[0] for column in cursor.description]
            for row in rows:
                resultaten.append(dict(zip(columns, row)))

            cursor.close()
            connection.close()
        else:
            return jsonify({"error": "Kan geen verbinding maken met de database"}), 500

        return jsonify(resultaten)

@ns.route('/zoek_facturen')
class ZoekFacturen(Resource):
    @api.doc(params={'naam': 'Naam van de klant'})
    def get(self):
        naam_query = request.args.get('naam')
        resultaten = []
        connection = get_db_connection()

        if connection is not None:
            cursor = connection.cursor()
            query = """
            SELECT k.Naam AS Klantnaam, f.*
            FROM facturen AS f
            JOIN kopers AS k ON f.koper_id = k.koper_id
            WHERE LOWER(k.Naam) LIKE LOWER(?)
            """
            cursor.execute(query, (f"%{naam_query}%",))

            # Fetch rows as dictionaries using the pyodbc.Row factory
            rows = cursor.fetchall()
            columns = [column[0] for column in cursor.description]
            for row in rows:
                resultaten.append(dict(zip(columns, row)))

            cursor.close()
            connection.close()
        else:
            return jsonify({"error": "Kan geen verbinding maken met de database"}), 500

        return jsonify(resultaten)

@ns.route('/alle_facturen')
class AlleFacturen(Resource):
    def get(self):
        alle_facturen = []
        connection = get_db_connection()

        if connection is not None:
            cursor = connection.cursor()
            query = """
            SELECT k.Gebouw AS Gebouwnaam, k.Naam AS Klantnaam, f.*
            FROM facturen AS f
            JOIN kopers AS k ON f.koper_id = k.koper_id
            """
            cursor.execute(query)

            # Fetch rows as dictionaries using the pyodbc.Row factory
            rows = cursor.fetchall()
            columns = [column[0] for column in cursor.description]
            for row in rows:
                alle_facturen.append(dict(zip(columns, row)))
            
            cursor.close()
            connection.close()
        else:
            return jsonify({"error": "Kan geen verbinding maken met de database"}), 500

        return jsonify(alle_facturen)
    
facturen_map = "C:\\Users\\jensvandevelde\\Desktop\\Pythonprogram\\Facturen"

@app.route('/open_factuur', methods=['GET'])
def open_factuur():
    factuurnummer = request.args.get('factuurnummer')
    klantnaam = request.args.get('klantnaam')

    # Genereer de bestandsnaam op basis van factuurnummer en klantnaam
    pdf_filename = f"{factuurnummer} - {klantnaam}.pdf"
    pdf_path = os.path.join("C:\\Users\\jensvandevelde\\Desktop\\Pythonprogram\\Facturen", pdf_filename)

    # Controleer of het PDF-bestand bestaat
    if os.path.exists(pdf_path):
        try:
            # Stuur het PDF-bestand als reactie
            return send_file(pdf_path, mimetype='application/pdf')
        except Exception as e:
            return jsonify({"error": f"Fout bij het openen van het PDF-bestand: {str(e)}"}), 500
    else:
        return jsonify({"error": f"PDF-bestand '{pdf_filename}' niet gevonden."}), 404
@ns.route('/alle_schijven')
class AlleSchijven(Resource):
        def get(self):
            alle_schijven = []
            connection = get_db_connection()

            if connection is not None:
                cursor = connection.cursor()
                cursor.execute("SELECT * FROM schijven")

                # Fetch rows as dictionaries using the pyodbc.Row factory
                rows = cursor.fetchall()
                columns = [column[0] for column in cursor.description]
                for row in rows:
                    alle_schijven.append(dict(zip(columns, row)))

                cursor.close()
                connection.close()
            else:
                return jsonify({"error": "Kan geen verbinding maken met de database"}), 500

            return jsonify(alle_schijven)

@api.route('/recentste_factuurnummer')
class RecentsteFactuurnummer(Resource):
        @api.doc(description='Haal het recentste factuurnummer op')
        def get(self):
            connection = get_db_connection()

            if connection is not None:
                try:
                    cursor = connection.cursor()
                    cursor.execute("SELECT MAX(factuurnummer) AS RecentsteFactuurnummer FROM facturen")
                    result = cursor.fetchone()

                    if result:
                        # Gebruik index toegang als het resultaat een tuple is
                        recentste_factuurnummer = result[0]
                        return jsonify({"recentste_factuurnummer": recentste_factuurnummer})
                    else:
                        return jsonify({"error": "Geen recentste factuurnummer gevonden"}), 404
                except Exception as e:
                    return jsonify({"error": str(e)}), 500
                finally:
                    cursor.close()
                    connection.close()
            else:
                return jsonify({"error": "Kan geen verbinding maken met de database"}), 500
            
# API-model voor de /run-script-route
run_script_model = api.model('RunScriptModel', {})

@api.route('/run-script')
@api.doc(description='Voer een extern script uit')
class RunScript(Resource):
    @api.expect(run_script_model)
    @api.doc(description='Voer een extern script uit')
    def post(self):
        try:
            data = request.json
            execute_script = data.get('execute_script', False)  # Standby default to False
            
            if execute_script:
                print("Probeer het script uit te voeren...")
                subprocess.run(['python', 'upload_naar_dropbox.py'], check=True)
                print("Script uitgevoerd.")
                response = {'message': 'Script uitgevoerd'}
            else:
                response = {'message': 'Script is niet uitgevoerd omdat execute_script op False staat.'}
        except subprocess.CalledProcessError as e:
            print(f'Fout bij het uitvoeren van het script: {e}')
            response = {'error': f'Fout bij het uitvoeren van het script: {e}'}

        return jsonify(response)

# Define the expected JSON format for updating a customer
update_customer_model = api.model('UpdateCustomer', {
    'Berging': fields.String,
    'Email': fields.String,
    'GEBOUW': fields.String,
    'Huisnummer': fields.String,
    'Naam': fields.String,
    'PARKING': fields.String,
    'Postcode': fields.String,
    'Prijs': fields.String,
    'Prijs_Berging': fields.String,
    'Prijs_Constructie': fields.String,
    'Prijs_Parking': fields.String,
    'Stad': fields.String,
    'Straat': fields.String,
    'Telefoonnummer': fields.String,
    'koper_id': fields.Integer
})
# Define the route to update customer information
@api.route('/update_customer')
class UpdateCustomer(Resource):
    @api.doc(description='Update customer information')
    @api.expect(update_customer_model)  # Expect the specified JSON format
    def put(self):
        try:
            update_data = request.json

            # Get the koper_id from the update_data JSON
            koper_id = update_data.get('koper_id')

            # SQL query to update customer data
            sql = """UPDATE kopers
                     SET GEBOUW = ?, Prijs = ?, Prijs_Constructie = ?, PARKING = ?,
                         Prijs_Parking = ?, Berging = ?, Prijs_Berging = ?, Naam = ?,
                         Straat = ?, Huisnummer = ?, Postcode = ?, Stad = ?, Email = ?,
                         Telefoonnummer = ?
                     WHERE koper_id = ?"""

            cnxn = get_db_connection()  # Establish a database connection
            if cnxn is not None:
                cursor = cnxn.cursor()
                try:
                    cursor.execute(sql, (update_data['GEBOUW'], update_data['Prijs'], update_data['Prijs_Constructie'],
                                         update_data['PARKING'], update_data['Prijs_Parking'], update_data['Berging'],
                                         update_data['Prijs_Berging'], update_data['Naam'], update_data['Straat'],
                                         update_data['Huisnummer'], update_data['Postcode'], update_data['Stad'],
                                         update_data['Email'], update_data['Telefoonnummer'], koper_id))
                    cnxn.commit()
                    response_message = f'Customer with koper_id {koper_id} updated successfully'
                    return {'message': response_message}, 200
                except Exception as e:
                    return {'error': str(e)}, 500
                finally:
                    cursor.close()
                    cnxn.close()
            else:
                return {'error': 'Error connecting to the database'}, 500
        except Exception as e:
            return {'error': str(e)}, 400



create_customer_model = api.model('CreateCustomer', {

    'Berging': fields.String,
    'Email': fields.String,
    'GEBOUW': fields.String,
    'Huisnummer': fields.String,
    'Naam': fields.String,
    'PARKING': fields.String,
    'Postcode': fields.String,
    'Prijs': fields.String,
    'Prijs_Berging': fields.String,
    'Prijs_Constructie': fields.String,
    'Prijs_Parking': fields.String,
    'Stad': fields.String,
    'Straat': fields.String,
    'Telefoonnummer': fields.String,
})
# Define the route to create a new customer
# Define the route to create a new customer
# Define the route to create a new customer
@api.route('/create_customer')
class CreateCustomer(Resource):
    @api.doc(description='Create a new customer')
    @api.expect(create_customer_model)  # Expect the specified JSON format
    def post(self):
        try:
            new_data = request.json

            # SQL query to insert customer data without specifying koper_id
            sql = """INSERT INTO kopers (GEBOUW, Prijs, Prijs_Constructie, PARKING, Prijs_Parking, Berging, Prijs_Berging, Naam, Straat, Huisnummer, Postcode, Stad, Email, Telefoonnummer)
                     VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""

            cnxn = get_db_connection()  # Establish a database connection
            if cnxn is not None:
                cursor = cnxn.cursor()
                try:
                    cursor.execute(sql, (new_data['GEBOUW'], new_data['Prijs'], new_data['Prijs_Constructie'],
                                         new_data['PARKING'], new_data['Prijs_Parking'], new_data['Berging'],
                                         new_data['Prijs_Berging'], new_data['Naam'], new_data['Straat'],
                                         new_data['Huisnummer'], new_data['Postcode'], new_data['Stad'],
                                         new_data['Email'], new_data['Telefoonnummer']))
                    cnxn.commit()
                    response_message = 'Customer created successfully'
                    return {'message': response_message}, 201
                except Exception as e:
                    return {'error': str(e)}, 500
                finally:
                    cursor.close()
                    cnxn.close()
            else:
                return {'error': 'Error connecting to the database'}, 500
        except Exception as e:
            return {'error': str(e)}, 400









if __name__ == "__main__":
    app.run(debug=True)
