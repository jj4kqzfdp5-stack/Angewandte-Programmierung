import pytest
import requests
from faker import Faker

name_faker = Faker()

BASE_URL = "http://localhost:8000"

def test_read_root():
    """Test root endpoint"""
    response = requests.get(f"{BASE_URL}/")
    assert response.status_code == 200
    response = requests.get(f"{BASE_URL}/")

    assert response.status_code == 200
    
    data = response.json()
    assert data["message"] == "Hello ... World!"

def test_check_404_error():
    response = requests.get(f"{BASE_URL}/does-not-exist")
    assert response.status_code == 404

def test_check_greetings():
    for _ in range(10):
        name = name_faker.name()
        response = requests.get(f"{BASE_URL}/greetings/{name}")

        assert response.status_code == 200
        data = response.json()
        assert data["message"] == f"Hello {name}!"


def test_is_adult():
    """Test if Check Adult works"""
    
    for age in range(0, 40):
        
        adult = age >= 18
        response = requests.get(f"{BASE_URL}/is-adult/{age}")
        assert response.status_code == 200
        data = response.json()
        for key in ["is_adult", "can_drive", "can_vote"]:
            assert data[key] == adult
        assert data["age"] == age

def test_is_adult_negative_age():
    """Test if Adult is not negative"""
    
    for age in range(-20, 0):
        
        response = requests.get(f"{BASE_URL}/is-adult/{age}")
        assert response.status_code == 400


#--------------- Copilot Code -----------------------#

import pytest
from fastapi.testclient import TestClient
from ALT_main import app  # Deine FastAPI-App Instanz

client = TestClient(app)

# Konstante für reproduzierbare Testdaten
SAMPLE_NOTE = {
    "title": "Integration Test",
    "content": "Checking JSON persistence",
    "category": "test-env",
    "tags": ["automated", "pytest"]
}

def test_note_lifecycle_and_filtering():
    """
    Testet Erstellung, Abruf via Filter und Löschung in einem Durchlauf.
    Verhindert Datenmüll in der produktiven notes.json.
    """
    # 1. CREATE: Notiz anlegen[cite: 4, 5]
    create_res = client.post("/notes", json=SAMPLE_NOTE)
    assert create_res.status_code == 201
    note_id = create_res.json()["id"]

    try:
        # 2. READ: Einzelabruf via Pfad-Parameter
        get_res = client.get(f"/notes/{note_id}")
        assert get_res.status_code == 200
        assert get_res.json()["category"] == "test-env"

        # 3. FILTER: Suche über Query-Parameter
        # Wir prüfen, ob unsere Test-Notiz in der Suche nach 'Integration' auftaucht
        search_res = client.get("/notes?search=Integration")
        ids = [note["id"] for note in search_res.json()]
        assert note_id in ids

        # 4. STATS: Prüfen ob der Statistik-Endpunkt antwortet[cite: 4, 5]
        stats_res = client.get("/notes/stats")
        assert stats_res.status_code == 200
        assert "total_notes" in stats_res.json()

    finally:
        # 5. DELETE: Cleanup (Wichtig für deine produktive JSON!)[cite: 5, 6]
        delete_res = client.delete(f"/notes/{note_id}")
        assert delete_res.status_code in [204, 200] # Je nach deiner Implementierung