from  NotesProcessor import NotesProcessor
from MongoDBService import MongoDBService
from KnowledgeGraphService import KnowledgeGraphService, Graph
import time
import os

## This file use to process community note and build community note graph
databaseName = "community-note-mongo"
collectionName = "community"
mongodbUri = os.getenv("MONGO_DB_URI")
mongodb = MongoDBService(mongodbUri, databaseName, collectionName)
kg_service = KnowledgeGraphService(temperature=0,model_name="gpt-4.1-nano")

process = input("""Please enter the process you want to run:
             1. Build Community Note Graph (Might Take a while)""")

process_number = int(process)
if process_number == 1:
    print("Building graph...")
    file_name = input("Please enter the file name (e.g., data/mislead_politics.xlsx): ")
    if not file_name.endswith(".xlsx"):
        print("Invalid file format. Please provide an Excel file.")
        exit(1)
        
    if not os.path.exists(file_name):
        print(f"File {file_name} does not exist.")
        exit(1)
    processor = NotesProcessor(file_name)
    data = processor.process_notes()
    print(f"Total notes: {len(data)}")
    batch_size = 20
    for i in range(0, len(data), batch_size):
        print(f"Processing batch {i//batch_size + 1}...")
        batch = data[i:i + batch_size]
        kg_service.build_multiple_graphs(batch, Graph.COMMUNITY)
        print(f"Batch {i//batch_size + 1} processed successfully.")
        print("Sleeping for 50 sec to avoid rate limit...")
        time.sleep(50)
        
    print("Graph built successfully.")    
else:
    print("Invalid process number. Please enter 1, 2, or 3.")    
