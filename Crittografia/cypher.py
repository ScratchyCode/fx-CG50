# TRASPOSIZIONE COLONNARE
# CON FRAZIONAMENTO

def stampa_impaginata(testo, dimensione_blocco=20):
    print("\n--- [EXE] ---")
    i = 0
    while i < len(testo):
        blocco = testo[i:i + dimensione_blocco]
        print(blocco)
        i += dimensione_blocco
        if i < len(testo):
            input("...")


def ordina_chiave(num_colonne, chiave):
    lista_da_ordinare = []
    for i in range(num_colonne):
        lista_da_ordinare.append((chiave[i], i))

    n = len(lista_da_ordinare)
    for i in range(n):
        for j in range(0, n - i - 1):
            if lista_da_ordinare[j][0] > lista_da_ordinare[j + 1][0]:
                temp = lista_da_ordinare[j]
                lista_da_ordinare[j] = lista_da_ordinare[j + 1]
                lista_da_ordinare[j + 1] = temp
    
    ordine_colonne = []
    for item in lista_da_ordinare:
        ordine_colonne.append(item[1])
        
    return ordine_colonne

def cifra_trasposizione(testo, chiave):
    if not chiave:
        return testo

    num_colonne = len(chiave)
    num_righe = (len(testo) + num_colonne - 1) // num_colonne
    
    padding_necessario = (num_righe * num_colonne) - len(testo)
    testo_paddato = testo + 'X' * padding_necessario
    
    ordine_colonne = ordina_chiave(num_colonne, chiave)
    
    testo_cifrato = ""
    for col in ordine_colonne:
        for riga in range(num_righe):
            indice = riga * num_colonne + col
            testo_cifrato += testo_paddato[indice]
            
    return testo_cifrato

def decifra_trasposizione(testo_cifrato, chiave):
    if not chiave:
        return testo_cifrato

    num_colonne = len(chiave)
    num_righe = len(testo_cifrato) // num_colonne
    
    ordine_colonne_cifratura = ordina_chiave(num_colonne, chiave)
    
    griglia = [''] * len(testo_cifrato)
    indice_cifrato = 0
    
    for col in ordine_colonne_cifratura:
        for riga in range(num_righe):
            indice_originale = riga * num_colonne + col
            griglia[indice_originale] = testo_cifrato[indice_cifrato]
            indice_cifrato += 1
            
    return "".join(griglia)


def esegui_cifratura():
    print("\n--- CIFRATURA ---")
    testo_originale = input("Testo: ")
    chiave1 = input("I chiave: ")
    chiave2 = input("II chiave: ")
    
    if not testo_originale or not chiave1 or not chiave2:
        print("Input non validi.")
        input("--- [EXE] ---")
        return

    stringa_decimale = ""
    for char in testo_originale:
        codice_str = str(ord(char))
        if len(codice_str) == 1:
            stringa_decimale += "00" + codice_str
        elif len(codice_str) == 2:
            stringa_decimale += "0" + codice_str
        else:
            stringa_decimale += codice_str
    
    intermedio = cifra_trasposizione(stringa_decimale, chiave1)
    testo_finale_cifrato = cifra_trasposizione(intermedio, chiave2)
    
    stampa_impaginata(testo_finale_cifrato)
    
    print("-----------------")
    print("Output terminato.")
    input("--- [EXE] ---")

def esegui_decifratura():
    print("\n--- DECIFRATURA ---")
    print("Cifre:")
    testo_cifrato = input("> ")
    chiave1 = input("I chiave: ")
    chiave2 = input("II chiave: ")

    if not testo_cifrato or not chiave1 or not chiave2:
        print("Input non validi.")
        input("--- [EXE] ---")
        return

    intermedio = decifra_trasposizione(testo_cifrato, chiave2)
    stringa_decimale_paddata = decifra_trasposizione(intermedio, chiave1)
    
    stringa_decimale = stringa_decimale_paddata
    while len(stringa_decimale) > 0 and stringa_decimale[-1] == 'X':
        stringa_decimale = stringa_decimale[:-1]
    
    testo_decifrato = ""
    try:
        if len(stringa_decimale) % 3 != 0:
            print("Cifre non valide.")
            input("--- [EXE] ---")
            return
            
        for i in range(0, len(stringa_decimale), 3):
            codice_ascii = int(stringa_decimale[i:i+3])
            testo_decifrato += chr(codice_ascii)
            
        print("\n--- RISULTATO ---")
        print(testo_decifrato)
        print("-----------------")
        input("--- [EXE] ---")
        
    except:
        print("\nChiave errata.")
        print("-----------------")
        input("--- [EXE] ---")


def menu():
    while True:
        print("\n=== Menu ===")
        print("1. Cifra")
        print("2. Decifra")
        print("3. Esci")
        
        scelta = input("Opzione: ")
        
        if scelta == '1':
            esegui_cifratura()
        elif scelta == '2':
            esegui_decifratura()
        elif scelta == '3':
            print("Arrivederci!")
            break
        else:
            print("Scelta non valida.")

menu()
