from flask import Flask, jsonify
from KnowledgeGraphService import KnowledgeGraphService
from MongoDBService import MongoDBService
from FactCheckAgent import FactCheckAgent
import os

app = Flask(__name__)

databaseName = "community-note-mongo"
collectionName = "community"
mongodbUri = os.getenv("MONGO_DB_URI")
mongo_service = MongoDBService(mongodbUri, databaseName, collectionName)
model = "gpt-4-turbo"
temperature = 0
kg_service = KnowledgeGraphService(temperature,model)
agent = FactCheckAgent(kg_service=kg_service,mongo_service=mongo_service,temperature=temperature,model_name=model)


@app.route('/get-facts/<string:twitter_id>', methods=['GET'])
def get_facts(twitter_id):
    """
    API endpoint to retrieve facts for a given Twitter ID.
    """
    try:
        # Query the knowledge graph for facts related to the Twitter ID
        facts = agent.invoke(twitter_id)
        final_answer = facts.get("output", "No answer generated.")
        return jsonify({
            "twitter_id": twitter_id,
            "result": final_answer
        }), 200
    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500
        
        

if __name__ == '__main__':
    app.run(debug=True)