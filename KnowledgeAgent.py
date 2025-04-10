from KnowledgeGraphService import KnowledgeGraphService

class KnowledgeAgent:
    def __init__(self, kg_service: KnowledgeGraphService, validator=None):
        """
        Parameters:
        - kg_service: An object responsible for querying the knowledge graph.
        - llm_service: An object for generating answers using an LLM.
        - validator: (Optional) A component to verify factual alignment with KG.
        """
        self.kg = kg_service
        self.validator = validator

    def answer_query(self, query: str, config: str = "community_only") -> dict:
        """
        Accepts a user query and returns a response based on configured data sources.
        config options: "community_only", "politifact_only", "hybrid"
        """
        # Step 1: Query KG for relevant facts
        facts = self.kg.get_facts(query)
        print(f"Facts retrieved: {facts}")
        
        # TODO 
        # factual validation
        # if self.validator:
        #     is_valid = self.validator.validate(response, facts)
        #     return {
        #         "answer": response,
        #         "valid": is_valid,
        #         "source": config
        #     }
        
        # return {
        #     "answer": response,
        #     "source": config
        # }
    def answer_extraction(self, answer: str) -> str:
        """
        Accepts an answer and extracts the relevant information.
        """
        # TODO  