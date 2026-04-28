from fastapi import FastAPI

app = FastAPI()

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