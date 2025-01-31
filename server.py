from fastapi import FastAPI, Query
import requests

app = FastAPI()

@app.get("/rechtspraak/uitspraken")
def get_uitspraken(
    case_type: str = Query("civiel", description="Filter zaken op type (bijv. strafrecht, civiel, belasting)"),
    aansprakelijkheid: bool = Query(True, description="Filter op aansprakelijkheidsrecht (bijv. letselschade, verkeersongevallen)")
):
    API_URL = "https://openrechtspraak.nl/api/v1/uitspraak"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    try:
        response = requests.get(API_URL, headers=headers, timeout=5)  # ✅ Voeg User-Agent toe
        response.raise_for_status()
        cases = response.json().get("results", [])

        print("✅ Rechtspraak API respons:", cases)

        if not cases:
            return {"message": "Geen juridische uitspraken gevonden. Controleer of de Rechtspraak API data geeft."}

        # ✅ Stap 1: Filter alleen civiele zaken
        civiele_zaken = [case for case in cases if "civiel" in case["title"].lower()]

        # ✅ Stap 2: Filter op aansprakelijkheidszaken
        if aansprakelijkheid:
            aansprakelijkheid_keywords = ["aansprakelijkheid", "schadevergoeding", "letsel", "verkeersongeval", "bedrijfsongeval", "medische fout"]
            filtered_cases = [
                case for case in civiele_zaken
                if any(keyword in case["summary"].lower() or keyword in case["title"].lower() for keyword in aansprakelijkheid_keywords)
            ]

            # ✅ Als er geen aansprakelijkheidszaken worden gevonden, geef een melding
            if not filtered_cases:
                return {"message": "Geen aansprakelijkheidszaken gevonden binnen civiel recht."}

            return {"results": filtered_cases}

        return {"results": civiele_zaken}
    
    except requests.exceptions.Timeout:
        return {"error": "Rechtspraak API reageert niet (timeout). Probeer het later opnieuw."}
    
    except requests.exceptions.RequestException as e:
        return {"error": f"Fout bij ophalen data: {str(e)}"}
