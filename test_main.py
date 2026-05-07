import pytest
from fastapi.testclient import TestClient
from main import app  # Importiert deine FastAPI Instanz

client = TestClient(app)

# --- HELPER ---
def create_note(title="Test", content="Content", category="General", tags=None):
    if tags is None: tags = ["test"]
    return client.post("/notes", json={
        "title": title,
        "content": content,
        "category": category,
        "tags": tags
    })

# --- TESTS ---

# 1. Basis Erreichbarkeit
def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()

# 2-6. CRUD Operationen (Erstellen, Lesen, Einzelabruf, Update, Löschen)
def test_create_note_success():
    response = create_note("Urlaub", "Italien planen", "Privat", ["urlaub", "2024"])
    assert response.status_code == 201
    assert response.json()["title"] == "Urlaub"
    assert "id" in response.json()

def test_get_notes_list():
    response = client.get("/notes")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_specific_note():
    new_note = create_note("Find mich").json()
    response = client.get(f"/notes/{new_note['id']}")
    assert response.status_code == 200
    assert response.json()["title"] == "Find mich"

def test_patch_note_partial():
    new_note = create_note("Alt").json()
    response = client.patch(f"/notes/{new_note['id']}", json={"title": "Neu"})
    assert response.status_code == 200
    assert response.json()["title"] == "Neu"

def test_delete_note_success():
    new_note = create_note("Weg").json()
    del_resp = client.delete(f"/notes/{new_note['id']}")
    assert del_resp.status_code == 204
    # Nachprüfung
    get_resp = client.get(f"/notes/{new_note['id']}")
    assert get_resp.status_code == 404

# 7-10. Filter Tests (Kategorie & Suche)
def test_filter_by_category():
    create_note(category="Work")
    response = client.get("/notes?category=Work")
    for note in response.json():
        assert note["category"] == "Work"

def test_filter_search_title():
    create_note(title="Geheimrezept")
    response = client.get("/notes?search=Geheim")
    assert any("Geheimrezept" in n["title"] for n in response.json())

def test_filter_search_content():
    create_note(content="Passwort ist 123")
    response = client.get("/notes?search=Passwort")
    assert any("123" in n["content"] for n in response.json())

def test_categories_unique_list():
    create_note(category="A")
    create_note(category="A")
    response = client.get("/categories")
    assert "A" in response.json()
    assert response.json().count("A") == 1 # Keine Duplikate

# 11-14. Tag System
def test_get_tags_list():
    create_note(tags=["coding", "python"])
    response = client.get("/tags")
    assert "coding" in response.json()

def test_tags_are_normalized():
    # Testet ob Tags durch den Pydantic Validator gesäubert werden
    response = create_note(tags=["  GROSS  ", "duplikat", "DUPLIKAT"])
    data = response.json()
    assert "gross" in data["tags"]
    assert data["tags"].count("duplikat") == 1

# 15-17. Statistik & Validierung (Tag 5)
def test_stats_endpoint():
    response = client.get("/notes/stats")
    assert response.status_code == 200
    assert "total_notes" in response.json()

def test_validation_short_title():
    # Pydantic sollte Titel < 1 Zeichen ablehnen
    response = client.post("/notes", json={"title": "", "content": "X"})
    assert response.status_code == 422

def test_validation_extra_fields():
    # Pydantic extra="forbid" Test
    response = client.post("/notes", json={"title": "X", "content": "X", "hacker_field": "hi"})
    assert response.status_code == 422

# 18-20. Fehlerfälle (404)
def test_error_get_nonexistent():
    response = client.get("/notes/999999")
    assert response.status_code == 404

def test_error_delete_nonexistent():
    response = client.delete("/notes/999999")
    assert response.status_code == 404

def test_error_patch_nonexistent():
    response = client.patch("/notes/999999", json={"title": "Hi"})
    assert response.status_code == 404

# 19. Test: Filter nach einem Tag, der nicht existiert
def test_filter_tag_no_results():
    # Wir suchen nach einem Tag, den wir sicher nicht vergeben haben
    response = client.get("/notes?tag=diesertagexistiertnicht123")
    assert response.status_code == 200
    # Die Liste sollte leer sein, aber die API darf nicht abstürzen
    assert isinstance(response.json(), list)

# 20. Test: Groß-/Kleinschreibung bei der Suche
def test_search_case_insensitive():
    # Wir erstellen eine Notiz mit Großbuchstaben
    create_note(title="Kaffee Pause", content="Wichtig!", category="Privat")
    # Wir suchen komplett kleingeschrieben
    response = client.get("/notes?search=kaffee")
    assert response.status_code == 200
    # Falls dein SQL 'LIKE' nutzt, sollte es das finden
    assert any("Kaffee" in n["title"] for n in response.json())