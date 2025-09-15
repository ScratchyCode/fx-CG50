# Calcolatore della Corrente
# Gemini 2.5 Pro
import math

def ottieni_float(prompt):
    """Richiede un valore float all'utente."""
    return float(input(prompt))

def ottieni_coordinate(prompt):
    """Richiede all'utente gradi e minuti per una coordinata."""
    print("- {} -".format(prompt))
    deg = ottieni_float("Gradi: ")
    min_val = ottieni_float("Minuti e decimi: ")
    return deg + min_val / 60.0

def ottieni_orario(prompt):
    """Richiede all'utente un orario e lo converte in ore decimali."""
    print("--- {} ---".format(prompt))
    ore = int(ottieni_float("Ora (0-23): "))
    minuti = int(ottieni_float("Minuti (0-59): "))
    return ore + minuti / 60.0

def rotta_a_radianti(angolo_gradi):
    """Converte un angolo di navigazione (0=N) in radianti matematici."""
    angolo_mat_gradi = (450 - angolo_gradi) % 360
    return angolo_mat_gradi * (math.pi / 180.0)

def radianti_a_rotta(angolo_radianti):
    """Converte radianti matematici in un angolo di navigazione (0=N)."""
    angolo_mat_gradi = angolo_radianti * (180.0 / math.pi)
    return (450 - angolo_mat_gradi) % 360

def calcola_corrente():
    """Funzione principale per il calcolo della corrente."""
    print("- CORRENTI -")
    
    print("\nPUNTO NAVE 1")
    lat1 = ottieni_coordinate("Lat Iniziale")
    lon1 = ottieni_coordinate("Lon Iniziale")
    orario1 = ottieni_orario("Orario Partenza")
    
    print("\nNAVIGAZIONE")
    prora_vera = ottieni_float("Prora Vera: ")
    vel_propulsiva = ottieni_float("Vel prop: ")

    print("\nPUNTO NAVE 2")
    lat2 = ottieni_coordinate("Lat Finale")
    lon2 = ottieni_coordinate("Lon Finale")
    orario2 = ottieni_orario("Orario Arrivo")

    try:
        tempo_trascorso = orario2 - orario1
        if tempo_trascorso <= 0:
            raise ValueError("Tempo nullo/negativo")

        # --- Calcolo Spostamento Stimato (Dead Reckoning) ---
        prora_rad = rotta_a_radianti(prora_vera)
        distanza_stimata = vel_propulsiva * tempo_trascorso
        
        # Correzione: X (Est) usa cos, Y (Nord) usa sin con l'angolo matematico
        spostamento_stimato_x = distanza_stimata * math.cos(prora_rad)
        spostamento_stimato_y = distanza_stimata * math.sin(prora_rad)

        # --- Calcolo Spostamento Effettivo (Fix-to-Fix) ---
        mid_lat_rad = ((lat1 + lat2) / 2) * (math.pi / 180.0)
        nm_per_grado_lat = 60.0
        nm_per_grado_lon = 60.0 * math.cos(mid_lat_rad)
        
        spostamento_effettivo_x = (lon2 - lon1) * nm_per_grado_lon
        spostamento_effettivo_y = (lat2 - lat1) * nm_per_grado_lat

        # --- Calcolo Vettore Corrente ---
        vettore_corrente_x = spostamento_effettivo_x - spostamento_stimato_x
        vettore_corrente_y = spostamento_effettivo_y - spostamento_stimato_y

        distanza_corrente = math.sqrt(vettore_corrente_x**2 + vettore_corrente_y**2)
        
        if tempo_trascorso == 0:
            drift = 0
        else:
            drift = distanza_corrente / tempo_trascorso
        
        # Correzione: l'ordine corretto degli argomenti è atan2(y, x)
        set_rad = math.atan2(vettore_corrente_y, vettore_corrente_x)
        set_gradi = radianti_a_rotta(set_rad)

    except (ValueError, ZeroDivisionError) as e:
        print("\n- ERRORE -")
        print(str(e))
        return

    # --- Stampa Risultato ---
    print("\n\n- STIMA CORRENTE -")
    print("Dir: {:.1f}*".format(set_gradi))
    print("Vel: {:.2f} kn".format(drift))
    print("\n\n------------------")

# Avvia il programma principale
calcola_corrente()
