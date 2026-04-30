from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime, timezone
import json
from pathlib import Path

app = FastAPI(
    title="Angewandte Programmierung",
    despription="Notizenmanagement"
    )

@app.get("/")
def root ():
    return {"message": "Hello ... World"}


@app.get("/name/{name}")
def greet_name(name: str):
    return{"message": f"Hallo {name} !"}

@app.get("/status")
def get_status():
    return{"message": "Aktueller Status: Kein Status !"}

@app.get("/berechnung")
def berechnung():
    ergebnis=3+3
    return{"message": f"Ergebnis ist {ergebnis} !"}

@app.get("/cal/{zahl1}/{zahl2}")                        #Entgegennehmen der Zahlen aus der URL
def calculation(zahl1: int, zahl2: int):                #Kopfzeile Funktion und Definition der Variablen
    ergebnis = zahl1 + zahl2                            #Berechnung
    return{"message": f"Ergebnis ist {ergebnis} !"}     #Ausgabe (f steht für formated string)

#######################################################
# Endpunkte für Notizen

class NoteCreate (BaseModel):
    title: str
    content: str

class Note(BaseModel):
    id: int
    title:str
    content: str
    created_at: str

NOTES_FILE = Path("data/notes.json")

def load_notes():
    """Load notes from JSON file and return notes list and next ID counter"""
    notes_db = []
    note_id_counter = 1

    if NOTES_FILE.exists():
        with open(NOTES_FILE, 'r') as f:
            data = json.load(f)
            notes_db = [Note(**note) for note in data]

            # Set counter to max ID + 1
            if notes_db:
                note_id_counter = max(note.id for note in notes_db) + 1

    return notes_db, note_id_counter


def save_notes(notes_db):
    """Save notes to JSON file after each change"""
    # Ensure data directory exists
    NOTES_FILE.parent.mkdir(parents=True, exist_ok=True)

    with open(NOTES_FILE, 'w') as f:
        # Convert Note objects to dicts
        notes_data = [note.dict() for note in notes_db]
        json.dump(notes_data, f, indent=2)




@app.post("/notes", status_code=201)
def create_note(note: NoteCreate) -> Note:

    """Create a new note"""

    notes_db, note_id_counter = load_notes()

    new_note = Note(

        id=note_id_counter,
        title=note.title,
        content=note.content,
        created_at=datetime.now(timezone.utc).isoformat()
    )

    notes_db.append(new_note)
    save_notes(notes_db)

    return new_note

#@app.get("/notes")
#def list_notes() -> list [Note]:
#   """Get a list of all notes"""

@app.get("/queryparameters")
def queryparameters(param1: str = None, param2: int = None) -> dict:
    """Example Entpoint query parameters"""
    
    namen = ['martin', 'sophia', 'nico']

    if not param1:
        return{"namen": namen}


    namen_gefiltert =[]
    for name in namen:
        if param1 in name:
            namen_gefiltert.append(name)


    return {
        "param1": param1,
        "param2": param2,
        "namen": namen_gefiltert
    }