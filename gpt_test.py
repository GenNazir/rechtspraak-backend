import requests

# URL van jouw backend
GPT_BACKEND_URL = "http://127.0.0.1:8000/rechtspraak/personen"

# Stuur een verzoek naar de backend
response = requests.get(GPT_BACKEND_URL)

# Controleer of het gelukt is
if response.status_code == 200:
    print("GPT heeft de API succesvol opgevraagd! ✅")
    print(response.json())  # Print de ontvangen data
else:
    print(f"Fout! Kan API niet bereiken: {response.status_code}")
