import json
import re

# Nome del file di input e del file di output
file_txt = "unione.txt"
file_json = "output.json"

# Struttura per contenere i dati
dati = {}

# Funzione per estrarre la stagione e l'episodio dal nome del file
def estrai_serie_e_episodio(nome_file):
    dati = {}
    match = re.search(r'TXT_Data/([^/]+)_e_(\d+)\.txt', nome_file)
    if match:
        stagione = match.group(1)  # Estrae la stagione (ad esempio DS9)
        episodio = int(match.group(2))  # Estrae il numero dell'episodio
        return stagione, episodio
    return None, None

try:
    with open(file_txt, 'r', encoding='utf-8') as file:
        # Variabili temporanee per raccogliere le informazioni
        personaggio = ""
        battuta = ""
        stagione = ""
        episodio = 0

        # Legge il file riga per riga
        for line in file:
            line = line.strip()  # Rimuove gli spazi bianchi extra

            # Estrazione della stagione e episodio dal nome del file
            if line.startswith("[TXT_Data/"):
                nome_file = line.split(']')[0][1:]  # Estrae il nome del file tra le parentesi quadre
                stagione, episodio = estrai_serie_e_episodio(nome_file)

            # Se la riga contiene il personaggio e la battuta
            nomeBattuta = line.split(']')[1].split(':')
            if 1:
                personaggio = nomeBattuta[0]
                battuta = nomeBattuta[1]

                # Aggiungi i dati al dizionario per la stagione ed episodio
                if stagione not in dati:
                    dati[stagione] = {}

                if episodio not in dati[stagione]:
                    dati[stagione][episodio] = []

                # Aggiungi l'informazione alla lista
                dati[stagione][episodio].append({
                    "personaggio": personaggio,
                    "battuta": battuta
                })
    # Scrive i dati nel file JSON
    with open(file_json, 'w', encoding='utf-8') as json_file:
        json.dump(dati, json_file, ensure_ascii=False, indent=4)

    print(f"I dati sono stati esportati in {file_json}")
except Exception as e:
    print(f"Errore: {e}")
