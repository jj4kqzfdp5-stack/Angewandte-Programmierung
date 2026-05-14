from fastapi import FastAPI, HTTPException, Depends
from sqlmodel import SQLModel, Field, Session, create_engine, select, func, or_
from typing import Optional, List, Annotated
from datetime import datetime, timezone

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

# --- 2. Modelle ---
class Note(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    content: str
    category: str = "General"
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    tags_raw: str = Field(default="", description="Tags als kommagetrennter String")

class NoteCreate(SQLModel): # Reines Daten-Schema für den Request
    title: str
    content: str
    category: str = "General"
    tags: List[str] = []

# --- 3. App Initialisierung ---
app = FastAPI(title="Note Management API v2", on_startup=[create_db_and_tables])

# --- 4. Endpunkte ---

@app.post("/notes", status_code=201, response_model=Note)
def create_note(note_in: NoteCreate, session: SessionDep):
    # Logik: Tags-Liste sauber säubern und als String speichern
    tags_string = ",".join([t.strip() for t in note_in.tags]) if note_in.tags else ""
    
    db_note = Note(
        title=note_in.title,
        content=note_in.content,
        category=note_in.category,
        tags_raw=tags_string
    )
    session.add(db_note)
    session.commit()
    session.refresh(db_note)
    return db_note

@app.get("/notes", response_model=List[Note])
def get_notes(session: SessionDep, category: Optional[str] = None, search: Optional[str] = None):
    statement = select(Note)
    if category:
        statement = statement.where(Note.category == category)
    if search:
        search_term = f"%{search}%"
        statement = statement.where(or_(Note.title.like(search_term), Note.content.like(search_term)))
    
    return session.exec(statement).all()

@app.get("/notes/stats")
def get_note_stats(session: SessionDep):
    """Hausaufgabe Tag 3: Statistiken berechnen"""
    # Alle Notizen für Tag-Extraktion holen (pragmatischer Ansatz)
    notes = session.exec(select(Note)).all()
    
    # Kategorien-Zählung via SQL
    cat_counts = session.exec(select(Note.category, func.count(Note.id)).group_by(Note.category)).all()
    
    all_tags = []
    for n in notes:
        if n.tags_raw:
            all_tags.extend([t.strip() for t in n.tags_raw.split(",")])
    
    from collections import Counter
    tag_counts = Counter(all_tags)
    
    return {
        "total_notes": len(notes),
        "by_category": {cat: count for cat, count in cat_counts},
        "top_tags": [{"tag": t, "count": c} for t, c in tag_counts.most_common(5)],
        "unique_tags_count": len(tag_counts)
    }

@app.delete("/notes/{note_id}", status_code=204)
def delete_note(note_id: int, session: SessionDep):
    note = session.get(Note, note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Notiz nicht gefunden")
    session.delete(note)
    session.commit()
    return None