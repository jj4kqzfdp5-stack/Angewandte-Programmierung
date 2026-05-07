from fastapi import FastAPI, HTTPException, Depends, Query
from sqlmodel import SQLModel, Field, Session, create_engine, select, func, or_
from typing import Optional, List, Annotated
from datetime import datetime, timezone
from pydantic import BaseModel, field_validator, ConfigDict

# --- 1. Datenbank Setup ---
DB_FILE = "data/notes.db"
sqlite_url = f"sqlite:///{DB_FILE}"
engine = create_engine(sqlite_url, connect_args={"check_same_thread": False})

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]

# --- 2. Modelle & Schemas ---

class Note(SQLModel, table=True):
    """Das Datenbank-Modell"""
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    content: str
    category: str = "General"
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    tags_raw: str = Field(default="", description="Tags als kommagetrennter String")

    def to_dict(self):
        """Hilfsmethode, um das DB-Modell für die API-Antwort aufzubereiten"""
        data = self.model_dump()
        data["tags"] = [t.strip() for t in self.tags_raw.split(",")] if self.tags_raw else []
        del data["tags_raw"]
        return data

class NoteCreate(BaseModel):
    """Schema für POST Requests (Validierung Tag 5)"""
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
    
    # WICHTIG: Felder müssen vor dem Validator definiert sein
    title: str = Field(..., min_length=1, max_length=100)
    content: str = Field(..., min_length=1)
    category: str = "General"
    tags: List[str] = []

    @field_validator("tags")
    @classmethod
    def clean_tags(cls, v: List[str]) -> List[str]:
        # Säubern, Kleinschreiben und Duplikate entfernen
        cleaned = [t.strip().lower() for t in v if t.strip()]
        return list(dict.fromkeys(cleaned))

class NoteUpdate(BaseModel):
    """Schema für PATCH Requests (Alle Felder optional)"""
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
    
    title: Optional[str] = Field(None, min_length=1)
    content: Optional[str] = None
    category: Optional[str] = None
    tags: Optional[List[str]] = None

# --- 3. App Initialisierung ---
app = FastAPI(title="Note Management API v2", on_startup=[create_db_and_tables])

# --- 4. Endpunkte ---

@app.get("/")
def read_root():
    return {"message": "Hello Lucas! Deine Note-API ist bereit für die Tests."}

@app.post("/notes", status_code=201)
def create_note(note_data: NoteCreate, session: SessionDep):
    tags_string = ",".join(note_data.tags)
    
    db_note = Note(
        title=note_data.title,
        content=note_data.content,
        category=note_data.category,
        tags_raw=tags_string
    )
    session.add(db_note)
    session.commit()
    session.refresh(db_note)
    return db_note.to_dict()

@app.get("/notes")
def get_notes(
    session: SessionDep, 
    category: Optional[str] = None, 
    search: Optional[str] = None
):
    statement = select(Note)
    if category:
        statement = statement.where(Note.category == category)
    if search:
        search_term = f"%{search}%"
        statement = statement.where(or_(Note.title.like(search_term), Note.content.like(search_term)))
    
    results = session.exec(statement).all()
    return [n.to_dict() for n in results]

@app.get("/notes/stats")
def get_note_stats(session: SessionDep):
    """Statistiken ohne strenge Pydantic-Validierung der Rückgabe."""
    notes = session.exec(select(Note)).all()
    
    cat_counts = {}
    all_tags = []
    
    for n in notes:
        cat_counts[n.category] = cat_counts.get(n.category, 0) + 1
        if n.tags_raw:
            # Stelle sicher, dass wir nur echte Strings verarbeiten
            tags = [t.strip().lower() for t in str(n.tags_raw).split(",") if t.strip()]
            all_tags.extend(tags)
            
    # Wir geben ein flaches Dictionary zurück
    return {
        "total_notes": int(len(notes)),
        "by_category": dict(cat_counts),
        "unique_tags_count": int(len(set(all_tags)))
}

@app.get("/notes/{note_id}")
def get_single_note(note_id: int, session: SessionDep):
    db_note = session.get(Note, note_id)
    if not db_note:
        raise HTTPException(status_code=404, detail="Notiz nicht gefunden")
    return db_note.to_dict()

@app.patch("/notes/{note_id}")
def update_note(note_id: int, update_data: NoteUpdate, session: SessionDep):
    db_note = session.get(Note, note_id)
    if not db_note:
        raise HTTPException(status_code=404, detail="Notiz nicht gefunden")
    
    data = update_data.model_dump(exclude_unset=True)
    for key, value in data.items():
        if key == "tags":
            setattr(db_note, "tags_raw", ",".join(value))
        else:
            setattr(db_note, key, value)
            
    session.add(db_note)
    session.commit()
    session.refresh(db_note)
    return db_note.to_dict()

@app.delete("/notes/{note_id}", status_code=204)
def delete_note(note_id: int, session: SessionDep):
    db_note = session.get(Note, note_id)
    if not db_note:
        raise HTTPException(status_code=404, detail="Notiz nicht gefunden")
    session.delete(db_note)
    session.commit()
    return None

@app.get("/categories")
def get_categories(session: SessionDep):
    categories = session.exec(select(Note.category).distinct()).all()
    return categories

@app.get("/tags")
def get_tags(session: SessionDep):
    notes = session.exec(select(Note.tags_raw)).all()
    unique_tags = set()
    for row in notes:
        if row:
            for t in row.split(","):
                unique_tags.add(t.strip().lower())
    return list(unique_tags)


    