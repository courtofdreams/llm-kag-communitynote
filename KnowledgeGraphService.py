import os

from langchain_community.graphs import Neo4jGraph
from langchain_experimental.graph_transformers import LLMGraphTransformer
from langchain_core.documents import Document
from langchain_neo4j import Neo4jGraph, GraphCypherQAChain
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from enum import Enum
from langchain.chains import LLMChain

class Graph(Enum):
    COMMUNITY = "community3topics"
    POLITIFACT = "politifact"
    BASELINE = "baseline"
    
class KnowledgeGraphService:
        def __init__(self, temperature=0, model_name="gpt-4-turbo"):   
            OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
            if OPENAI_API_KEY is None:
                raise ValueError("OPENAI_API_KEY environment variable not set.")
            
            self.llm = ChatOpenAI(openai_api_key=OPENAI_API_KEY,temperature=temperature, model_name=model_name)

            self.graph_politifact = Neo4jGraph(
                database=Graph.POLITIFACT.value
            )

            self.graph_community = Neo4jGraph(
                database=Graph.COMMUNITY.value
            )
            
            self.llm_transformer = LLMGraphTransformer(
                llm=self.llm
            )          
        
        def build_graph(self, text, config: Graph):
            documents = [Document(page_content=text)]
            graph_documents = self.llm_transformer.convert_to_graph_documents(documents)
            print(f"Nodes:{graph_documents[0].nodes}")
            print(f"Relationships:{graph_documents[0].relationships}")
            if config == Graph.COMMUNITY:
                self.graph_community.add_graph_documents(graph_documents)
            elif config == Graph.POLITIFACT:
                self.graph_politifact.add_graph_documents(graph_documents)
            else:
                raise ValueError("Invalid config. Choose 'community' or 'politifact'.")   
        
        def build_multiple_graphs(self, data: list, config: Graph):
            combined_text = '\n'.join([doc['note'] for doc in data])
            documents = [Document(page_content=combined_text)]
            graph_documents = self.llm_transformer.convert_to_graph_documents(documents)
            if config == Graph.COMMUNITY:
                self.graph_community.add_graph_documents(graph_documents)
            elif config == Graph.POLITIFACT:
                self.graph_politifact.add_graph_documents(graph_documents)
            else:
                raise ValueError("Invalid config. Choose 'community' or 'politifact'.") 
            
        def reset_database(self, config: Graph):
            if config == Graph.COMMUNITY:
                with self.graph_community.session() as session:
                    session.run("MATCH (n) DETACH DELETE n")
                    print("Database reset successfully!")   
        
            elif config == Graph.POLITIFACT:
                with self.graph_politifact.session() as session:
                    session.run("MATCH (n) DETACH DELETE n")
                    print("Database reset successfully!")   
            else:
                raise ValueError("Invalid config. Choose 'community' or 'politifact'.")
        
        def search(self, query: str):
            with self.graph_community.session() as session:
                result = session.run(query)
            return [record.data() for record in result]
        
        def get_graph(self, config: Graph):
            if config == Graph.COMMUNITY:
                return self.graph_community
            elif config == Graph.POLITIFACT:
                return self.graph_politifact
            else:
                raise ValueError("Invalid config. Choose 'community' or 'politifact'.")
            
            
        def get_facts_for_verdict(self, query, config: Graph=Graph.COMMUNITY):
            custom_prompt_template = """
                check the factuality of the statement and give out the result as yes or no only
                Rules for Cypher:
                - Use MATCH for nodes/relationships.
                - WHERE only for properties (e.g., p.party = 'REPUBLICAN').
                - Use EXISTS((p)-[:REL]->(c)) correctly.
                - No backticks.
                - RETURN clean expressions, e.g., RETURN EXISTS((p)-[:AIM]->(c)).

                Statement: {question}
                Answer:
            """
            
            CUSTOM_PROMPT = PromptTemplate(
                template=custom_prompt_template, input_variables=["question"]
            )
            if config == Graph.COMMUNITY:
                chain = GraphCypherQAChain.from_llm(
                    llm=self.llm,
                    verbose=True,
                    allow_dangerous_requests=True,
                    graph=self.graph_community,
                    qa_prompt=CUSTOM_PROMPT,
                )
                result = chain.run({'query': query}) # result = yes
                return result
            elif config == Graph.POLITIFACT:
                print(f"Querying {config.value} database with query: {query}")
                chain = GraphCypherQAChain.from_llm(
                    llm=self.llm,
                    verbose=True,
                    allow_dangerous_requests=True,
                    graph=self.graph_politifact,
                    qa_prompt=CUSTOM_PROMPT,
                )
                result = chain.run({'query':query})
                return result
            elif config == Graph.BASELINE: # Blind Model
                custom_prompt_template = """
                check the factuality of the statement and give out the result as yes or no only
                Statement: {question}
                Answer:
                """
                CUSTOM_PROMPT = PromptTemplate(
                template=custom_prompt_template, input_variables=["question"]
                )
                chain = LLMChain(llm=self.llm, prompt=CUSTOM_PROMPT)
                result = chain.run({'question':query})
                return result
            else:    
                raise ValueError("Invalid config. Choose 'community' or 'politifact'.")        

        def get_facts(self, query: str):
            custom_prompt_template = """
                check the factuality of the statement and give out the result as yes or no based on community graph
                additionally, give out the reasoning for the answer use the community graph context
                
                Statement: {question}
                Answer:
            """
            
            CUSTOM_PROMPT = PromptTemplate(
                template=custom_prompt_template, input_variables=["query"]
            )
            
            chain = GraphCypherQAChain.from_llm(
                llm=self.llm,
                verbose=True,
                allow_dangerous_requests=True,
                graph=self.graph_community,
                qa_prompt=CUSTOM_PROMPT,
            )
            
            result = chain.run({'query':query}) # result = yes 
            return result
                        
        def close(self):
            self.graphDB.close()
            print("Connection closed")  


            