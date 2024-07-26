"""
This example uses LexRank (https://www.aaai.org/Papers/JAIR/Vol22/JAIR-2214.pdf)
to create an extractive summarization of a long document.
The document is splitted into sentences using NLTK, then the sentence embeddings are computed. We
then compute the cosine-similarity across all possible sentence pairs.
We then use LexRank to find the most central sentences in the document, which form our summary.
Input document: First section from the English Wikipedia Section
Output summary:
Located at the southern tip of the U.S. state of New York, the city is the center of the New York metropolitan area, the largest metropolitan area in the world by urban landmass.
New York City (NYC), often called simply New York, is the most populous city in the United States.
Anchored by Wall Street in the Financial District of Lower Manhattan, New York City has been called both the world's leading financial center and the most financially powerful city in the world, and is home to the world's two largest stock exchanges by total market capitalization, the New York Stock Exchange and NASDAQ.
New York City has been described as the cultural, financial, and media capital of the world, significantly influencing commerce, entertainment, research, technology, education, politics, tourism, art, fashion, and sports.
If the New York metropolitan area were a sovereign state, it would have the eighth-largest economy in the world.
"""
import nltk


from sentence_transformers import SentenceTransformer, util
import numpy as np
from LexRank import degree_centrality_scores


model = SentenceTransformer('all-MiniLM-L6-v2')

# Our input document we want to summarize
# As example, we take the first section from Wikipedia
document = """
Responsibilities
Design and build optimization algorithms for budget pacing and automated bidding to achieve various advertising goals
Establish a data-driven framework to understand how the bid density and market competitiveness would affect advertising value and platform revenue
Develop new data solutions (eg embeddings and consumer profiles) to target the relevant audience
Be responsible for the end-to-end ML lifecycle, including ideation, offline model training, online shadowing/deployment, experimentation, and post-launch monitoring/measurement
Build and extend the current data/ML infrastructure to empower Ads data applications including data analysis, ML modeling, and experimentation
Scale our systems and services to fuel the growth of our business
"""

# Split the document into sentences
sentences = nltk.sent_tokenize(document)
print("Num sentences:", len(sentences))

# Compute the sentence embeddings
embeddings = model.encode(sentences, convert_to_tensor=True)

# Compute the pair-wise cosine similarities
cos_scores = util.cos_sim(embeddings, embeddings).numpy()

# Compute the centrality for each sentence
centrality_scores = degree_centrality_scores(cos_scores, threshold=None)

# We argsort so that the first element is the sentence with the highest score
most_central_sentence_indices = np.argsort(-centrality_scores)


# Print the 5 sentences with the highest scores
print("\n\nSummary:")
for idx in most_central_sentence_indices[0:1]:
    print(sentences[idx].strip())

