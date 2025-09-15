# TRASPOSIZIONE COLONNARE
# + FRAZIONAMENTO
# + XOR BITWISE

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
    lista = [(chiave[i], i) for i in range(num_colonne)]
    lista.sort(key=lambda x: x[0])
    return [item[1] for item in lista]

def transpose_blocks(blocks, chiave, pad_block='000'):
    if not chiave:
        return blocks[:]
    num_col = len(chiave)
    num_rows = (len(blocks) + num_col - 1) // num_col
    padding_needed = num_rows * num_col - len(blocks)
    blocks_padded = blocks + [pad_block] * padding_needed
    ordine = ordina_chiave(num_col, chiave)
    result = []
    for col in ordine:
        for r in range(num_rows):
            idx = r * num_col + col
            result.append(blocks_padded[idx])
    return result

def inverse_transpose_blocks(blocks, chiave):
    if not chiave:
        return blocks[:]
    num_col = len(chiave)
    num_rows = len(blocks) // num_col
    ordine = ordina_chiave(num_col, chiave)
    result = [None] * (num_rows * num_col)
    idx_cifrato = 0
    for col in ordine:
        for r in range(num_rows):
            orig_idx = r * num_col + col
            result[orig_idx] = blocks[idx_cifrato]
            idx_cifrato += 1
    return result

def xor_con_chiave(testo, chiave):
    if not chiave:
        return testo
    risultato = []
    klen = len(chiave)
    for i in range(len(testo)):
        c = testo[i]
        risultato.append(chr(ord(c) ^ ord(chiave[i % klen])))
    return "".join(risultato)

def applica_padding(blocks, num_col, pad_block='000'):
    num_rows = (len(blocks) + num_col - 1) // num_col
    padding_needed = num_rows * num_col - len(blocks)
    return blocks + [pad_block] * padding_needed

def esegui_cifratura():
    print("\n--- CIFRATURA ---")
    testo_originale = input("Testo: ")
    chiave1 = input("I   chiave: ")
    chiave2 = input("II  chiave: ")
    chiave3 = input("III chiave: ")

    if not testo_originale or not chiave1 or not chiave2 or not chiave3:
        print("Input non validi.")
        input("--- [EXE] ---")
        return

    testo_xor = xor_con_chiave(testo_originale, chiave1)
    blocks = ["{:03d}".format(ord(c)) for c in testo_xor]

    if len(blocks) > 999:
        print("Testo troppo lungo.")
        input("--- [EXE] ---")
        return

    length_block = "{:03d}".format(len(blocks))
    blocks_with_header = [length_block] + blocks

    blocks_padded = applica_padding(blocks_with_header, len(chiave2), pad_block='000')
    blocks_after_t2 = transpose_blocks(blocks_padded, chiave2, pad_block='000')

    blocks_padded2 = applica_padding(blocks_after_t2, len(chiave3), pad_block='000')
    blocks_final = transpose_blocks(blocks_padded2, chiave3, pad_block='000')

    testo_finale_cifrato = "".join(blocks_final)
    stampa_impaginata(testo_finale_cifrato)
    print("-----------------")
    print("Output terminato.")
    input("--- [EXE] ---")

def esegui_decifratura():
    print("\n--- DECIFRATURA ---")
    testo_cifrato = ""
    while True:
        parte = input("> ")
        if parte == "":
            break
        testo_cifrato += parte

    chiave1 = input("I   chiave: ")
    chiave2 = input("II  chiave: ")
    chiave3 = input("III chiave: ")

    if not testo_cifrato or not chiave1 or not chiave2 or not chiave3:
        print("Input non validi.")
        input("--- [EXE] ---")
        return

    if len(testo_cifrato) % 3 != 0:
        print("Cifre non valide:", len(testo_cifrato))
        input("--- [EXE] ---")
        return

    blocks = [testo_cifrato[i:i+3] for i in range(0, len(testo_cifrato), 3)]

    blocks_after_inv3 = inverse_transpose_blocks(blocks, chiave3)
    blocks_after_inv2 = inverse_transpose_blocks(blocks_after_inv3, chiave2)

    if not blocks_after_inv2:
        print("Errore: dati vuoti.")
        input("--- [EXE] ---")
        return

    try:
        n = int(blocks_after_inv2[0])
    except Exception:
        print("Errore nella lettura.")
        input("--- [EXE] ---")
        return

    if len(blocks_after_inv2) < 1 + n:
        print("Dati incompleti.")
        input("--- [EXE] ---")
        return

    data_blocks = blocks_after_inv2[1:1+n]

    try:
        testo_post_trasposizioni = ''.join(chr(int(b)) for b in data_blocks)
    except Exception:
        print("Errore conv.")
        input("--- [EXE] ---")
        return

    testo_decifrato = xor_con_chiave(testo_post_trasposizioni, chiave1)

    print("\n--- RISULTATO ---")
    print(testo_decifrato)
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

