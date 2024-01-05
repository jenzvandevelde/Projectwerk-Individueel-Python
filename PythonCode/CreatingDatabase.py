import pyodbc
from database_config import connection_string_azure_sql_edge

def create_database_and_tables():
    try:
        connection = pyodbc.connect(connection_string_azure_sql_edge)
        cursor = connection.cursor()

        # Beëindig eventuele lopende transacties
        cursor.execute("COMMIT")

        # Database maken als deze niet bestaat
        create_database_query = "IF NOT EXISTS (SELECT name FROM sys.databases WHERE name = 'python') CREATE DATABASE python"
        cursor.execute(create_database_query)
        connection.commit()

        # Gebruik de database 'python'
        cursor.execute("USE python")

        # Maak de tabel 'kopers' aan als deze niet bestaat
        create_table_kopers_query = """
        IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'kopers')
        CREATE TABLE kopers (
            koper_id INT IDENTITY(1,1) PRIMARY KEY,
            GEBOUW NVARCHAR(255),
            Prijs DECIMAL(10, 2),
            Prijs_Constructie DECIMAL(10, 2),
            PARKING NVARCHAR(255),
            Prijs_Parking DECIMAL(10, 2),
            Berging NVARCHAR(255),
            Prijs_Berging DECIMAL(10, 2),
            Naam NVARCHAR(255),
            Straat NVARCHAR(255),
            Huisnummer NVARCHAR(255),
            Postcode NVARCHAR(255),
            Stad NVARCHAR(255),
            Email NVARCHAR(255),
            Telefoonnummer NVARCHAR(255)
        )
        """
        cursor.execute(create_table_kopers_query)
        connection.commit()

        # Maak de tabel 'Schijven' aan als deze niet bestaat
        create_table_schijven_query = """
        IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'schijven')
        CREATE TABLE schijven (
            schijf_id INT IDENTITY(1,1) PRIMARY KEY,
            Omschrijving NVARCHAR(255),
            Percentage INT,
            Opmerking NVARCHAR(255)
        )
        """
        cursor.execute(create_table_schijven_query)
        connection.commit()

        # Maak de tabel 'facturen' aan als deze niet bestaat
        create_table_facturen_query = """
        IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'facturen')
        CREATE TABLE facturen (
            id INT IDENTITY(1,1) PRIMARY KEY,
            factuurnummer NVARCHAR(255) NOT NULL,
            koper_id INT NOT NULL,
            schijf_id INT NOT NULL,
            FOREIGN KEY (koper_id) REFERENCES kopers(koper_id),
            FOREIGN KEY (schijf_id) REFERENCES schijven(schijf_id)
        )
        """
        cursor.execute(create_table_facturen_query)
        connection.commit()

        print("Database en tabellen succesvol aangemaakt!")

    except pyodbc.Error as err:
        print(f"Fout bij het verbinden met Azure SQL Edge: {err}")

    finally:
        if 'connection' in locals():
            # Verbinding met de database sluiten
            cursor.close()
            connection.close()

if __name__ == "__main__":
    create_database_and_tables()
