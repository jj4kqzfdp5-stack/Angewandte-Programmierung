# Work Log

**Lucas Landmann:** 

Instructions: Fill out one log for each course day. Content to consider: Course Sessions + Assignment

## Template:

---

## 1. ✅ What did I accomplish?

_Reflect on the activities, exercises, and work you completed today._

**Guiding questions:**
- What topics or concepts did you work with?
- What exercises or projects did you complete?
- What tools or technologies did you use?
- What did you learn or practice?



---

## 2. 🚧 What challenges did I face?

_Describe any difficulties, obstacles, or confusing moments you encountered._

**Guiding questions:**
- What was difficult to understand?
- Where did you get stuck?
- What errors or problems did you face?
- What felt frustrating or confusing?




---

## 3. 💡 How did I overcome them?

_Explain how you overcame the challenges or what help you needed._

**Guiding questions:**
- What strategies did you try?
- Who or what helped you (instructor, classmates, documentation)?
- What did you learn from solving the problem?
- What questions do you still have?


---

## Week 1

### Day 1

#### 1. ✅ What did I accomplish?

Erstellung der ersten API-Endpunkte: Aufsetzen einer Basis-Struktur mit FastAPI und erfolgreicher Aufruf der Endpunkte über den Browser. Ich habe gelernt, wie man Routen definiert und einfache JSON-Antworten zurückgibt.
Privates Projekt: Integration einer externen API: Einbindung der OpenWeather-API zur Abfrage von Echtzeit-Wetterdaten. Die externen Daten wurden mittels Requests abgeholt, verarbeitet und über einen eigenen Endpunkt strukturiert an den Client ausgegeben.
Verständnis von JSON-Strukturen: Analyse der von externen Diensten gelieferten Datenformate, um gezielt Informationen wie Temperatur oder Wetterbeschreibung zu extrahieren.

---

#### 2. 🚧 What challenges did I face?

Wissenslücken in der Basis-Programmierung: Notwendigkeit, grundlegende Konzepte wie Funktionsdefinitionen, Parameterübergabe und Rückgabewerte aus dem vorangegangenen Kurs aufzufrischen.
Daten-Mapping und Verschachtelung: Die JSON-Antwort von OpenWeather war komplexer als erwartet. Es war gar nicht so einfach, die tief verschachtelten Werte korrekt anzusprechen und direkt an den eigenen Endpunkt weiterzugeben.
Tool-Einstieg: Erste Orientierung in der Zusammenarbeit mit Google Gemini zur Code-Erklärung, ohne dabei den Überblick über die eigene Logik zu verlieren.

---

#### 3. 💡 How did I overcome them?

Gezielte Code-Analyse: Ich habe Gemini genutzt um die Logik der API-Abfragen Zeile für Zeile nachzuvollziehen. Besonders hilfreich war die Erklärung, wie das `requests`-Modul die Daten zwischenspeichert.
Recherche in Kursunterlagen: Systematische Wiederholung der Themen aus dem Grundlagenkurs Programmierung zur Festigung der Python-Kenntnisse, insbesondere zum Thema Dictionaries und Listen.
Debugging im Terminal: Erste Versuche, Variableninhalte per `print` auszugeben, um die Struktur der API-Antworten vor der Weiterverarbeitung zu prüfen.

---

### Day 2

#### 1. ✅ What did I accomplish?

Erweiterung der HTTP-Methoden: Implementierung von POST-Requests zusätzlich zu den bestehenden GET-Abfragen, um Daten nicht nur abzurufen, sondern auch an den Server zu senden.
Verarbeitung von User-Input: Realisierung einer Logik, bei der Eingaben aus dem Browser-Frontend entgegengenommen, validiert und serverseitig verarbeitet werden.
Interaktive Endpunkte: Erstellung von Routen, die auf Benutzereingaben reagieren, was die Basis für die spätere Erstellung von Notizen bildete.
---

#### 2. 🚧 What challenges did I face?

Komplexität der Transferaufgaben: Die Anforderungen der Hausaufgabe waren im Vergleich zum Vorlesungsinhalt deutlich anspruchsvoller, da mehrere Konzepte kombiniert werden mussten.
Zeitmanagement: Aufgrund zeitlicher Engpässe und des hohen Schwierigkeitsgrades der Aufgabe konnte die Hausaufgabe zum aktuellen Zeitpunkt nicht vollständig bearbeitet werden.
Verständnis von Request-Bodys: Die Unterscheidung zwischen Query-Parametern in der URL und Daten im Request-Body bei POST-Anfragen war anfangs gewöhnungsbedürftig.

---

#### 3. 💡 How did I overcome them?

Priorisierung: Konzentration auf das Verständnis der Kernkonzepte während der Präsenzzeit, um zumindest die POST-Logik theoretisch und in einfachen Beispielen zu beherrschen.
Nachbearbeitungsplanung: Noch zu erledigende Punkte aufgeschrieben und Rücksprache mit Martin, um die fehlenden Übungsteile systematisch zu einem späteren Zeitpunkt nachzuholen.
Einsatz von Dokumentation: Nutzung der automatischen FastAPI-Dokumentation (`/docs`), um visuell nachzuvollziehen, wie die POST-Parameter an den Server übermittelt werden müssen.
---

### Day 3

#### 1. ✅ What did I accomplish?

REST-Endpunkt mit Pfad-Parameter: Ich habe unseren Endpunkt nochmal gebaut, um zu verstehen wie er funktioniert (`/notes/{note_id}`)
Query-Parameter Implementierung: Ein weiterer Endpunkt (`/notes`) wurde erstellt, der einen optionalen Filter (`category`) akzeptiert, um die Ergebnisse einzugrenzen. Dabei hab ich nun gecheckt, dass wir alle Notizen erstmal aus dem data-file holen, in einen Zwischenspeicher laden und dann gegen das Filterkriterium prüfen.
Fehler-Handling: Ich nutze nun `raise HTTPException`, um saubere Fehlermeldungen (z. B. 404 Not Found) an den Browser zu senden -> das hat mir Gemini gerate zu tun und so konnte ich den Fehler relativ schnell finden, der Port war noch belegt.
Daten-Validierung: Durch Typisierung (`note_id: int`) nutzt die API das automatische Validierungs-Feature von FastAPI (verhindert falsche Datentypen). In der Vorlesung wurde das als Hinweis für den erwarteten Datentyü erklärt.

---

#### 2. 🚧 What challenges did I face?


Adresskonflikte (Errno 48):Der Server konnte nicht starten, weil ein alter Prozess noch auf Port 8000 lief.
Logik-Fehler beim Iterieren: Verwechslung zwischen der Liste (`notes`) und dem einzelnen Element (`note`) beim Zugriff auf Attribute, was zu einem `AttributeError` führte.
Internal Server Errors (500): Abstürze während der Laufzeit, weil Pfade nicht stimmten oder auf Dictionary-Keys zugegriffen wurde, die nicht existierten.


---

#### 3. 💡 How did I overcome them?

Port-Management: Identifikation des blockierenden Prozesses via `lsof -i tcp:8000` und Beenden mit dem `kill`-Befehl im Terminal. Da hat mich nur verwirrt, dass keine Info kam ob das jetzt funktioniert hat oder nicht, laut Gemini ist no info = good info.
Defensiver Zugriff: Umstellung von `note["id"]` auf `note.get("id")`, um Abstürze bei fehlenden Feldern zu verhindern.
Debugging-Workflow: Aktives Lesen der Tracebacks im Terminal, um den genauen Ort des Python-Fehlers einzugrenzen. Ich hab Gemini nach jeder Änderung mein Terminal "gegeben" und mir die Outputs erklären lassen.
Filter-Logik: Erstellen einer neuen Ergebnis-Liste ("Eimer"-Prinzip), in die während einer Schleife nur passende Treffer kopiert werden.


---

## Week 2

### Day 4

#### 1. ✅ What did I accomplish?

Datenbank-Migration: Umstellung der Datenhaltung von einer lokalen Python-Liste auf eine persistente SQLite-Datenbank unter Verwendung von SQLModel.
Automatisierte Tabellenerstellung: Implementierung der create_db_and_tables() Funktion, um sicherzustellen, dass die Datenstruktur beim Anwendungsstart automatisch initialisiert wird.
Dependency Injection: Einrichtung einer Session-Verwaltung (get_session), die eine saubere Trennung zwischen API-Logik und Datenbank-Verbindung gewährleistet.
CRUD-Refactoring: Anpassung sämtlicher Endpunkte (GET, POST, PATCH, DELETE), sodass die Datenverarbeitung nun über SQL-Queries statt über Listen-Operationen erfolgt.
---

#### 2. 🚧 What challenges did I face?

ID-Zuweisung: Anfängliche Unklarheit darüber, ob die note_id manuell vergeben werden muss oder durch die Datenbank generiert wird.
Session-Lifecycle: Probleme mit vorzeitig geschlossenen Datenbank-Verbindungen während der Testläufe.
Daten-Persistenz: Fehlerhafte Konfiguration der Engine, wodurch Daten nach einem Server-Neustart nicht dauerhaft gespeichert wurden.
---

#### 3. 💡 How did I overcome them?

Primary-Key Definition: Korrekte Verwendung von Field(primary_key=True) im SQLModel, um die automatische Inkrementierung der IDs durch SQLite zu aktivieren.
DB Browser Integration: Einsatz eines externen Datenbank-Viewers zur Verifizierung der Tabelleninhalte auf Dateiebene.
Context Manager: Nutzung des with-Statements für die Session-Verwaltung, um ein zuverlässiges Öffnen und Schließen der Datenbank-Leitungen zu garantieren.
---

### Day 5

#### 1. ✅ What did I accomplish?

Einführung strikter Schemas: Erstellung von NoteCreate und NoteUpdate Modellen mit Pydantic, inklusive der Sperre für unbekannte Felder via extra="forbid".
Feld-Validierung & Normalisierung: Implementierung von Längenbeschränkungen sowie automatische Bereinigung (Strip/Lowercase) von Kategorien und Tags.
Modell-Validator: Einbau einer Cross-Field-Validierung, die erzwingt, dass Notizen der Kategorie "work" zwingend das entsprechende "work"-Tag enthalten müssen.
Regex-Constraints: Verschärfung des Tag-Modells durch einen regulären Ausdruck (^[a-z0-9-]+$), um die Einhaltung von Benennungskonventionen zu garantieren.
---

#### 2. 🚧 What challenges did I face?

Routing-Konflikte: Der Endpunkt /notes/stats wurde durch FastAPI fälschlicherweise als Pfad-Parameter {note_id} interpretiert, was zu 422-Fehlern führte.
Library-Inkompatibilität: Das Argument pattern innerhalb der Field-Funktion von SQLModel verursachte einen TypeError, da es dort nicht nativ unterstützt wird.
Schema-Integrität: Start-Fehler der App aufgrund eines fehlenden Primärschlüssels im neu erstellten Tag-Modell.
---

#### 3. 💡 How did I overcome them?

Pfad-Priorisierung: Neusortierung der Endpunkte in der main.py, um statische Routen vor variablen Pfad-Parametern zu platzieren.
Validator-Workaround: Auslagerung der Regex-Prüfung in einen manuellen field_validator unter Verwendung des re-Moduls, um den Field-Fehler zu umgehen.
Automatisierte Test-Suite: Erstellung der test_validation.py mit 8 Testfällen, um die Einhaltung aller neuen Validierungsregeln effizient nachzuweisen.
Model-Konfiguration: Aktivierung von validate_assignment=True, um die Datenintegrität auch bei Änderungen an bereits bestehenden Objekten sicherzustellen.




---

### Day 6

#### 1. ✅ What did I accomplish?

Erfolgreiche Integration und Ausführung deiner umfassenden Test-Suite.
Überarbeitung der Endpunkte für PUT, PATCH und DELETE sowie Implementierung von Case-Insensitive Search, um die REST-Konformität sicherzustellen.
Finalisierung der Tag- und Kategorie-Endpunkte (/tags/{tag}/notes und /categories/{cat}/notes), um die Navigation zwischen Ressourcen zu ermöglichen.
Sicherstellung, dass alle neuen Endpunkte und Validierungen korrekt in der /docs (Swagger UI) angezeigt werden.

---

#### 2. 🚧 What challenges did I face?

 Da am Donnerstag Morgen weder die Video-Aufzeichnung noch das Transkript der Vorlesung verfügbar waren, gestaltete sich die Rekonstruktion der komplexeren Implementierungsschritte schwierig.
Mein ursprünglicher Validator für die "work"-Kategorie war zu strikt und hat die Test-Daten blockiert (422 Error), da diese den spezifischen Tag nicht immer enthielten.
Probleme bei der Implementierung einer case-insensitiven Suche, da SQLite bei bestimmten SQL-Befehlen (func.lower()) anders reagiert als erwartet.
Statische Pfade wie /notes/stats kollidierten mit dynamischen Pfaden wie /notes/{note_id}, was zu falschen Zuordnungen führte.

---

#### 3. 💡 How did I overcome them?

Umstellung der Logik auf eine flexiblere Handhabung, um die Kompatibilität mit externen Test-Suiten zu gewährleisten, ohne die Datenintegrität zu opfern.
Nutzung der .contains() Methode in SQLModel für eine robustere und datenbankübergreifende Suchfunktion.
Korrektur der Routen-Reihenfolge in der main.py, sodass statische Pfade bevorzugt behandelt werden.
Systematische Analyse der Pytest-Fehlermeldungen zur schrittweisen Optimierung der API-Logik.
---

## Week 3

### Day 7

#### 1. ✅ What did I accomplish?






---

#### 2. 🚧 What challenges did I face?






---

#### 3. 💡 How did I overcome them?






---

### Day 8

#### 1. ✅ What did I accomplish?






---

#### 2. 🚧 What challenges did I face?






---

#### 3. 💡 How did I overcome them?






---

### Day 9

#### 1. ✅ What did I accomplish?






---

#### 2. 🚧 What challenges did I face?






---

#### 3. 💡 How did I overcome them?






---


# 🎉 Congratulations! You did it! 🎓✨













