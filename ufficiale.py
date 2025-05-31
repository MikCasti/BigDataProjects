import zipfile
import os
import json
import pyodbc
 
class Episodio:
    def __init__(self, stagione, episodio_numero):
        self.stagione = stagione
        self.episodio_numero = episodio_numero
        self.script = []
 
    def aggiungi_dialoghi(self, personaggio, battute):
        self.script.append({
            "nome_personaggio": personaggio,
            "battute": battute
        })
 
    def contiene_dialoghi(self):
        return bool(self.script)
 
 
class Database:
    def __init__(self, connection_string):
        try:
            self.conn = pyodbc.connect(connection_string)
            self.cursor = self.conn.cursor()
            print("Connessione al database avvenuta con successo.")
        except pyodbc.Error as e:
            print("Errore nella connessione al database:", e)
            exit()
 
    def inserisci_dati(self, stagione, episodio_numero, personaggio, numero_battute, lunghezza_battute):
        try:
            self.cursor.execute("""
                INSERT INTO [Episodi] (Stagione, EpisodioNumero, Personaggio, numeroBattute, LunghezzaBattute)
                VALUES (?, ?, ?, ?, ?)
            """, stagione, episodio_numero, personaggio, numero_battute, lunghezza_battute)
            self.conn.commit()
        except pyodbc.Error as e:
            print(f"Errore nell'inserimento del personaggio '{personaggio}' per episodio {episodio_numero}: {e}")
 
    def chiudi(self):
        self.cursor.close()
        self.conn.close()
 
 
class ElaboraFile:
    def __init__(self, file_zip, cartella_estratta, file_output_json, db_conn):
        self.file_zip = file_zip
        self.cartella_estratta = cartella_estratta
        self.file_output_json = file_output_json
        self.db_conn = db_conn
 
    def estrai_file_zip(self):
        if not os.path.exists(self.file_zip):
            print(f"Errore: il file ZIP non esiste al percorso {self.file_zip}")
            exit()
 
        try:
            with zipfile.ZipFile(self.file_zip, 'r') as zip_ref:
                zip_ref.extractall(self.cartella_estratta)
            print("Estrazione completata!")
        except PermissionError:
            print("Errore: Permesso negato durante l'accesso al file ZIP o alla cartella di estrazione.")
            exit()
 
    def elabora_file_testo(self):
        episodi = []
        for root, _, files in os.walk(self.cartella_estratta):
            for file in files:
                if file.endswith(".txt"):
                    try:
                        parte_nome = file.split("_e_")
                        if len(parte_nome) != 2:
                            print(f"Nome del file non conforme: {file}")
                            continue
 
                        stagione = parte_nome[0]
                        episodio_numero = int(parte_nome[1].replace(".txt", ""))
                    except ValueError:
                        print(f"Errore nell'estrazione del numero dell'episodio per il file {file}.")
                        continue
 
                    episodio = Episodio(stagione, episodio_numero)
                    dialoghi = {}
 
                    percorso_file = os.path.join(root, file)
                    print(f"Elaborazione del file {file}...")  # Debug
 
                    with open(percorso_file, "r", encoding="utf-8") as f:
                        for riga in f:
                            if ":" in riga:
                                try:
                                    personaggio, battuta = map(str.strip, riga.split(":", 1))
                                    if personaggio not in dialoghi:
                                        dialoghi[personaggio] = []
                                    dialoghi[personaggio].append(battuta)
                                except ValueError:
                                    print(f"Errore nella formattazione della riga: {riga}")
                            else:
                                print(f"Riga ignorata (non contiene ':'): {riga}")
 
                    for personaggio, battute in dialoghi.items():
                        if battute:
                            numero_battute = len(battute)
                            lunghezza_totale_battute = sum(len(battuta) for battuta in battute)
 
                            # Inserimento nel database SQL Server
                            self.db_conn.inserisci_dati(stagione, episodio_numero, personaggio, numero_battute, lunghezza_totale_battute)
 
                            # Aggiungi i dialoghi all'episodio
                            episodio.aggiungi_dialoghi(personaggio, battute)
 
                    if episodio.contiene_dialoghi():
                        episodi.append(episodio)
 
        return episodi
 
    def salva_json(self, episodi):
        print("Salvataggio dei dati in formato JSON...")
        try:
            with open(self.file_output_json, "w", encoding="utf-8") as json_file:
                json.dump([episodio.__dict__ for episodio in episodi], json_file, ensure_ascii=False, indent=4)
            print(f"Dati salvati in: {self.file_output_json}")
        except PermissionError:
            print("Errore: Permesso negato durante il salvataggio del file JSON.")
 
 
if __name__ == "__main__":
    # Connessione al database
    db_conn = Database('DRIVER={ODBC Driver 17 for SQL Server};SERVER=MSI;DATABASE=Test_C001;Trusted_Connection=yes;')
 
    # Creazione dell'oggetto per elaborare il file
    elabora_file = ElaboraFile(
        r"C:\Users\Casti\Downloads\TXT_Data.zip",
        r"C:\Users\Casti\Documents\Python\Project work\TXT_Data",
        r"C:\Users\Casti\Documents\Python\Project work\output.json",
        db_conn
    )
 
    # Estrazione dei file dal ZIP
    elabora_file.estrai_file_zip()
 
    # Elaborazione dei file di testo e creazione dell'elenco degli episodi
    episodi = elabora_file.elabora_file_testo()
 
    # Salvataggio in JSON
    elabora_file.salva_json(episodi)
 
    # Chiusura della connessione al database
    db_conn.chiudi()
 