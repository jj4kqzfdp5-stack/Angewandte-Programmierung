# API Project

# Note Management System (API Project)

## Projektbeschreibung

Dieses Projekt implementiert eine vollständige REST-API zur Verwaltung von Notizen mit einem zusätzlichen Frontend zur Visualisierung der Daten.

Die Anwendung ermöglicht:

- Erstellen von Notizen
- Abrufen einzelner oder aller Notizen
- Filtern nach Kategorie, Tags und Suchbegriffen
- Bearbeiten und Löschen von Notizen
- Anzeigen von Statistiken
- Speicherung der Daten in einer SQLite-Datenbank

Zusätzlich wurde ein Frontend mit Streamlit entwickelt, das die API nutzt und vorhandene Notizen übersichtlich darstellt.

Das Projekt basiert auf modernen Python-Technologien und orientiert sich an REST-Prinzipien.

---

# Verwendete Technologien

- **FastAPI** – REST-API Framework
- **SQLModel** – ORM und Datenbankmodellierung
- **SQLite** – Persistente Datenbank
- **Pydantic** – Datenvalidierung
- **Streamlit** – Frontend
- **Pytest** – Automatisierte Tests

---

# Installation & Start der Applikation

Zum Starten des Projekts wird der Python-Package-Manager `uv` benötigt.

## 1. Projekt herunterladen

```bash
git clone <repository-url>
cd <projektordner>
```

---

## 2. Backend starten

Im Hauptverzeichnis folgenden Befehl ausführen:

```bash
uv run fastapi dev main.py
```

Die API läuft anschließend unter:

```text
http://127.0.0.1:8000
```

Die Swagger-Dokumentation befindet sich unter:

```text
http://127.0.0.1:8000/docs
```

---

## 3. Frontend starten

Ein zweites Terminal öffnen und folgenden Befehl ausführen:

```bash
uv run streamlit run frontend.py
```

---

## 4. Tests ausführen

Die Test-Suite überprüft die API automatisch gegen die Referenz-Implementierung.

```bash
uv run pytest test_main.py -v
```

---

# Nutzung der App

Nach dem Start des Frontends werden alle vorhandenen Notizen automatisch aus der API geladen.

## Funktionen des Frontends

### Übersicht aller Notizen

In der Sidebar werden alle vorhandenen Notiz-Titel angezeigt.

### Detailansicht

Nach Auswahl einer Notiz werden folgende Informationen dargestellt:

- Titel
- Kategorie
- Erstellungsdatum
- Inhalt
- Tags

### Entwickleransicht

Zusätzlich können die Rohdaten der API angezeigt werden.

---

# Beispiel-Durchlauf der API

Im folgenden Abschnitt wird gezeigt, wie eine Notiz erstellt und anschließend wieder abgerufen werden kann.

---

## 1. Notiz anlegen (POST Request)

```python
import requests

payload = {
    "title": "Projekt-Abgabe",
    "content": "Alle Dateien auf GitHub hochladen und Readme prüfen.",
    "category": "work",
    "tags": ["urgent"]
}

response = requests.post(
    "http://127.0.0.1:8000/notes",
    json=payload
)

print(response.json())
```

### Beispiel-Ausgabe

```json
{
    "id": 1,
    "title": "Projekt-Abgabe",
    "content": "Alle Dateien auf GitHub hochladen und Readme prüfen.",
    "category": "work",
    "created_at": "2026-05-14T12:00:00+00:00",
    "tags": [
        "urgent",
    ]
}
```

---

## 2. Alle Notizen abrufen (GET Request)

```python
import requests

response = requests.get("http://127.0.0.1:8000/notes")

notes = response.json()

for note in notes:
    print(f"ID: {note['id']} - Titel: {note['title']}")
```

### Beispiel-Ausgabe

```text
ID: 1 - Titel: Projekt-Abgabe
```

---

## 3. Notizen nach Kategorie filtern

```python
import requests

response = requests.get(
    "http://127.0.0.1:8000/notes",
    params={"category": "work"}
)

print(response.json())
```

---

# Wichtige API-Endpunkte

| Methode | Endpoint | Beschreibung |
|---|---|---|
| GET | `/` | API Startseite |
| POST | `/notes` | Neue Notiz erstellen |
| GET | `/notes` | Alle Notizen abrufen |
| GET | `/notes/{id}` | Einzelne Notiz abrufen |
| PATCH | `/notes/{id}` | Notiz teilweise bearbeiten |
| PUT | `/notes/{id}` | Notiz vollständig ersetzen |
| DELETE | `/notes/{id}` | Notiz löschen |
| GET | `/notes/stats` | Statistik abrufen |
| GET | `/categories` | Kategorien abrufen |
| GET | `/tags` | Tags abrufen |

---

# Projektstruktur

```text
.
├── main.py
├── frontend.py
├── test_main.py
├── data/
│   └── notes.db
└── README.md
```

---

# Tests

Die Anwendung enthält eine vollständige automatisierte Test-Suite mit Pytest.

Geprüft werden unter anderem:

- Erstellen von Notizen
- Abrufen einzelner Notizen
- Filterfunktionen
- Tag-Normalisierung
- Fehlerbehandlung
- Statistik-Endpunkte

Testausführung:

```bash
uv run pytest test_main.py -v
```

---

# Verwendete Bibliotheken

- **FastAPI** – Erstellung der REST-API
- **SQLite** – Persistente Datenbank
- **Pydantic** – Validierung der Eingabedaten
- **Streamlit** – Frontend-Oberfläche
- **Requests** – HTTP-Anfragen an die API
- **Pytest** – Automatisierte API-Tests