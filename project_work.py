import zipfile

# Nome del file ZIP
file_zip = r"C:\Users\MicheleCastillo\Downloads\TXT_Data.zip"
# Nome del file di output
file_unione = "unione.txt"

try:
    with zipfile.ZipFile(file_zip, 'r') as zip:
        # Elenca tutti i file nel file ZIP
        nomi_file = zip.namelist()

        with open(file_unione, 'w', encoding='utf-8') as output_file:
            for nome_file in nomi_file:
                if nome_file.endswith('.txt'):  # Processa solo i file .txt
                    with zip.open(nome_file) as input_file:
                        # Processa ogni riga del file
                        for line in input_file:
                            riga = line.decode('utf-8').strip()  # Decodifica e rimuove spazi inutili
                            
                            # Rimuove il prefisso "TXT_Data" se presente
                            if riga.startswith("TXT_Data"):
                                riga = riga[len("TXT_Data"):].strip()
                            
                            # Scrive la riga nel file di output con il riferimento al file .txt
                            output_file.write(f"[{nome_file}] {riga}\n")
                        
    print(f"I file sono stati uniti in {file_unione}")
except Exception as e:
    print(f"Errore: {e}")


    


