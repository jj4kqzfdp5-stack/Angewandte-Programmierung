import json
import random
import requests
import os
from pathlib import Path
from datetime import datetime, timedelta, timezone

# Random Notizen erzeugen

def generate_mock_data(count=50):
    """Erstellt 50 Notizen im Ordner data/"""
    base_path = Path(__file__).parent
    data_folder = base_path / "data"
    file_path = data_folder / "notes.json"
    
    # Ordner erstellen falls er fehlt
    data_folder.mkdir(parents=True, exist_ok=True)

    categories = ["Work", "Personal", "Study", "Finance", "Health"]
    tag_pool = ["urgent", "todo", "meeting", "important", "university"]
    notes = []
    
    for i in range(1, count + 1):
        timestamp = datetime.now(timezone.utc) - timedelta(days=random.randint(0, 30))
        notes.append({
            "id": i,
            "title": f"Test Notiz {i}",
            "content": "Dies ist eine automatisch generierte Testnotiz.",
            "category": random.choice(categories),
            "tags": random.sample(tag_pool, random.randint(1, 2)),
            "created_at": timestamp.isoformat()
        })

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(notes, f, indent=4, ensure_ascii=False)
    print(f"✅ 50 Notizen generiert in: {file_path}")

################# Verbindungstest ######################

def test_api_connection():
    """Prüft ob der FastAPI Server online ist"""
    url = "http://127.0.0.1:8000/"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            print(f"✅ API ist online! Antwort: {response.json()}")
        else:
            print(f"⚠️ API antwortet mit Status: {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("❌ API nicht erreichbar. Läuft 'uv run fastapi dev'?")

if __name__ == "__main__":
    # WICHTIG: Beide Funktionen müssen hier stehen!
    generate_mock_data(50)
    test_api_connection()