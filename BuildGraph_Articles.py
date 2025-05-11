import json
import requests
from bs4 import BeautifulSoup
from  NotesProcessor import NotesProcessor
from MongoDBService import MongoDBService
from KnowledgeGraphService import KnowledgeGraphService, Graph
import time
import os

# Replace 'file_path.json' with the path to your JSON file
file_path = 'data/graph_data/scrapped_news.json'

# Open and read the JSON file
with open(file_path, 'r') as file:
    data = json.load(file)

news = data["data"]

print(f"Number of news: {len(news)}")

databaseName = "community-note-mongo"
collectionName = "community"
mongodbUri = os.getenv("MONGO_DB_URI")
mongodb = MongoDBService(mongodbUri, databaseName, collectionName)
kg_service = KnowledgeGraphService(temperature=0,model_name="gpt-4.1-nano")
#add index 8
error_news_index = [8,20, 27, 44, 56]
for i in range(70, len(news)):
    
    try:
        # Extract the text content from the HTML
        print(f"Processing news {i+1}/{len(news)}")
        kg_service.build_graph(news[i], Graph.POLITIFACT)
        print("Sleeping for 50 sec to avoid rate limit...")
        time.sleep(50)
    except Exception as e:
        print(f"Error processing news {i+1}: {e}")
        print("Sleeping for 50 sec to avoid rate limit...")
        error_news_index.append(i)
        time.sleep(50)    


print("Graph built successfully.")     
print("Error news index: ", error_news_index)  