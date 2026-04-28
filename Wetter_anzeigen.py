import requests
from fastapi import FastAPI

app = FastAPI()

API_KEY = "e3862ba5f508172108f8c0a85fda1dc4"

@app.get("/wetter/{stadt}")
def get_weather(stadt: str):
    # 1. Die Ziel-URL zusammenbauen (metrische Einheiten & deutsche Sprache)
    url = f"http://api.openweathermap.org/data/2.5/weather?q={stadt}&appid={API_KEY}&units=metric&lang=de"
    
    # 2. Die externe API aufrufen
    response = requests.get(url)
    
    # 3. Prüfen, ob die Anfrage erfolgreich war (Code 200)
    if response.status_code == 200:
        data = response.json()
        
        # 4. Nur die wichtigen Daten extrahieren
        temp = data["main"]["temp"]
        wetter = data["weather"][0]["description"]
        
        return {
            "stadt": stadt,
            "temperatur": f"{temp} Grad",
            "Wetter": wetter
        }
    else:
        # Falls die Stadt nicht existiert oder der Key falsch ist
        return {"error": "Daten konnten nicht geladen werden", "status": response.status_code}