# Community Notes as an Efficient Fact-Checking Source

## Abstract
Community Notes, a crowdsourced fact- checking system on Twitter/X, offers contextual annotations to potentially misleading posts as an alternative to expert and automate fact- checking. This study explores the feasibility of using published Community Notes as a standalone fact-checking source. We hypothesize that Community Notes, as a curated knowledge base, can improve fact-checking efficiency without compromising accuracy. Un-like large-scale fact-checking systems, Community Notes offers a targeted approach that captures recurring misinformation topics. To test this, we will create a knowledge graph (KG) from Community Notes using large language models (LLMs) and integrate it into an automated fact-checking pipeline, applying Knowledge-Augmented Generation (KAG) and Retrieval-Augmented Generation (RAG) techniques. We will evaluate the system by com- paring its outputs to established fact-checking datasets like DBPedia, . This report outlines the literature review, data collection, preliminary experiments, methodology, evaluation strategy, and project tasks.

## Files
- `BuildGraph.py`: This file is used to build the knowledge graph from the Community Notes data.
- `AnalyzeAccuracy.py`: This file is used to analyze the accuracy of the knowledge graph.
- `NotesProcessor.py`: This file is a class that processes the Community Notes files and extracts relevant information.
- `MongoDBService.py`: This file is used to connect to the MongoDB database and perform operations on it.
- `KnowledgeGraphService.py`: This file is used to connect to the Neo4j database and perform operations on it.
- `FactCheckAgent.py`: this file is used to create a fact-checking agent that uses the knowledge graph and the Community Notes data to perform fact-checking.
- `API.py`: this file is used to create a REST API for the fact-checking agent.


## Published Knowledge Graph from X's Community Notes
Please provide us with your email address of Neo4j Aura if you want to access the knowledge graph. We will send you the invitation link to access the knowledge graph.

![Knowledge Graph](image/KG_public.png "Knowledge Graph")


## How to setup in your local environment
1. Download Neo4j Desktop
2. Install APOC plugin and follow their instruction
https://neo4j.com/docs/apoc/5/installation/?_gl=1*1gdaha5*_ga*MTk0MDk5NjkzNy4xNzQxNjUyMjM2*_ga_DZP8Z65KK4*MTc0MTY1MjIzNC4xLjEuMTc0MTY1NTIyNi4wLjAuMA..
3. create 2 database 
```
- community
- news_articles
```

(optional) if there is problem with APOC, you can add the following lines to your `neo4j.conf` file:

```
dbms.security.procedures.unrestricted=apoc.*
dbms.security.procedures.allowlist=apoc.*
```

4. Clone this repository:

```
git clone https://github.com/courtofdreams/llm-kag-communitynote.git
cd llm-kag-communitynote
```
5. Create and activate a virtual environment:

```
# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

6. Install the required dependencies:

```
pip install -r requirements.txt
```

4. Create a `.env` file in the project root with:

```
 OPENAI_API_KEY=your-openai-api-key
 NEO4J_URI=neo4j_uri ex : bolt://localhost:7687
 NEO4J_USERNAME=your-neo4j-username
 NEO4J_PASSWORD=NEO4J_USERNAME=your-neo4j-password
```
(optional) if you want to use the chrome extension, add the following lines to your `.env` file:
```
TWITTER_API_KEY=
TWITTER_API_SECRET_KEY=
TWITTER_ACCESS_BEARER_TOKEN=
TWITTER_ACCESS_TOKEN=
TWITTER_ACCESS_TOKEN_SECRET=
```

5. To build the knowledge graph, run the following command:

```
python3 -m BuildGraph.py 
```

```
enter 1: for building community notes knowledge graph
enter 2: for building news articles/other compared knowledge graph
```

after that, you will be asked enter data file path, you can use the following data files:
data/graph_data/mislead_politics.xlsx


6. to verify the knowledge graph, run the following command:

```
python3 -m AnalyzeAccuracy.py 
```

7. To run the API, run the following command:

```
python3 -m API.py
```

