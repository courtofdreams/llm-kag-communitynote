from FactCheckAgent import FactCheckAgent
from KnowledgeGraphService import KnowledgeGraphService, Graph
import time
import pandas as pd
from tqdm import tqdm
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
from MongoDBService import MongoDBService
import csv
 
## For testing purposes, we will use the politifact dataset
gold_answers = []
system_answers = []
questions = []

file_path = "data/output_3topics_articles.csv"
df = pd.read_csv(file_path)
count_different = 0
time_average = 0
for index, row in df.iterrows():
    questions.append(row["question"])
    gold_answers.append(True if row["gold_answer"] == True else False)
    system_answers.append(True if row["system_answer"] == True else False)
    if row["gold_answer"]  != row["system_answer"]:
        count_different += 1
        time_average += row["time_answered"]


accuracy = accuracy_score(gold_answers, system_answers)
f1 = f1_score(gold_answers, system_answers, average='weighted')
precision = precision_score(gold_answers, system_answers, average='weighted')
recall = recall_score(gold_answers, system_answers, average='weighted')

print(f"Total questions: {len(questions)}")
print(f"Total system answers: {len(system_answers)}")
print(f"Total gold answers: {len(gold_answers)}")
print(f"Total different answers: {count_different}")
print(f"Average time to answer: {time_average / len(system_answers)}")
print(f"Accuracy: {accuracy}")
print(f"F1 Score: {f1}")
print(f"Precision: {precision}")
print(f"Recall: {recall}")
