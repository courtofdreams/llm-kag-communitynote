from FactCheckAgent import FactCheckAgent
from KnowledgeGraphService import KnowledgeGraphService, Graph
import json
import os
from tqdm import tqdm
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
from MongoDBService import MongoDBService
 
databaseName = "community-note-mongo"
collectionName = "community"
mongodbUri = "mongodb://root:password@0.0.0.0:27017/"
mongo_service = MongoDBService(mongodbUri, databaseName, collectionName)
model = "gpt-4-turbo"
temperature = 0
kg_service = KnowledgeGraphService(temperature,model)
agent = FactCheckAgent(kg_service=kg_service,mongo_service=mongo_service,temperature=temperature,model_name=model)

## For testing purposes, we will use the politifact dataset
gold_answers = []
questions = []

file_path = "data/data.json"
with open(file_path, "r") as file:
    data = json.load(file)

# Print the data
print(data)

# Example: Access individual questions and answers
for item in data:
    questions.append(item["question"])
    gold_answers.append(item["is_factual"])

system_answers = []
for question in tqdm(questions):
    system_answer = agent.get_fact_for_verdict(question, Graph.COMMUNITY)
    system_answers.append(system_answer["is_factual"])
    print(f"System Answer: {system_answer["answer"]}")
    
# calculate accuracy of 
accuracy = accuracy_score(gold_answers, system_answers)
f1 = f1_score(gold_answers, system_answers, average='weighted')
precision = precision_score(gold_answers, system_answers, average='weighted')
recall = recall_score(gold_answers, system_answers, average='weighted')
print(f"Accuracy: {accuracy}")
print(f"F1 Score: {f1}")
print(f"Precision: {precision}")
print(f"Recall: {recall}")


# TODO: Add configurations for community and politifact based on the user input
## should i add frontend for this?