import pyodbc
import database_config  # Importeer de database_config module

# Gebruik de connection_string_azure_sql_edge uit de database_config module
connection_string = database_config.connection_string_azure_sql_edge

# Verbinding maken met de database
connection = None
try:
    connection = pyodbc.connect(connection_string)
    cursor = connection.cursor()

    # Voer hier je SQL-query in
    query = "SELECT 'Verbinding is geslaagd' AS Resultaat"
    cursor.execute(query)

    # Haal de resultaten op
    result = cursor.fetchone()
    print(result.Resultaat)

except Exception as e:
    print(f"Fout bij verbinden met de database: {str(e)}")

finally:
    # Sluit de verbinding
    if connection:
        connection.close()
