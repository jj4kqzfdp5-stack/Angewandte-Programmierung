from fastapi import FastAPI, HTTPException, Depends, Query
from sqlmodel import SQLModel, Field, Session, create_engine, select, func, or_
from typing import Optional, List, Annotated
from datetime import datetime, timezone
from pydantic import BaseModel, field_validator, model_validator, ConfigDict
from typing_extensions import Self
import re

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

class Tag(SQLModel, table=True):
    """Task 5: Tighten the Tag Model"""
    # WICHTIG: validate_assignment sorgt dafür, dass Validatoren 
    # auch beim Erstellen und Ändern feuern
    model_config = ConfigDict(validate_assignment=True, str_strip_whitespace=True)

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(unique=True, index=True, min_length=2, max_length=30)

    @field_validator("name", mode="before")
    @classmethod
    def normalize_and_validate_tag_name(cls, v: str) -> str:
        if not isinstance(v, str):
            return v
        v = v.strip().lower()
        if not re.match(r"^[a-z0-9-]+$", v):
            raise ValueError("Tag name must contain only lowercase letters, digits, and dashes")
        return v

class Note(SQLModel, table=True):
    """Das Datenbank-Modell für Notizen"""
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    content: str
    category: str = "general"
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    tags_raw: str = Field(default="", description="Tags als kommagetrennter String")

    def to_dict(self):
        data = self.model_dump()
        data["tags"] = [t.strip() for t in self.tags_raw.split(",")] if self.tags_raw else []
        del data["tags_raw"]
        return data

class NoteCreate(BaseModel):
    """Task 1, 2 & 3: Strikte Validierung für neue Notizen"""
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
    
    # Task 1: Constraints (pattern entfernt, da es den TypeError verursacht)
    title: str = Field(..., min_length=3, max_length=100)
    content: str = Field(..., min_length=1, max_length=10000)
    category: str = Field(..., min_length=2, max_length=30)
    tags: List[str] = Field(default_factory=list, max_length=10)

    @field_validator("title")
    @classmethod
    def title_not_empty(cls, v: str) -> str:
        if not v.strip() or len(v.strip()) < 3:
            raise ValueError("Title must not be only whitespace and at least 3 chars")
        return v.strip()

    @field_validator("category")
    @classmethod
    def validate_category(cls, v: str) -> str:
        # Task 1 & 2: Normalisierung + Regex-Ersatz + Whitelist
        v = v.lower().strip()
        
        # Regex-Ersatz: Nur Kleinbuchstaben erlaubt (Task 1)
        if not re.match(r"^[a-z]+$", v):
            raise ValueError("Category must contain lowercase letters only")
            
        allowed = {"work", "personal", "school", "ideas", "general"}
        if v not in allowed:
            raise ValueError(f"Category must be one of {allowed}")
        return v

    @field_validator("tags")
    @classmethod
    def clean_tags(cls, v: List[str]) -> List[str]:
        cleaned = []
        seen = set()
        for t in v:
            tag = t.strip().lower()
            if not tag or len(tag) < 2:
                raise ValueError("Tags must be at least 2 chars long")
            if tag not in seen:
                cleaned.append(tag)
                seen.add(tag)
        return cleaned

    @model_validator(mode="after")
    def work_notes_need_work_tag(self) -> Self:
        if self.category == "work" and "work" not in self.tags:
            raise ValueError("work notes must include the 'work' tag")
        return self

class NoteUpdate(BaseModel):
    """Task 4: Partielle Updates mit denselben Constraints"""
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")
    
    title: Optional[str] = Field(None, min_length=3, max_length=100)
    content: Optional[str] = Field(None, min_length=1, max_length=10000)
    category: Optional[str] = Field(None, min_length=2, max_length=30)
    tags: Optional[List[str]] = Field(None, max_length=10)
    
    @field_validator("category")
    @classmethod
    def validate_category_update(cls, v: Optional[str]) -> Optional[str]:
        if v is None: return v
        v = v.lower().strip()
        if not re.match(r"^[a-z]+$", v):
            raise ValueError("Category must contain lowercase letters only")
        allowed = {"work", "personal", "school", "ideas", "general"}
        if v not in allowed:
            raise ValueError(f"Category must be one of {allowed}")
        return v

# --- 3. App Initialisierung ---
app = FastAPI(title="Note Management API v2", on_startup=[create_db_and_tables])

# --- 4. Endpunkte ---

@app.post("/notes", status_code=201)
def create_note(note_data: NoteCreate, session: SessionDep):
    db_note = Note(
        title=note_data.title,
        content=note_data.content,
        category=note_data.category,
        tags_raw=",".join(note_data.tags)
    )
    session.add(db_note)
    session.commit()
    session.refresh(db_note)
    return db_note.to_dict()

# WICHTIG: /stats MUSS vor /{note_id} stehen!
@app.get("/notes/stats")
def get_note_stats(session: SessionDep):
    notes = session.exec(select(Note)).all()
    
    cat_counts = {}
    all_tags = []
    
    for n in notes:
        cat_counts[n.category] = cat_counts.get(n.category, 0) + 1
        if n.tags_raw:
            all_tags.extend([t.strip().lower() for t in n.tags_raw.split(",")])
            
    from collections import Counter
    tag_counts = Counter(all_tags)
    
    return {
        "total_notes": len(notes),
        "by_category": cat_counts,
        "unique_tags_count": len(tag_counts),
        "top_tags": [{"tag": t, "count": c} for t, c in tag_counts.most_common(5)]
    }

@app.get("/notes")
def get_notes(session: SessionDep, category: Optional[str] = None, search: Optional[str] = None):
    statement = select(Note)
    if category:
        statement = statement.where(Note.category == category)
    if search:
        search_term = f"%{search}%"
        statement = statement.where(or_(Note.title.like(search_term), Note.content.like(search_term)))
    
    results = session.exec(statement).all()
    return [r.to_dict() for r in results]

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