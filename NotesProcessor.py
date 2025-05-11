import pandas as pd
import re
class Note:
    def __init__(self, id, note, url=[]):
        self.id = id
        self.note = note
        self.url = url

class NotesProcessor:
    def __init__(self, file):
        self.file = file

    def process_notes(self) -> list:
        # Process the notes to extract relevant information
        df = pd.read_excel(self.file)
        note_data = []
        url_pattern = r'https?://\S+'
        print(f"Processing {self.file}...\n total {len(df)} notes")
        for index, row in df.iterrows():
            document = row["Document"]
            urls = re.findall(url_pattern, document)
            
            cleaned_text = re.sub(url_pattern, '', document).strip()
            cleaned_text = cleaned_text.replace('NNN', '')
            note = {
                'id': index,
                'note':cleaned_text,
                'sources':urls
            } 
            note_data.append(note)
        
        return note_data
