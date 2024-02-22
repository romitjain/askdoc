import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer

class UserHistory:
    def __init__(self) -> None:
        self.encoder = SentenceTransformer('pritamdeka/S-PubMedBert-MS-MARCO')
        """
        We need a data structure like this:
        - idx
        - encoding
        - 
        """

    def embed_documents(self, documents):
        """
        Embed a list of documents using the provided embedding model.

        :param documents: List of documents to embed
        :param embedding_model: A model to convert documents to embeddings
        :return: Numpy array of document embeddings
        """
        embeddings = [self.encoder.encode(doc) for doc in documents]
        return np.array(embeddings)


    def search(self, query, top_k=5):
        """
        Search for the most similar documents to a query embedding.
        """
        similarities = cosine_similarity(query_embedding.reshape(1, -1), document_embeddings)
        top_k_indices = np.argsort(similarities[0])[::-1][:top_k]
        return top_k_indices

