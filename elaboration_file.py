import json
import os
import zipfile
from episode import Episode

"""Initializes paths and database connection for file processing"""
class ProcessFiles:
    def __init__(self, zip_file, extracted_folder, output_json_file, db_conn):
        self.zip_file = zip_file
        self.extracted_folder = extracted_folder
        self.output_json_file = output_json_file
        self.db_conn = db_conn
"""Extracts the contents of the ZIP file into the specified folder"""
def extract_zip_file(self):
        if not os.path.exists(self.zip_file):
            print(f"Error: The ZIP file does not exist at path {self.zip_file}")
            exit()
            #Checks if the ZIP file exists
 
        try:
            with zipfile.ZipFile(self.zip_file, 'r') as zip_ref:
                zip_ref.extractall(self.extracted_folder)
            print("Extraction completed!")
            #Uses zipfile.ZipFile to extract the contents
        except PermissionError:
            print("Error: Permission denied while accessing the ZIP file or extraction folder.")
            exit()
            # If the file doesn’t exist or permissions are insufficient, it prints an error and exits
 
"""Processes extracted text files, parses dialogues, and inserts them into the database"""
def process_text_files(self):
        episodes = []
        for root, _, files in os.walk(self.extracted_folder):
            #Finds all .txt files in the extracted folder
            for file in files:
                if file.endswith(".txt"):
                   
                    episode_number = file.split("_e_")[1].replace(".txt", "")
                    season = file.split("_e_")[0]
                    #Extracts season and episode_number from the file name
 
                    episode = Episode(season, episode_number)
                    dialogues = {}
 
                    file_path = os.path.join(root, file)
                    with open(file_path, "r", encoding="utf-8") as f:
                        for line in f:
                            if ":" in line:
                                character, line_text = map(str.strip, line.split(":", 1))
                                #Reads each line of the file, splitting it into character and line_text using :
                                if character not in dialogues:
                                    dialogues[character] = []
                                dialogues[character].append(line_text)
                                #Organizes dialogues in a dictionary by character
 
                               
                                self.db_conn.insert_quote(season, episode_number, character, line_text)
                                #Calls insert_quote for each dialogue to save it in the database
 
                    for character, lines in dialogues.items():
                        episode.add_dialogues(character, lines)
                        #Adds the dialogues to an Episode object
 
                    if episode.has_dialogues():
                        episodes.append(episode)
                        #Appends the Episode object to a list if it contains dialogue
 
        return episodes

"""Saves the list of Episode objects in JSON format"""
def save_to_json(self, episodes):
        print("Saving data to JSON format...")
        try:
            with open(self.output_json_file, "w", encoding="utf-8") as json_file:
                json.dump([episode.__dict__ for episode in episodes], json_file, ensure_ascii=False, indent=4)
            print(f"Data saved to: {self.output_json_file}")
        except PermissionError:
            print("Error: Permission denied while saving the JSON file.")
            #Converts each Episode object into a dictionary using __dict__.
            #Writes the resulting list of dictionaries to the specified JSON file
 