import pyodbc
import pandas as pd
from database_config import connection_string_azure_sql_edge

# Function to convert percentage values to integers (e.g., '10%' to 10)
def convert_percentage(percentage_str):
    if isinstance(percentage_str, int):
        return percentage_str
    if isinstance(percentage_str, float):
        return int(percentage_str * 100)
    percentage_str = percentage_str.strip('%')
    if '.' in percentage_str:
        return int(float(percentage_str) * 100)
    else:
        return int(percentage_str)

def import_schijven_data_from_excel(excel_file_path):
    try:
        # Establish a connection to the Azure SQL Edge database using the provided connection string from database_config.py
        connection_azure_sql_edge = pyodbc.connect(connection_string_azure_sql_edge)
        cursor_azure_sql_edge = connection_azure_sql_edge.cursor()

        # Read data from the Excel file for Schijven data
        df_schijven = pd.read_excel(excel_file_path, sheet_name="Schijven")

        # Iterate through the rows of the DataFrame and insert data into the "Schijven" table in Azure SQL Edge
        for index, row in df_schijven.iterrows():
            omschrijving = row['Op basis van prijs constructie']
            percentage_str = str(row['percentage'])
            opmerking = row['omschrijving']

            # Convert the percentage string to an integer
            percentage = convert_percentage(percentage_str)

            # Ensure that the percentage value is in the range of 0 to 100
            if 0 <= percentage <= 100:
                # SQL query to insert data into the "Schijven" table in Azure SQL Edge
                insert_query_schijven_azure_sql_edge = """
                INSERT INTO Schijven (Omschrijving, Percentage, Opmerking)
                VALUES (?, ?, ?)
                """

                # Insert data into the "Schijven" table in Azure SQL Edge
                cursor_azure_sql_edge.execute(insert_query_schijven_azure_sql_edge, (omschrijving, percentage, opmerking))
                connection_azure_sql_edge.commit()
            else:
                print(f"Percentage '{percentage}' is out of the valid range (0-100) and will not be inserted.")

        print("Schijvengegevens succesvol geïmporteerd!")

    except pyodbc.Error as err_azure_sql_edge:
        print(f"Fout bij het verbinden met Azure SQL Edge: {err_azure_sql_edge}")

    except pd.errors.ParserError as err:
        print(f"Fout bij het verwerken van het Excel-bestand: {err}")

    except pd.errors.EmptyDataError:
        print("Het Excel-bestand is leeg of bevat geen gegevens.")

    except PermissionError as err:
        print(f"PermissionError: {err}. Zorg ervoor dat je leestoegang hebt tot het bestand.")

    finally:
        if 'connection_azure_sql_edge' in locals():
            # Close the Azure SQL Edge database connection
            cursor_azure_sql_edge.close()
            connection_azure_sql_edge.close()

if __name__ == "__main__":
    excel_file_path = r'C:\Users\jensvandevelde\Desktop\Pythonprogram\PythonFile\kopersbestand.xlsx'
    import_schijven_data_from_excel(excel_file_path)
