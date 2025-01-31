from fastapi import FastAPI
import requests

app = FastAPI()  # Maak een nieuwe FastAPI-app

# Endpoint om gegevens op te halen van Rechtspraak.nl
@app.get("/rechtspraak/personen")
def get_personen():
    API_URL = "https://openrechtspraak.nl/api/v1/person"  # API URL van Rechtspraak.nl
    response = requests.get(API_URL)  # Stuur een aanvraag naar de API
    
    if response.status_code == 200:  # Als het lukt
        return response.json()  # Stuur de data terug
    else:
        return {"error": f"Fout bij ophalen data: {response.status_code}"}  # Geef een foutmelding terug
