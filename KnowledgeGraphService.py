import os

from langchain_community.graphs import Neo4jGraph
from langchain_experimental.graph_transformers import LLMGraphTransformer
from langchain_core.documents import Document
from langchain_neo4j import Neo4jGraph, GraphCypherQAChain
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_deepseek import ChatDeepSeek
from langchain_core.prompts import PromptTemplate
from enum import Enum

class Graph(Enum):
    COMMUNITY = "community"
    POLITIFACT = "politifact"
    BASELINE = "baseline"
    
class KnowledgeGraphService:
        def __init__(self, temperature=0, model_name="gpt-4-turbo"):   
            OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
            if OPENAI_API_KEY is None:
                raise ValueError("OPENAI_API_KEY environment variable not set.")
            
            self.llm = ChatOpenAI(openai_api_key=OPENAI_API_KEY,temperature=temperature, model_name=model_name)

            # GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
            # if GOOGLE_API_KEY is None:
            #     raise ValueError("GOOGLE_API_KEY environment variable not set.")
            
            # self.llm = ChatGoogleGenerativeAI(
            #     model="gemini-2.0-flash",
            #     temperature=0,                  
            #     max_tokens=None,
            #     timeout=None,
            #     max_retries=2,
            # )
            
            # DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
            # if DEEPSEEK_API_KEY is None:
            #     raise ValueError("DEEPSEEK_API_KEY environment variable not set.")
            
            # self.llm = ChatDeepSeek(
            #     model="deepseek-chat",
            #     temperature=0,
            #     max_tokens=None,
            #     timeout=None,
            #     max_retries=2,
            # )

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
            combined_text = '\n'.join(data)
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
                result = chain.run({'query':query}) # result = yes
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
            elif config == Graph.BASELINE: # TODO baseline = only use the LLM, Need to decide what model to use., this will call openai or xxx directly
                chain = GraphCypherQAChain.from_llm(
                    llm=self.llm,
                    verbose=True,
                    allow_dangerous_requests=True,
                    graph=None,
                    qa_prompt=CUSTOM_PROMPT,
                )
                return result
            else:    
                raise ValueError("Invalid config. Choose 'community' or 'politifact'.")        

        def get_facts(self, query: str):
            custom_prompt_template = """
                check the factuality of the statement and give out the result as yes or no based on community graph
                additionally, give out the reasoning for the answer
                
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


            