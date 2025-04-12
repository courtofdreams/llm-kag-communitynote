from KnowledgeAgent import KnowledgeAgent
from KnowledgeGraphService import KnowledgeGraphService, Graph
import json
import os
from tqdm import tqdm
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
 
kg_service = KnowledgeGraphService(0.1,"gpt-4o-2024-08-06")
agent = KnowledgeAgent(kg_service=kg_service)

## For testing purposes, we will use the politifact dataset
gold_answers = []
questions = []
for file in os.listdir("data"):
    if file.endswith(".json"):
        with open(os.path.join("data", file), "r") as f:
            data = json.load(f)  
            if isinstance(data, dict):
                questions.append(data["question"])
                gold_answers.append(data["is_factual"])
            else:
                raise ValueError("Expected a JSON object, but got something else.")

system_answers = []
for question in tqdm(questions):
    system_answer = agent.answer_query(question, Graph.COMMUNITY)
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