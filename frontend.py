# Streamlit installieren
# Streamlit Hello World erstellen und testen
# say nö app erstellen und testen (mit no as a service)
# Button in Streamlit, der bei klick die anfrage and die api sendet

# Hausaufgabe:
# Stramlit app mit 2 funktionen für Notizen APi (anzeigen, Liste mit Titel, )


import streamlit as st
import requests

# Deine API-URL aus der main.py
API_BASE_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="Notizen API Frontend", page_icon="📝")

st.title("📝 Notizen Management")

# --- Funktionen, die deine API-Endpunkte aufrufen ---

def fetch_all_notes():
    """Nutzt den GET /notes Endpunkt deiner API"""
    try:
        response = requests.get(f"{API_BASE_URL}/notes")
        if response.status_code == 200:
            return response.json()
        return []
    except Exception as e:
        st.error(f"Verbindung zur API (main.py) fehlgeschlagen: {e}")
        return []

def fetch_note_details(note_id):
    """Nutzt den GET /notes/{id} Endpunkt deiner API"""
    response = requests.get(f"{API_BASE_URL}/notes/{note_id}")
    if response.status_code == 200:
        return response.json()  
    return None

# --- Hausaufgabe Teil 1: Liste mit Titeln anzeigen ---

st.sidebar.header("Notizen Übersicht")
all_notes = fetch_all_notes()

if not all_notes:
    st.sidebar.info("Keine Notizen in der Datenbank gefunden.")
else:
    # Erstellt ein Wörterbuch {Titel: ID} für die Auswahl
    note_options = {n["title"]: n["id"] for n in all_notes}
    selected_title = st.sidebar.selectbox("Wähle eine Notiz:", list(note_options.keys()))

    # --- Hausaufgabe Teil 2: Notiz anzeigen (Details) ---
    
    if selected_title:
        note_id = note_options[selected_title]
        details = fetch_note_details(note_id)

        if details:
            st.header(details['title'])
            
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**Kategorie:** `{details['category']}`")
            with col2:
                st.write(f"**Datum:** {details['created_at'][:10]}")

            st.divider()
            st.write("**Inhalt:**")
            st.info(details['content'])
            
            if details.get('tags'):
                st.write("**Tags:**")
                # Zeigt die Tags schön als kleine Badges an
                tags_str = " ".join([f"`{t}`" for t in details['tags']])
                st.markdown(tags_str)

# Debug Bereich zur Kontrolle
with st.expander('API Rohdaten (Entwickler-Ansicht)'):
    st.json(all_notes)