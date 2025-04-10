class Validator:
    def validate(self, answer, facts):
        # Very simple check for now — expand with semantic similarity if needed
        return any(fact.lower() in answer.lower() for fact in facts)