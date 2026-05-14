import time
from coppeliasim_zmqremoteapi_client import RemoteAPIClient

# --- INITIALISIERUNG ---
client = RemoteAPIClient()
sim = client.getObject('sim')

# Handles für die Objekte in CoppeliaSim (müssen dort so benannt sein!)
# Beispiel: Ein Sensor und ein Motor für die Schranke
try:
    sensor_ticket = sim.getObject('/TicketSensor')
    motor_schranke = sim.getObject('/SchrankenMotor')
except:
    print("Warnung: Objekte in CoppeliaSim noch nicht angelegt.")

# --- SCHRITTKETTE (GRAFCET) ---
step = "IDLE"
sim.startSimulation()

try:
    while True:
        # 1. Eingänge lesen (Sensor-Simulation)
        # Beispiel: Ein einfacher Annäherungssensor
        # result, distance, detectedPoint, detectedObjectHandle, detectedSurfaceNormalVector = sim.readProximitySensor(sensor_ticket)
        
        # 2. Logik (Schrittkette)
        match step:
            case "IDLE":
                # Warte auf Ticket (hier als Tastendruck oder Sensor)
                print("Status: Warte auf Auto...")
                # Wenn Sensor ausgelöst -> step = "OEFFNEN"
                time.sleep(1) 
                
            case "OEFFNEN":
                # Befehl an Motor: Schranke hoch
                # sim.setJointTargetVelocity(motor_schranke, 0.5)
                pass

        # Kurze Pause für die CPU
        time.sleep(0.05)

except KeyboardInterrupt:
    # Sauberes Beenden bei Strg+C in VS Code
    sim.stopSimulation()
    print("Simulation beendet.")