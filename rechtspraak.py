import requests  # Dit is een hulpmiddel om API's te gebruiken

# API-adres van Rechtspraak.nl
API_URL = "https://openrechtspraak.nl/api/v1/person"

# Stuur een verzoek naar de API
response = requests.get(API_URL)

# Controleer of het gelukt is
if response.status_code == 200:
    print("Gelukt! Hier is de informatie:")
    print(response.json())  # Laat de opgehaalde gegevens zien
else:
    print(f"Fout! De API geeft code {response.status_code}")
