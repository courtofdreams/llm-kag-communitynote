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
        for index, row in df.iterrows():
            document = row["Document"]
            urls = re.findall(url_pattern, document)
            cleaned_text = re.sub(url_pattern, '', document).strip()
            note = {
                'id': index,
                'note':cleaned_text,
                'sources':urls
            } 
            note_data.append(note)
        
        
        return note_data
