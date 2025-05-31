import zipfile
import os
import json
import pyodbc
 
# Percorsi file
file_zip = r"C:\Users\Casti\Downloads\TXT_Data.zip"  
cartella_estratta = r"TXT_Data"
file_output_json = r"C:\Users\Casti\Documents\Python\Project work\output.json"
 
# Connessione al database SQL Server
try:
    conn = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=MSI;'
        'DATABASE=Test_C001;'
        'Trusted_Connection=yes;'
    )
    cursor = conn.cursor()
    print("Connessione al database avvenuta con successo.")
except pyodbc.Error as e:
    print("Errore nella connessione al database:", e)
    exit()
 
# Controlla se il file ZIP esiste
if not os.path.exists(file_zip):
    print(f"Errore: il file ZIP non esiste al percorso {file_zip}")
    exit()
 
# Estrazione del file ZIP
print("Estrazione dei file ZIP...")
try:
    with zipfile.ZipFile(file_zip, 'r') as zip_ref:
        zip_ref.extractall(cartella_estratta)
    print("Estrazione completata!")
except PermissionError:
    print("Errore: Permesso negato durante l'accesso al file ZIP o alla cartella di estrazione.")
    exit()
 
# Elaborazione dei file di testo
episodi = []
for root, _, files in os.walk(cartella_estratta):
    for file in files:
        if file.endswith(".txt"):
            episodio_numero = file.split("_e_")[1].replace(".txt", "")
            stagione = file.split("_e_")[0]  # Aggiunge la stagione dal nome file
 
            episodio = {
                "episode number": episodio_numero,
                "season": stagione,
                "script": []
            }
            dialoghi = {}  
 
            percorso_file = os.path.join(root, file)
            with open(percorso_file, "r", encoding="utf-8") as f:
                for riga in f:
                    if ":" in riga:
                        personaggio, battuta = map(str.strip, riga.split(":", 1))
                        if personaggio not in dialoghi:
                            dialoghi[personaggio] = []
                        dialoghi[personaggio].append(battuta)
 
            for personaggio, battute in dialoghi.items():
                numero_battute = len(battute)
                lunghezza_totale_battute = sum(len(battuta) for battuta in battute)
 
                # Inserimento nel database SQL Server
                try:
                    print(f"Inserimento nel database: Stagione {stagione}, Episodio {episodio_numero}, Personaggio {personaggio}, Battute {numero_battute}, Lunghezza {lunghezza_totale_battute}")
                    cursor.execute("""
                    INSERT INTO [Episodi] (Stagione, EpisodioNumero, Personaggio, numeroBattute, LunghezzaBattute)
                    VALUES (?, ?, ?, ?, ?)
                   
                    """, stagione, episodio_numero, personaggio, numero_battute, lunghezza_totale_battute)
                    conn.commit()
                except pyodbc.Error as e:
                    print(f"Errore nell'inserimento del personaggio '{personaggio}' per episodio {episodio_numero}: {e}")
           
            # Aggiungi i dialoghi all'episodio per il JSON finale
            for personaggio, battute in dialoghi.items():
                episodio["script"].append({
                    "nome_personaggio": personaggio,
                    "battute": battute
                })
 
            episodi.append(episodio)
 
# Salvataggio dei dati in formato JSON
print("Salvataggio dei dati in formato JSON...")
try:
    with open(file_output_json, "w", encoding="utf-8") as json_file:
        json.dump(episodi, json_file, ensure_ascii=False, indent=4)
    print(f"Dati salvati in: {file_output_json}")
except PermissionError:
    print("Errore: Permesso negato durante il salvataggio del file JSON.")
 
# Chiusura della connessione al database
cursor.close()
conn.close()
 
 
 
 
