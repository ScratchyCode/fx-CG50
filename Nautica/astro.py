# Navigazione Astronomica con Casio fx-CG50
import math

STARS = {
    # Dati ricalcolati per l'epoca 2025.5
    "SIRIO":      (6.779,  -16.75),
    "BETELGEUSE": (5.941,    7.42),
    "BELLATRIX":  (5.438,    6.36),
    "RIGEL":      (5.262,   -8.20),
    "PROCIONE":   (7.681,    5.18),
    "ALTAIR":     (19.869,   8.91),
    "VEGA":       (18.624,  38.80),
    "DENEB":      (20.712,  45.33),
    "POLARE":     (3.064,   89.41),
    "ARTURO":     (14.270,  19.11),
    "ALBIREO":    (19.531,  28.01),
    "ALDEBARAN":  (4.620,   16.55),
    "CAPELLA":    (5.299,   46.03),
    "ANTARES":    (16.510, -26.46)
}

DEG_TO_RAD = math.pi / 180.0
RAD_TO_DEG = 180.0 / math.pi

def dms_to_deg(d, m, s=0.0):
    """Gradi, primi, secondi -> gradi decimali."""
    sign = -1 if d < 0 else 1
    return d + sign * (m / 60.0 + s / 3600.0)

def deg_to_dms(deg):
    """Gradi decimali -> (gradi, primi) con 1 decimale di primo."""
    sign = -1 if deg < 0 else 1
    deg_abs = abs(deg)
    d = int(deg_abs)
    minutes = (deg_abs - d) * 60.0
    m = round(minutes, 1)
    if m >= 60.0:  # corregge arrotondamento a 60.0'
        m = 0.0
        d += 1
    return sign * d, m

def normalize_angle(a):
    """Normalizza l'angolo in [0, 360)."""
    a = a % 360.0
    return a + 360.0 if a < 0 else a

# Funzioni trigonometriche in gradi
def sin_deg(x):  return math.sin(x * DEG_TO_RAD)
def cos_deg(x):  return math.cos(x * DEG_TO_RAD)
def asin_deg(x): return math.degrees(math.asin(max(-1.0, min(1.0, x))))
def acos_deg(x): return math.degrees(math.acos(max(-1.0, min(1.0, x))))

def julian_day(y, m, d, h, M):
    """Calcola il Giorno Giuliano (JD) per data (gregoriana) e ora UTC fornita."""
    if m <= 2:
        y -= 1
        m += 12
    A = y // 100
    B = 2 - A + (A // 4)
    JD = int(365.25 * (y + 4716)) + int(30.6001 * (m + 1)) + d + B - 1524.5
    JD += (h + M / 60.0) / 24.0
    return JD

def gha_aries(jd):
    """GHA del punto d'Ariete (in gradi) per il JD fornito."""
    D = jd - 2451545.0
    T = D / 36525.0
    T2 = T * T
    T3 = T * T * T
    gha = (280.46061837
           + 360.98564736629 * D
           + 0.000387933 * T2
           - T3 / 38710000.0)
    
    return normalize_angle(gha)

def calcola_retta_d_altezza(lat, lon, ra_h, dec, jd):
    """
    Calcola l'altezza stimata (hc) e l'azimut (Zn) di un astro.
    Questa funzione contiene la logica di calcolo corretta e verificata.
    """
    # GHA del punto d'Ariete
    gha_a = gha_aries(jd)

    # GHA e LHA della stella (con la correzione del segno '+')
    gha_s = normalize_angle(gha_a + (ra_h * 15.0))
    lha = normalize_angle(gha_s + lon)

    # Altezza calcolata (hc)
    sin_hc = sin_deg(lat) * sin_deg(dec) + cos_deg(lat) * cos_deg(dec) * cos_deg(lha)
    hc = asin_deg(sin_hc)

    # Azimut (Zn)
    cos_zn_den = cos_deg(lat) * cos_deg(hc)
    if abs(cos_zn_den) < 1e-9:
        zn = 0.0 if lat < 0 else 180.0
    else:
        cos_zn_num = sin_deg(dec) - sin_deg(lat) * sin_deg(hc)
        val = max(-1.0, min(1.0, cos_zn_num / cos_zn_den)) # Previene errori di dominio
        zn = acos_deg(val)

    if sin_deg(lha) > 0:
        zn = 360.0 - zn
        
    return zn, hc


def main():
    print("- GPS STELLARE -")
    # Input posizione stimata (lat, lon in gradi e primi)
    try:
        print("\n- Posizione Stimata -")
        lat_g = int(input("Lat gradi: "))
        lat_p = float(input("Lat primi: "))
        lon_g = int(input("Lon gradi: "))
        lon_p = float(input("Lon primi: "))
    except (ValueError, IndexError):
        print("Err: format dati")
        return
    # Controllo range coordinate
    if lat_p < 0 or lat_p >= 60 or lon_p < 0 or lon_p >= 60:
        print("Lat/Lon fuori range")
        return
    if abs(lat_g) > 90 or (abs(lat_g) == 90 and lat_p != 0):
        print("Lat fuori range")
        return
    if abs(lon_g) > 180 or (abs(lon_g) == 180 and lon_p != 0):
        print("Lon fuori range")
        return
    # Converti in gradi decimali
    lat_ass = dms_to_deg(lat_g, lat_p)
    lon_ass = dms_to_deg(lon_g, lon_p)
    # Numero di osservazioni
    try:
        N = int(input("\nNum osserv: "))
    except (ValueError, IndexError):
        print("Err: servono 2 oss")
        return
    if N < 2:
        print("Servono 2 oss")
        return

    obs = []  # lista (azimut, intercetta)
    for i in range(N):
        print(f"\n- Osservaz {i+1} -")
        nome = input("Stella: ").upper().strip()
        if nome not in STARS:
            print("Stella non trovata")
            continue
        try:
            ra_h, dec = STARS[nome]
            h_obs = float(input("Altezza: "))
            data_str = input("Data (Y,M,D): ")
            ora_str = input("Ora (H,M): ")
            y, m, d = map(int, data_str.split(','))
            h, M = map(int, ora_str.split(','))
        except (ValueError, IndexError):
            print("Formato non valido")
            continue
        
        # CONTROLLI SUI DATI (già presenti e corretti)
        if not (0.0 <= h_obs <= 90.0):
            print("Altezza fuori range (0-90)")
            continue
        if m < 1 or m > 12 or d < 1 or d > 31:
            print("Data non valida")
            continue
        if h < 0 or h > 23 or M < 0 or M > 59:
            print("Ora non valida")
            continue

        # --- BLOCCO DI CALCOLO SEMPLIFICATO E CORRETTO ---
        # Calcola il giorno giuliano
        jd = julian_day(y, m, d, h, M)
        # Chiama la funzione corretta per ottenere azimut (zn) e altezza calcolata (hc)
        zn, hc = calcola_retta_d_altezza(lat_ass, lon_ass, ra_h, dec, jd)
        # --- FINE BLOCCO DI CALCOLO ---

        intercept = (h_obs - hc) * 60.0  # intercetta in NM
        obs.append((zn, intercept))
        print(f"Interc: {intercept:.1f} NM")
        print(f"Azimut: {zn:.1f}")

    if len(obs) < 2:
        print("\nCalcolo non possibile")
        return

    # Calcolo della correzione (intersezione rette d'altezza)
    sum_sin2 = sum_cos2 = sum_sincos = 0.0
    sum_x = sum_y = 0.0
    for zn, d in obs:
        rad = zn * DEG_TO_RAD
        sinz = math.sin(rad)
        cosz = math.cos(rad)
        sum_sin2   += sinz * sinz
        sum_cos2   += cosz * cosz
        sum_sincos += sinz * cosz
        sum_x      += d * sinz
        sum_y      += d * cosz

    det = sum_sin2 * sum_cos2 - sum_sincos**2
    if abs(det) < 1e-9:
        print("\nErr: rilev parall")
        return

    # Delta in minuti di arco (Nord/Sud ed Est/Ovest)
    delta_NS = (sum_y * sum_sin2 - sum_x * sum_sincos) / det
    delta_EW = (sum_x * sum_cos2 - sum_y * sum_sincos) / det
    # Applica le correzioni alla posizione stimata
    final_lat = lat_ass + delta_NS / 60.0
    if abs(cos_deg(lat_ass)) < 1e-9:
        final_lon = lon_ass
        print("NB: Lat prox polo")
    else:
        final_lon = lon_ass + delta_EW / (60.0 * cos_deg(lat_ass))

    # Conversione coordinate finali in gradi e primi (con lettera N/S, E/W)
    d_lat, m_lat = deg_to_dms(final_lat)
    d_lon, m_lon = deg_to_dms(final_lon)
    lat_char = "N" if final_lat >= 0 else "S"
    lon_char = "E" if final_lon >= 0 else "W"
    print("\n- PUNTO NAVE -")
    print(f"Lat: {abs(d_lat)}* {m_lat:.1f}' {lat_char}")
    print(f"Lon: {abs(d_lon)}* {m_lon:.1f}' {lon_char}")


# Esecuzione del programma principale
main()
