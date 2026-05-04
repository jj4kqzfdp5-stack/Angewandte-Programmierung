from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional, List
import json

app = FastAPI(
    title="Angewandte Programmierung",
    description="Notizenmanagement API für den Kurs"
)

# --- Modelle ---

class NoteCreate(BaseModel):
    title: str
    content: str
    category: str = "General"  # Standardwert für Kategorie

class Note(BaseModel):
    id: int
    title: str
    content: str
    category: str
    created_at: str

# --- Hilfsfunktionen für Persistenz ---

NOTES_FILE = Path("data/notes.json")

def load_notes() -> tuple[List[Note], int]:
    """Lädt Notizen aus der JSON-Datei und gibt (Liste, Nächste_ID) zurück."""
    if not NOTES_FILE.exists():
        return [], 1
    
    with open(NOTES_FILE, 'r') as f:
        data = json.load(f)
        # Wir wandeln Dicts aus JSON direkt in Pydantic-Objekte um
        notes = [Note(**n) for n in data]
        
    next_id = max((n.id for n in notes), default=0) + 1
    return notes, next_id

def save_notes(notes: List[Note]):
    """Speichert die Liste der Notizen-Objekte als JSON."""
    NOTES_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(NOTES_FILE, 'w') as f:
        # .model_dump() ist der moderne Ersatz für .dict() in Pydantic V2
        json.dump([n.model_dump() for n in notes], f, indent=2)

# --- Basis Endpunkte ---

@app.get("/")
def root():
    return {"message": "Hello ... World!"}  # Fix für den Test (Ausrufezeichen)

@app.get("/is-adult/{age}")
def check_adult(age: int):
    """Prüft Volljährigkeit und validiert gegen negative Werte."""
    if age < 0:
        raise HTTPException(status_code=400, detail="Alter darf nicht negativ sein.")
    
    is_adult = age >= 18
    return {
        "age": age,
        "is_adult": is_adult,
        "can_drive": is_adult,
        "can_vote": is_adult
    }

# --- Notizen Endpunkte (CRUD & Filter) ---

@app.post("/notes", status_code=201)
def create_note(note_in: NoteCreate) -> Note:
    """Erstellt eine neue Notiz und speichert sie lokal."""
    notes, next_id = load_notes()
    
    new_note = Note(
        id=next_id,
        title=note_in.title,
        content=note_in.content,
        category=note_in.category,
        created_at=datetime.now(timezone.utc).isoformat()
    )
    
    notes.append(new_note)
    save_notes(notes)
    return new_note

@app.get("/notes", response_model=List[Note])
def get_notes(category: Optional[str] = None, search: Optional[str] = None):
    """Gibt alle Notizen zurück, optional gefiltert nach Kategorie oder Suchbegriff."""
    notes, _ = load_notes()
    
    filtered = notes
    if category:
        filtered = [n for n in filtered if n.category.lower() == category.lower()]
    
    if search:
        s = search.lower()
        filtered = [n for n in filtered if s in n.title.lower() or s in n.content.lower()]
        
    return filtered

@app.get("/notes/{note_id}", response_model=Note)
def get_single_note(note_id: int):
    """Sucht eine spezifische Notiz per ID."""
    notes, _ = load_notes()
    for n in notes:
        if n.id == note_id:
            return n
    raise HTTPException(status_code=404, detail=f"Notiz {note_id} nicht gefunden.")

@app.delete("/notes/{note_id}", status_code=204)
def delete_note(note_id: int):
    """Löscht eine Notiz."""
    notes, _ = load_notes()
    initial_length = len(notes)
    
    # Behalte alle Notizen, außer der mit der gesuchten ID
    notes = [n for n in notes if n.id != note_id]
    
    if len(notes) == initial_length:
        raise HTTPException(status_code=404, detail="Notiz nicht gefunden.")
    
    save_notes(notes)
    return None  # 204 No Content sendet nichts zurück