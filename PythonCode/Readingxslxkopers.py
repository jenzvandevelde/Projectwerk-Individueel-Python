import pyodbc
import pandas as pd
from database_config import connection_string_azure_sql_edge

def import_kopers_data_from_excel(excel_file_path):
    try:
        # Connect to the Azure SQL Edge database using the provided connection string from database_config.py
        connection = pyodbc.connect(connection_string_azure_sql_edge)
        cursor = connection.cursor()

        # Read data from the Excel file for kopers data
        df_kopers = pd.read_excel(excel_file_path)

        # Iterate through the rows of the DataFrame and insert data into the "kopers" table
        for index, row in df_kopers.iterrows():
            gebouw = row['GEBOUW']
            prijs = float(row['Prijs'])
            prijs_constructie = float(row['Prijs-Constructie'])
            naam = row['Naam']
            straat = row['Straat']
            huisnummer = row['Huisnummer']
            postcode = row['Postcode']
            stad = row['Stad']
            email = row['Email']
            telefoonnummer = row['Telefoonnummer']

            # Check if the value for 'Parking' is empty
            parking = None if pd.isna(row['PARKING']) else row['PARKING']

            # Check if the value for 'Prijs_Parking' is empty
            prijs_parking = None if pd.isna(row['Prijs-Parking']) else float(row['Prijs-Parking'])

            # Check if the value for 'Berging' is empty
            berging = None if pd.isna(row['Berging']) else row['Berging']

            # Check if the value for 'Prijs_Berging' is empty
            prijs_berging = None if pd.isna(row['Prijs-Berging']) else float(row['Prijs-Berging'])

            # SQL query to insert data into the "kopers" table
            insert_query = """
            INSERT INTO kopers (GEBOUW, Prijs, Prijs_Constructie, PARKING, Prijs_Parking, Berging, Prijs_Berging, Naam, Straat, Huisnummer, Postcode, Stad, Email, Telefoonnummer)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """

            # Insert data into the "kopers" table
            cursor.execute(insert_query, (gebouw, prijs, prijs_constructie, parking, prijs_parking, berging, prijs_berging, naam, straat, huisnummer, postcode, stad, email, telefoonnummer))
            connection.commit()

        print("Kopersgegevens succesvol geïmporteerd!")

    except pyodbc.Error as err:
        print(f"Fout bij het verbinden met Azure SQL Edge: {err}")

    except pd.errors.ParserError as err:
        print(f"Fout bij het verwerken van het Excel-bestand: {err}")

    except pd.errors.EmptyDataError:
        print("Het Excel-bestand is leeg of bevat geen gegevens.")

    except PermissionError as err:
        print(f"PermissionError: {err}. Zorg ervoor dat je leestoegang hebt tot het bestand.")

    finally:
        if 'connection' in locals():
            # Close the database connection
            cursor.close()
            connection.close()

if __name__ == "__main__":
    excel_file_path = r'C:\Users\jensvandevelde\Desktop\Pythonprogram\PythonFile\kopersbestand.xlsx'
    import_kopers_data_from_excel(excel_file_path)
