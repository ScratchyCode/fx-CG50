from casioplot import *
import random

def gioco_del_caos():
    clear_screen()

    try:
        # Chiediamo il numero di punti da disegnre
        n_str = input("Num punti: ")
        if n_str == "":
            punti = 15000
        else:
            punti = int(n_str)
    except (ValueError, TypeError):
        print("Input non valido.")
        punti = 15000

    # Definiamo i tre vertici per riempire lo schermo
    vertice_A = (192, 0)      # In alto al centro
    vertice_B = (0, 215)      # In basso a sinistra
    vertice_C = (383, 215)    # In basso a destra
    vertici = [vertice_A, vertice_B, vertice_C]
    
    # === MODIFICA CHIAVE ===
    pixel_color = (0, 0, 0) # NERO

    # Partiamo da un punto a caso (es. il centro)
    px, py = 192, 108

    # Inizia il ciclo
    for i in range(punti):
        # Scegli un vertice a caso
        vertice_scelto = random.choice(vertici)
        
        # Calcola il punto medio e aggiorna la posizione
        px = (px + vertice_scelto[0]) // 2
        py = (py + vertice_scelto[1]) // 2
        
        # Disegna il pixel nella nuova posizione
        set_pixel(px, py, pixel_color)
        
        # Ogni 500 punti, aggiorniamo lo schermo per vedere il progresso
        if i % 500 == 0:
            show_screen()

    # Mostra il risultato finale
    show_screen()
    input("--- [EXE] ---")

# Esegui lo script
gioco_del_caos()
