from FactCheckAgent import FactCheckAgent
from KnowledgeGraphService import KnowledgeGraphService, Graph
import time
import pandas as pd
from tqdm import tqdm
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
from MongoDBService import MongoDBService
import csv
import os
 
databaseName = "community-note-mongo"
collectionName = "community"
mongodbUri = os.getenv("MONGO_DB_URI")
mongo_service = MongoDBService(mongodbUri, databaseName, collectionName)
model = "gpt-4.1-nano-2025-04-14"
temperature = 0
kg_service = KnowledgeGraphService(temperature,model)
agent = FactCheckAgent(kg_service=kg_service,mongo_service=mongo_service,temperature=temperature,model_name=model)

gold_answers = []
questions = []

# Excel file
file_path = "data/question_full.xlsx"
df = pd.read_excel(file_path)
for index, row in df.iterrows():
    questions.append(row["question"])
    print(f"Question: {row['question']}")
    print(f"Gold Answer: {row['is_factual']}")
    
    gold_answers.append(row["is_factual"])
    print(gold_answers[index])
    
    
# file_path = "data/query_output_71.json"
# with open(file_path, "r") as file:
#     data = json.load(file)

# # Example: Access individual questions and answers
# for item in data:
#     print(f"Gold Answer: {item['is_factual']}")
#     questions.append(item["question"])
#     gold_answers.append(True if item["is_factual"]== "Y" else False)
#     print(f"Gold Answer: {item["is_factual"]}")
#     print(f"Gold Answer: {True if item["is_factual"]== "Y" else False}")
  
    
final_results = []
system_answers = []
index = 0
for question in tqdm(questions):
    try:
        system_answer = agent.get_fact_for_verdict(question, Graph.BASELINE)
    except Exception as e:
        print(f"Error processing question: {question}")
        print(f"Exception: {e}")
        index += 1
        continue
    
    system_answers.append(system_answer["is_factual"])
    final_results.append({
        "question": question,
        "system_answer": system_answer["is_factual"],
        "gold_answer": gold_answers[index]
    })
    print(f"Question: {question}")
    print(f"Gold Answer: {gold_answers[index]}")
    print(f"System Answer: {system_answer["is_factual"]}")
    print("Sleep for 20 second")
    index += 1
    time.sleep(45)
    
gold_answers_result = [result["gold_answer"] for result in final_results]
system_answers_result = [result["system_answer"] for result in final_results]


accuracy = accuracy_score(gold_answers_result, system_answers_result)
f1 = f1_score(gold_answers_result, system_answers_result, average='weighted')
precision = precision_score(gold_answers_result, system_answers_result, average='weighted')
recall = recall_score(gold_answers_result, system_answers_result, average='weighted')

print(f"Total questions: {len(questions)}")
print(f"Total system answers: {len(system_answers_result)}")

print(f"Accuracy: {accuracy}")
print(f"F1 Score: {f1}")
print(f"Precision: {precision}")
print(f"Recall: {recall}")

keys = final_results[0].keys()
with open('data/output_blind.csv', 'w', newline='') as output_file:
    dict_writer = csv.DictWriter(output_file, fieldnames=keys)
    dict_writer.writeheader()
    dict_writer.writerows(final_results)