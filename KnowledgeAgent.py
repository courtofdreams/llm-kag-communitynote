from KnowledgeGraphService import KnowledgeGraphService, Graph


class KnowledgeAgent:
    def __init__(self, kg_service: KnowledgeGraphService):
        """
        Parameters:
        - kg_service: An object responsible for querying the knowledge graph.
        - llm_service: An object for generating answers using an LLM.
        - validator: (Optional) A component to verify factual alignment with KG.
        """
        self.kg = kg_service

    def answer_query(self, query: str, config: Graph) -> dict:
        """
        Accepts a user query and returns a response based on configured data sources.
        config options: "community_only", "politifact_only", "hybrid"
        """
        # Step 1: Query KG for relevant facts
        facts = self.kg.get_facts(query, config)        
        # TODO 
        is_factual = self.answer_extraction(facts)
        return {
                "answer": facts,
                "is_factual": is_factual,
                "source": config
            }
        
    def answer_extraction(self, answer: str) -> bool:
        if answer.lower().startswith("yes"):
            return True
        elif answer.lower().startswith("no"):
            return False
        else:
            raise ValueError("Answer must be 'Yes' or 'No'")
        
        