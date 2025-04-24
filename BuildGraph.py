from  NotesProcessor import NotesProcessor
from MongoDBService import MongoDBService
from KnowledgeGraphService import KnowledgeGraphService, Graph

## This file use to process community note and build community note graph
databaseName = "community-note-mongo"
collectionName = "community"
mongodbUri = "mongodb://root:password@0.0.0.0:27017/"
mongodb = MongoDBService(mongodbUri, databaseName, collectionName)
processor = NotesProcessor("data/community_note_data.xlsx")
## 'index': index, 'note':cleaned_text, 'sources':urls
data = processor.process_notes()
kg_service = KnowledgeGraphService(temperature=0,model_name="gpt-4.1-nano")


process = input("""Please enter the process you want to run:
             1. Insert data into MongoDB
             2. Reset MongoDB
             3. Build Graph (Might Take a while)""")

process_number = int(process)
if process_number == 1:
    print(f'Inserting data size {len(data)} into communityNote collection...')
    mongodb.insert_notes(data)
    print("Data inserted successfully.")

elif process_number == 2:
    print("Resetting MongoDB...")
    mongodb.reset_database()
    print("Database reset successfully.")
elif process_number == 3:
    print("Building graph...")
    notes = [item['note'] for item in data[:5]]
    kg_service.build_multiple_graphs(notes, Graph.COMMUNITY)
    print("Graph built successfully.")    
else:
    print("Invalid process number. Please enter 1, 2, or 3.")    
