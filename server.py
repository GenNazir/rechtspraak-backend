from fastapi import FastAPI, Query
import requests

app = FastAPI()

@app.get("/rechtspraak/uitspraken")  # ✅ Endpointnaam gewijzigd
def get_uitspraken(
    case_type: str = Query("civiel", description="Filter zaken op type (bijv. strafrecht, civiel, belasting)"),
    aansprakelijkheid: bool = Query(True, description="Filter op aansprakelijkheidsrecht (bijv. letselschade, verkeersongevallen)")
):
    API_URL = "https://openrechtspraak.nl/api/v1/uitspraak"  # ✅ Gebruik de juiste API voor uitspraken

    try:
        response = requests.get(API_URL)
        response.raise_for_status()
        cases = response.json().get("results", [])

        print("✅ Onbewerkte API-output:", cases)  # Log alle opgehaalde zaken

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
    
    except requests.exceptions.RequestException as e:
        return {"error": f"Fout bij ophalen data: {str(e)}"}
