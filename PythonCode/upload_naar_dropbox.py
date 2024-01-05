import dropbox
import os

# Vervang deze waarden door je eigen API-sleutels
APP_KEY = 'rqlkvdzglwt77lt'
APP_SECRET = 'mrk3u0gvi6uc0ov'
ACCESS_TOKEN = 'sl.Bq69V5ppQlJQAfNCZENOdfDikqjVuqgwXumXNJGSFzkWZQ5GUGsRnM4s3xjBzWdi8YLkLLwCplTbpfhme5L1pNfL1-Bnc5PY7osXx6kqqTOlsOCyqX_I8sizgp1Zbti3ZCm9eKkgCXKiSThJvfwg'

# Maak een Dropbox-client
dbx = dropbox.Dropbox(ACCESS_TOKEN)

# Lokale map waarin de bestanden zich bevinden die je wilt uploaden
lokale_map = 'C:\\Users\\jensvandevelde\\Desktop\\Pythonprogram\\Facturen'

# Doelmap op Dropbox waarin je de bestanden wilt plaatsen (vervang dit met het pad uit de Dropbox-link)
doelmap_dropbox = '/Facturen/'

# Lijst alle bestanden in de lokale map op
bestanden_lokaal = os.listdir(lokale_map)

# Loop door de lokale bestanden
for bestandsnaam in bestanden_lokaal:
    lokaal_bestand_pad = os.path.join(lokale_map, bestandsnaam)
    doel_bestand_pad = doelmap_dropbox + bestandsnaam

    # Controleer of het bestand nog niet in Dropbox staat
    try:
        dbx.files_get_metadata(doel_bestand_pad)
        print(f'Bestand "{bestandsnaam}" bestaat al in Dropbox, wordt overgeslagen.')
    except dropbox.exceptions.ApiError as e:
        # Het bestand bestaat nog niet in Dropbox, upload het
        with open(lokaal_bestand_pad, 'rb') as f:
            dbx.files_upload(f.read(), doel_bestand_pad)
            print(f'Bestand "{bestandsnaam}" succesvol geüpload naar Dropbox in de map "{doelmap_dropbox}"')
