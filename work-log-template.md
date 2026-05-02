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

- erste API Endpunkte erstellt und im Browser aufgerufen
- Einbindung der openweather API und ausgabe über eigenen Endpunkt



---

#### 2. 🚧 What challenges did I face?

- ich musste meine Kentnisse aus dem Grundlagen Programmierung Kurs etwas auffrischen zum Thema Funktionen
- die Daten von openweather abzuholen und direkt an den eigenen Enpunkt weiterzugegeb, war gar nicht so einfach
- Gemini hat ganz gut geholfen ;)




---

#### 3. 💡 How did I overcome them?

- Gemini gefragt und mir den Code Zeile für Zeile erklären lassen (vor allem bei der openweather API)
- Unterlagen vom Grundlagenkurs nochmal durchgelesen




---

### Day 2

#### 1. ✅ What did I accomplish?

- nicht nur get sondern auch poast
- Eingaben im Browser werden auch verarbeitet




---

#### 2. 🚧 What challenges did I face?

- Aufgabe der Hausaufgabe fand ich schwierig
- habs aus Zeitmangel nicht gemacht



---

#### 3. 💡 How did I overcome them?


/



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






---

#### 2. 🚧 What challenges did I face?






---

#### 3. 💡 How did I overcome them?






---

### Day 5

#### 1. ✅ What did I accomplish?






---

#### 2. 🚧 What challenges did I face?






---

#### 3. 💡 How did I overcome them?






---

### Day 6

#### 1. ✅ What did I accomplish?






---

#### 2. 🚧 What challenges did I face?






---

#### 3. 💡 How did I overcome them?






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













