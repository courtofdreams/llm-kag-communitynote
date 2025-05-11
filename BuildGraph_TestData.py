# TODO: Build it with the actual data

from KnowledgeGraphService import KnowledgeGraphService, Graph


kg_service = KnowledgeGraphService(0.1,"gpt-4.1-nano")

# community_note_data = """
# Elon Musk, born in South Africa in 1971, is a tech entrepreneur best known for founding SpaceX, cofounding PayPal, and leading Tesla. He became the world’s richest person by 2025 with a net worth of $393 billion and also acquired Twitter (renamed X) in 2022.
# """

politifact_data = """
Since 2012, Donald Trump and many other Republicans have claimed there was substantial voter fraud in US elections and that, if not for that fraud, Trump would have won the popular vote in the 2016 election (he lost by 2,868,686 million votes), and would have won the 2020 election (he lost by 7,052,770 million votes) and be president today.

To try to gain an objective view of the election and voter fraud claims, this section charts all election and voter fraud convictions in US elections between 2016 and 2020.

There have been 306 election and voter fraud convictions to date – including fraudulently voting and registering to vote, false declaration of candidacy, and facilitating or attempting to vote illegally. Included are convictions from the 2016, 2018, and 2020 federal elections, as well as other types of elections, with a focus on the potential election impact on congressional or presidential election results.

The information comes from online news stories, official court records, the Heritage Foundation Election Fraud Database, and other sources. We have included our own summaries and attempted to add the case number and political party for every case listed. We will continue to look for the information currently listed as “not found.”

Please let us know of any voter fraud convictions we have missed.
"""

# kg_service.build_graph(community_note_data, Graph.COMMUNITY)
kg_service.build_graph(politifact_data, Graph.POLITIFACT)



    
        
        