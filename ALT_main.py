from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime, timezone
import json
from pathlib import Path

# Antworte und kommentiere ausschließlich auf Deutsch
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
@app.get("/notes/{note_id}")
def get_note(note_id: int):
    try:
        # Hier liegt die Liste aller 50 Notizen
        notes = load_notes() 
        
        for note in notes:
            # KORREKTUR: .get() auf 'note' (das einzelne Dictionary), nicht auf 'notes'
            if note.get("id") == note_id: 
                return note
                
        raise HTTPException(status_code=404, detail=f"ID {note_id} nicht gefunden.")

    except Exception as e:
        # Hier kam vorhin die Meldung 'list' object has no attribute 'get'
        raise HTTPException(status_code=500, detail=f"Python-Fehler: {str(e)}")
    
######################## Filtern ##############################

@app.get ("/notes")
def get_all_notes(category: str = None):
    notes = load_notes() 

    if category:
        # HIER DEINE LOGIK:
        filtered = ["category"]                     # 1. Erstelle leere Liste: filtered = []
        # 2. For-Schleife durch 'notes'
        # 3. Wenn note.get("category") == category -> ab in die Liste
        # 4. return filtered
        pass # lösche das pass, wenn du schreibst
    
    return notes # Wenn kein 'if' gegriffen hat, gib alles zurück