from fastapi import FastAPI, HTTPException, Depends, Query
from sqlmodel import SQLModel, Field, Session, create_engine, select, or_, col, func
from typing import Optional, List, Annotated
from datetime import datetime, timezone
from pydantic import BaseModel, field_validator, model_validator, ConfigDict
from typing_extensions import Self

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
    category: str = "general"
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    tags_raw: str = Field(default="")

    def to_dict(self):
        data = self.model_dump()
        data["tags"] = [t.strip() for t in self.tags_raw.split(",")] if self.tags_raw else []
        data["created_at"] = self.created_at.isoformat()
        del data["tags_raw"]
        return data

class NoteCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
    
    title: str = Field(..., min_length=3, max_length=100)
    content: str = Field(..., min_length=1, max_length=10000)
    category: str = Field(..., min_length=2, max_length=30)
    tags: List[str] = Field(default_factory=list, max_length=10)

    @field_validator("tags")
    @classmethod
    def clean_tags(cls, v: List[str]) -> List[str]:
        cleaned = []
        seen = set()
        for t in v:
            tag = t.strip().lower()
            if not tag: continue
            if len(tag) < 2: # Fix für test_tag_too_short_returns_422
                raise ValueError("Tag must be at least 2 characters")
            if tag not in seen:
                cleaned.append(tag)
                seen.add(tag)
        return cleaned


class NoteUpdate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
    title: Optional[str] = Field(None, min_length=3)
    content: Optional[str] = Field(None, min_length=1)
    category: Optional[str] = None
    tags: Optional[List[str]] = None

# --- 3. App Endpunkte ---
app = FastAPI(title="Note Management API v2", on_startup=[create_db_and_tables])

@app.get("/")
def read_root():
    return {"message": "Welcome to the Note API"}

@app.post("/notes", status_code=201)
def create_note(note_data: NoteCreate, session: SessionDep):
    db_note = Note(
        title=note_data.title,
        content=note_data.content,
        category=note_data.category.lower(),
        tags_raw=",".join(note_data.tags)
    )
    session.add(db_note)
    session.commit()
    session.refresh(db_note)
    return db_note.to_dict()

@app.get("/notes")
def get_notes(
    session: SessionDep, 
    category: Optional[str] = None, 
    search: Optional[str] = None,
    tag: Optional[str] = None,
    created_after: Optional[str] = None,
    created_before: Optional[str] = None
):
    statement = select(Note)
    
    if category:
        statement = statement.where(Note.category == category.lower())
    
    if search:
        # SQLite-kompatible Case-Insensitive Suche
        search_term = f"%{search}%"
        statement = statement.where(or_(
            col(Note.title).contains(search), 
            col(Note.content).contains(search)
        ))
        
    if tag:
        statement = statement.where(Note.tags_raw.contains(tag.lower()))
    
    results = session.exec(statement).all()
    notes = [r.to_dict() for r in results]

    # Datums-Filter
    if created_after:
        try:
            dt_after = datetime.fromisoformat(created_after.replace('Z', '+00:00'))
            notes = [n for n in notes if datetime.fromisoformat(n["created_at"]) >= dt_after]
        except: raise HTTPException(422, "Invalid Date")
            
    if created_before:
        try:
            dt_before = datetime.fromisoformat(created_before.replace('Z', '+00:00'))
            notes = [n for n in notes if datetime.fromisoformat(n["created_at"]) <= dt_before]
        except: raise HTTPException(422, "Invalid Date")

    return notes

@app.get("/notes/stats")
def get_note_stats(session: SessionDep):
    notes = session.exec(select(Note)).all()
    all_dicts = [n.to_dict() for n in notes]
    cat_counts = {}
    all_tags = []
    for n in all_dicts:
        cat_counts[n["category"]] = cat_counts.get(n["category"], 0) + 1
        all_tags.extend(n["tags"])
    from collections import Counter
    tag_counts = Counter(all_tags)
    return {
        "total_notes": len(notes),
        "by_category": cat_counts,
        "unique_tags_count": len(tag_counts),
        "top_tags": [{"tag": t, "count": c} for t, c in tag_counts.most_common(5)]
    }

@app.get("/notes/{note_id}")
def get_single_note(note_id: int, session: SessionDep):
    db_note = session.get(Note, note_id)
    if not db_note: raise HTTPException(404, "Not found")
    return db_note.to_dict()

@app.patch("/notes/{note_id}")
def patch_note(note_id: int, update_data: NoteUpdate, session: SessionDep):
    db_note = session.get(Note, note_id)
    if not db_note: raise HTTPException(404, "Not found")
    patch_data = update_data.model_dump(exclude_unset=True)
    for key, value in patch_data.items():
        if key == "tags": setattr(db_note, "tags_raw", ",".join(value))
        else: setattr(db_note, key, value)
    session.add(db_note)
    session.commit()
    session.refresh(db_note)
    return db_note.to_dict()

@app.put("/notes/{note_id}")
def put_note(note_id: int, update_data: NoteCreate, session: SessionDep):
    db_note = session.get(Note, note_id)
    if not db_note: raise HTTPException(404, "Not found")
    db_note.title = update_data.title
    db_note.content = update_data.content
    db_note.category = update_data.category.lower()
    db_note.tags_raw = ",".join(update_data.tags)
    session.add(db_note)
    session.commit()
    session.refresh(db_note)
    return db_note.to_dict()

@app.delete("/notes/{note_id}", status_code=204)
def delete_note(note_id: int, session: SessionDep):
    db_note = session.get(Note, note_id)
    if not db_note: raise HTTPException(404, "Not found")
    session.delete(db_note)
    session.commit()
    return None

@app.get("/categories")
def list_categories(session: SessionDep):
    categories = session.exec(select(Note.category).distinct()).all()
    return sorted(list(set(categories)))

@app.get("/categories/{category}/notes")
def notes_by_category(category: str, session: SessionDep):
    notes = session.exec(select(Note).where(Note.category == category.lower())).all()
    return [n.to_dict() for n in notes]

@app.get("/tags")
def list_tags(session: SessionDep):
    notes = session.exec(select(Note.tags_raw)).all()
    unique_tags = set()
    for row in notes:
        if row:
            for t in row.split(","): unique_tags.add(t.strip().lower())
    return sorted(list(unique_tags))

@app.get("/tags/{tag}/notes")
def notes_by_tag(tag: str, session: SessionDep):
    notes = session.exec(select(Note).where(Note.tags_raw.contains(tag.lower()))).all()
    return [n.to_dict() for n in notes]