from KnowledgeAgent import KnowledgeAgent
from KnowledgeGraphService import KnowledgeGraphService
 

kg_service = KnowledgeGraphService(0.1,"gpt-4o-2024-08-06")
agent = KnowledgeAgent(kg_service=kg_service)

agent.answer_query("Did Elon Musk buy Meta?", config="hybrid")
