# Calcolatore Rotta di Intercettazione
# Gemini 2.5 Pro
import math

def ottieni_coordinate(prompt):
    """Richiede all'utente gradi e minuti per una coordinata."""
    print("- {} -".format(prompt))
    deg = int(input("Gradi: "))
    min_val = float(input("Minuti e decimi: "))
    return deg + min_val / 60.0

def gradi_a_dms_str(gradi_decimali):
    """Converte gradi decimali in una stringa Gradi° Minuti'."""
    if gradi_decimali is None: return "N/A"
    negativo = gradi_decimali < 0
    gradi_decimali = abs(gradi_decimali)
    gradi = int(gradi_decimali)
    minuti = (gradi_decimali - gradi) * 60
    segno_str = "-" if negativo else ""
    return "{}{}* {:.1f}'".format(segno_str, gradi, minuti)

def rotta_a_radianti(angolo_gradi):
    """Converte un angolo di navigazione (0=N) in radianti matematici."""
    angolo_mat_gradi = (450 - angolo_gradi) % 360
    return angolo_mat_gradi * (math.pi / 180.0)

def radianti_a_rotta(angolo_radianti):
    """Converte radianti matematici in un angolo di navigazione (0=N)."""
    angolo_mat_gradi = angolo_radianti * (180.0 / math.pi)
    return (450 - angolo_mat_gradi) % 360

def calcola_intercettazione():
    print("ROTTA INTERCETTA")
    
    # --- Raccolta Input ---
    print("\nPOS. TARGET")
    t_lat = ottieni_coordinate("Lat Target")
    t_lon = ottieni_coordinate("Lon Target")
    
    print("\nCORRENTE")
    c_set_gradi = float(input("Dir Corrente: "))
    c_dft = float(input("Vel Corrente: "))
    
    print("\nMOTO PROP TARGET")
    print("(0 se alla deriva)")
    t_crs_acqua_gradi = float(input("Rotta Target: "))
    t_spd_acqua = float(input("Vel Target: "))
    
    print("\nPOS E VEL MIA")
    u_lat = ottieni_coordinate("Mia Lat")
    u_lon = ottieni_coordinate("Mia Lon")
    u_spd = float(input("Mia vel prop: "))

    try:
        # --- Calcoli ---
        mid_lat_rad = (u_lat + t_lat) / 2 * (math.pi / 180.0)
        nm_per_grado_lat = 60.0
        nm_per_grado_lon = 60.0 * math.cos(mid_lat_rad)
        
        delta_lon = (t_lon - u_lon) * nm_per_grado_lon
        delta_lat = (t_lat - u_lat) * nm_per_grado_lat
        
        t_rad_acqua = rotta_a_radianti(t_crs_acqua_gradi)
        # Inversione di sin e cos per un calcolo fisicamente corretto
        t_vx_acqua = t_spd_acqua * math.cos(t_rad_acqua) # <-- CORRETTO
        t_vy_acqua = t_spd_acqua * math.sin(t_rad_acqua) # <-- CORRETTO
        
        c_rad = rotta_a_radianti(c_set_gradi)
        # Inversione di sin e cos per un calcolo fisicamente corretto
        c_vx = c_dft * math.cos(c_rad) # <-- CORRETTO
        c_vy = c_dft * math.sin(c_rad) # <-- CORRETTO
        
        t_vx_fondo = t_vx_acqua + c_vx
        t_vy_fondo = t_vy_acqua + c_vy
        
        vrx = t_vx_acqua
        vry = t_vy_acqua
        
        A = vrx**2 + vry**2 - u_spd**2
        B = 2 * (delta_lon * vrx + delta_lat * vry)
        C = delta_lon**2 + delta_lat**2
        
        if abs(A) < 1e-9: A = 1e-9
        discriminante = B**2 - 4 * A * C
        if discriminante < 0: raise ValueError("Interc. imposs.")
        
        t1 = (-B + math.sqrt(discriminante)) / (2 * A)
        t2 = (-B - math.sqrt(discriminante)) / (2 * A)
        
        tti = -1
        if t1 > 0 and t2 > 0: tti = min(t1, t2)
        elif t1 > 0: tti = t1
        elif t2 > 0: tti = t2
        else: raise ValueError("Nessuna soluz. valida")

        u_vx_acqua = (delta_lon / tti) + vrx
        u_vy_acqua = (delta_lat / tti) + vry
        
        # Correzione ordine argomenti: atan2(y, x)
        cts_rad = math.atan2(u_vy_acqua, u_vx_acqua) # <-- CORRETTO
        cts_gradi = radianti_a_rotta(cts_rad)
        
        tti_ore = int(tti)
        tti_minuti = (tti * 60) % 60
        
        spostamento_lon_nm = t_vx_fondo * tti
        spostamento_lat_nm = t_vy_fondo * tti
        
        intercetto_lat_dec = t_lat + (spostamento_lat_nm / nm_per_grado_lat)
        intercetto_lon_dec = t_lon + (spostamento_lon_nm / nm_per_grado_lon)

    except (ValueError, ZeroDivisionError) as e:
        print("\n- ERRORE -")
        print(str(e))
        return

    # --- Stampa Risultati ---
    print("\n\n- RISULTATO -")
    print("Segui ProraV: {:.1f}*".format(cts_gradi))
    print("ETA: {}h {}m".format(tti_ore, int(tti_minuti)))
    print("-----------------")
    print("Punto Interc:")
    print("  Lat: {}".format(gradi_a_dms_str(intercetto_lat_dec)))
    print("  Lon: {}".format(gradi_a_dms_str(intercetto_lon_dec)))

# --- Avvia il calcolatore ---
calcola_intercettazione()
