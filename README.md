# Community Notes as an Efficient Fact-Checking Source

## Abstract
Community Notes, a crowdsourced fact- checking system on Twitter/X, offers contex- tual annotations to potentially misleading posts as an alternative to expert and automate fact- checking. This study explores the feasibil- ity of using published Community Notes as a standalone fact-checking source. We hy- pothesize that Community Notes, as a curated knowledge base, can improve fact-checking ef- ficiency without compromising accuracy. Un- like large-scale fact-checking systems, Com- munity Notes offers a targeted approach that captures recurring misinformation topics. To test this, we will create a knowledge graph (KG) from Community Notes using large lan- guage models (LLMs) and integrate it into an automated fact-checking pipeline, applying Knowledge-Augmented Generation (KAG) and Retrieval-Augmented Generation (RAG) tech- niques. We will evaluate the system by com- paring its outputs to established fact-checking datasets like PolitiFact. This report outlines the literature review, data collection, preliminary experiments, methodology, evaluation strategy, and project tasks.


## How to setup in your local environment

1. Download Neo4j Desktop

2. Install APOC plugin and follow their instruction
https://neo4j.com/docs/apoc/5/installation/?_gl=1*1gdaha5*_ga*MTk0MDk5NjkzNy4xNzQxNjUyMjM2*_ga_DZP8Z65KK4*MTc0MTY1MjIzNC4xLjEuMTc0MTY1NTIyNi4wLjAuMA..

3. (optional) if there is problem with APOC, you can add the following lines to your `neo4j.conf` file:

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

5. # TODO

