import pytest
from fastapi.testclient import TestClient
from main import app  # Importiert deine FastAPI Instanz

client = TestClient(app)

# 1. Test: Titel zu kurz (Task 2)
def test_create_note_rejects_short_title():
    response = client.post("/notes", json={
        "title": "Ab", 
        "content": "Inhalt ist okay", 
        "category": "general"
    })
    assert response.status_code == 422

# 2. Test: Unbekannte Kategorie (Task 2)
def test_create_note_rejects_unknown_category():
    response = client.post("/notes", json={
        "title": "Gültiger Titel", 
        "content": "Testinhalt", 
        "category": "party" # Nicht in der Whitelist
    })
    assert response.status_code == 422

# 3. Test: Tag-Normalisierung & Deduplizierung (Task 2)
def test_create_note_normalizes_tags():
    response = client.post("/notes", json={
        "title": "Tag Test", 
        "content": "Inhalt", 
        "category": "ideas",
        "tags": ["  Python  ", "python", "API"]
    })
    assert response.status_code == 201
    data = response.json()
    # Erwartet: ["python", "api"] - kleingeschrieben, ohne Leerzeichen, keine Duplikate
    assert data["tags"] == ["python", "api"]

# 4. Test: Verbot von Extra-Feldern (Task 1: extra="forbid")
def test_create_note_forbids_extra_fields():
    response = client.post("/notes", json={
        "title": "Titel", 
        "content": "Inhalt", 
        "category": "general",
        "hacker_attack": "true" # Dieses Feld existiert nicht im Modell
    })
    assert response.status_code == 422

# 5. Test: Cross-Field Rule für 'work' (Task 3)
def test_work_note_requires_work_tag():
    response = client.post("/notes", json={
        "title": "Büroarbeit", 
        "content": "Bericht schreiben", 
        "category": "work",
        "tags": ["büro"] # 'work' tag fehlt
    })
    assert response.status_code == 422

# 6. Test: PATCH mit leerem Body (Task 4)
def test_patch_with_empty_body_succeeds():
    # Erst eine Notiz erstellen
    first_resp = client.post("/notes", json={"title": "Original", "content": "C", "category": "general"})
    note_id = first_resp.json()["id"]
    
    response = client.patch(f"/notes/{note_id}", json={})
    assert response.status_code == 200 # Muss laut Task 4 erfolgreich sein

# 7. Test: PATCH mit ungültigem Titel (Task 4)
def test_patch_with_invalid_title_fails():
    first_resp = client.post("/notes", json={"title": "Original", "content": "C", "category": "general"})
    note_id = first_resp.json()["id"]
    
    response = client.patch(f"/notes/{note_id}", json={"title": ""})
    assert response.status_code == 422

# 8. Test: Tag-Name Normalisierung (Task 5)
def test_tag_name_normalization():
    from main import Tag
    # Wir erstellen einen Tag mit Großbuchstaben
    test_tag = Tag(name="  TEST-Tag  ")
    
    # Erwartung: Es wird nicht abgelehnt, sondern normalisiert (Task 5)
    assert test_tag.name == "test-tag"
    
    # Test auf den Regex (Task 5: match ^[a-z0-9-]+$)
    # Hier sollte es weiterhin krachen, wenn verbotene Zeichen genutzt werden
    with pytest.raises(Exception):
        Tag(name="unzulässiges_zeichen!")