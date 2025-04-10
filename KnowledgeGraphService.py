import os

from langchain_community.graphs import Neo4jGraph
from langchain_experimental.graph_transformers import LLMGraphTransformer
from langchain_core.documents import Document
from langchain_neo4j import Neo4jGraph, GraphCypherQAChain
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate

class KnowledgeGraphService:
        def __init__(self, temperature=0, model_name="gpt-4-turbo"):   
            OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
            if OPENAI_API_KEY is None:
                raise ValueError("OPENAI_API_KEY environment variable not set.")
            self.graphDB = Neo4jGraph()
            print(f"{OPENAI_API_KEY}, {temperature}, {model_name}")
            self.llm = ChatOpenAI(openai_api_key=OPENAI_API_KEY,temperature=temperature, model_name=model_name)
            self.llm_transformer = LLMGraphTransformer(
                llm=self.llm
            )          
        
        def build_graph(self, text):
            documents = [Document(page_content=text)]
            graph_documents = self.llm_transformer.convert_to_graph_documents(documents)
            print(f"Nodes:{graph_documents[0].nodes}")
            print(f"Relationships:{graph_documents[0].relationships}")
            self.graphDB.add_graph_documents(graph_documents) # store into database       
            
        def reset_database(self):
            with self.graphDB.session() as session:
                session.run("MATCH (n) DETACH DELETE n")
                print("Database reset successfully!")   
        
        def get_facts(self, query):
            custom_prompt_template = """
                check the factuality of the statement and give out the result as yes or no
                Statement: {question}
                Answer:
            """
            CUSTOM_PROMPT = PromptTemplate(
                template=custom_prompt_template, input_variables=["question"]
            )
            chain = GraphCypherQAChain.from_llm(
                llm=self.llm,
                verbose=True,
                allow_dangerous_requests=True,
                graph=self.graphDB,
                qa_prompt=CUSTOM_PROMPT,
            )
            result = chain.run({'query':query}) # result = yes
            return result
                        
        def close(self):
            self.graphDB.close()
            print("Connection closed")  


            