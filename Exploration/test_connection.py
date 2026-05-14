try:
    from coppeliasim_zmqremoteapi_client import RemoteAPIClient
    print("✅ Bibliothek erfolgreich geladen.")
except ImportError:
    print("❌ Fehler: Bibliothek 'coppeliasim-zmqremoteapi-client' nicht gefunden.")
    exit()

def test_bridge():
    try:
        # Verbindung aufbauen
        client = RemoteAPIClient()
        sim = client.getObject('sim')
        
        print("🔗 Verbinde mit CoppeliaSim...")
        
        # Test: Simulation starten
        sim.startSimulation()
        print("🚀 Simulation gestartet!")
        
        # 2 Sekunden warten (Simulationszeit abfragen)
        time_start = sim.getSimulationTime()
        import time
        time.sleep(20)
        time_end = sim.getSimulationTime()
        
        print(f"⏱ Simulationszeit vergangen: {time_end - time_start:.2f}s")
        
        # Test: Simulation stoppen
        sim.stopSimulation()
        print("⏹ Simulation gestoppt!")
        print("\n🎉 TEST ERFOLGREICH! VS Code und CoppeliaSim sprechen miteinander.")
        
    except Exception as e:
        print(f"❌ Verbindung fehlgeschlagen: {e}")
        print("Tipp: Läuft CoppeliaSim im Hintergrund?")

if __name__ == "__main__":
    test_bridge()