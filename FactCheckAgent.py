from KnowledgeGraphService import KnowledgeGraphService, Graph
from MongoDBService import MongoDBService
from langchain_openai import ChatOpenAI
from langchain.tools import Tool
from langchain.agents import initialize_agent, AgentType
from langchain.memory import ConversationBufferMemory
from TwitterXAPIService import TwitterXAPIService
from langchain_core.prompts import PromptTemplate

import os

custom_prompt = PromptTemplate(
    input_variables=["question"],
    template="""
    Based on the following context, answer the question. Return:
    - Answer: yes/no
    - Explanation:
    - Source: Community Note or URL if available
    Question: {question}
    """
)

            
class FactCheckAgent:
    def __init__(self, kg_service: KnowledgeGraphService, mongo_service: MongoDBService, temperature=0, model_name="gpt-4-turbo"):
        self.kg_service = kg_service
        if mongo_service is not None:
            self.mongo_service = mongo_service
        OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
        if OPENAI_API_KEY is None:
            raise ValueError("OPENAI_API_KEY environment variable not set.")
        self.llm = ChatOpenAI(openai_api_key=OPENAI_API_KEY,temperature=temperature, model_name=model_name)
        self.twitter_api_service = TwitterXAPIService(
            api_key=os.getenv("TWITTER_API_KEY"),
            api_secret_key=os.getenv("TWITTER_API_SECRET_KEY"),
            access_token=os.getenv("TWITTER_ACCESS_TOKEN"),
            access_token_secret=os.getenv("TWITTER_ACCESS_TOKEN_SECRET"),
            bearer_token=os.getenv("TWITTER_ACCESS_BEARER_TOKEN")
        )
    
        tool = Tool(
            name="FactCheck",
            func=self.fact_check,
            description="Query graph data from Neo4j and MongoDB. "
                        "Use this tool to check the factuality of a statement. "
        )
        
        tools = [tool]
        self.memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

        self.agent = initialize_agent(
            tools,
            self.llm,
            agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
            verbose=True,
            memory=self.memory,
            additional_kwargs={"prompt": custom_prompt},
        )
        
    def get_facts(self, query: str, config: Graph) -> dict:
        facts = self.kg_service.get_facts(query)        
        return {
                "answer": facts,
        }

    def get_fact_for_verdict(self, query: str, config: Graph) -> dict:
        """
        Accepts a user query and returns a response based on configured data sources.
        config options: "community_only", "politifact_only", "hybrid"
        """
        # Step 1: Query KG for relevant facts
        facts = self.kg_service.get_facts_for_verdict(query, config)        
        is_factual = self.answer_extraction(facts)
        return {
                "answer": facts,
                "is_factual": is_factual,
                "source": config
        }
    
        
    def answer_extraction(self, answer: str) -> bool:
        print(f"Answer: {answer}")
        if answer.lower().startswith("yes"):
            return True
        elif answer.lower().startswith("no"):
            return False
        else:
            raise ValueError("Answer must be 'Yes' or 'No'")
    
    def get_facts_by_twitter_id(self, twitter_id: str) -> dict:
        """
        Retrieve facts for a given Twitter ID.
        """
        statement = self.twitter_api_service.get_tweet(twitter_id)
        return self.fact_check(statement)
    
    
    def fact_check(self,statement: str) -> str:
        mongo_context = None
        if self.mongo_service is not None:
            try:
                mongo_context = self.mongo_service.search(statement)
                print(f"MongoDB Context: {mongo_context}")
            except Exception as e:
                print(f"Error searching MongoDB: {e}")    

        return self.kg_service.get_facts(statement) 
    
    def invoke(self, twitter_id: str) -> dict:
        """
        Run the agent with the provided query.
        """
        
        response = self.twitter_api_service.get_tweet(twitter_id)
        statement = response["data"][0]["text"]
        print(f"Statement: {statement}")
        if not statement:
            raise ValueError("No text found in the tweet.")
        response = self.agent.invoke({"input": statement})
        return response

     
        


