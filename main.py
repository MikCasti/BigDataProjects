from database import Database
from elaboration_file import ProcessFiles


if __name__ == "__main__":
    db_conn = Database(
        #Creates a database connection by using the Database class
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=DATA-CASTILLO;'
        'DATABASE=ProjWorkOff;'
        'Trusted_Connection=yes;'
    )
 
 
    process_files = ProcessFiles(
        #Initializes the ProcessFiles object by setting up file paths and the database connection.
        r"C:/Users/MicheleCastillo\Downloads/TXT_Data.zip",
        r"TXT_Data",
        r"Test.json",
        db_conn
    )
 
    process_files.extract_zip_file()
    #Extracts the contents of the ZIP file
 
    episodes = process_files.process_text_files()
    #It reads the text files, adds the dialogues to the database, and creates Episode objects
 
    process_files.save_to_json(episodes)
    #Exports the processed episodes to a JSON file
 
    db_conn.close()
    #Releases the database resources