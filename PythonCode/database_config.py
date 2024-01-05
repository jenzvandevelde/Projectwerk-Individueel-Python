# database_config.py

# Connection string for Azure SQL Edge
server = '78.22.195.15,1433'  # IP-adres van je Raspberry Pi
username = 'SA'           # Gebruikersnaam SA
password = 'Mylo1621'     # Wachtwoord
database = 'python'       # Naam van de database

connection_string_azure_sql_edge = f"DRIVER=ODBC Driver 17 for SQL Server;SERVER={server};DATABASE={database};UID={username};PWD={password}"
