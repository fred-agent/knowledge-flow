from typing import List
from langchain.embeddings.base import Embeddings


class Embedder(Embeddings):
    """
    Generic Embedder
    -------------------
    1. Generic wrapper around a LangChain-compatible embedding model.
    2. Conforms to LangChain's Embeddings interface.
    3. Can be passed directly to OpenSearchVectorSearch or any LangChain component.
    """

    def __init__(self, model: Embeddings):
        """
        Args:
            model (Embeddings): A LangChain-compatible embedding model (e.g., OpenAIEmbeddings, AzureOpenAIEmbeddings).
        """
        self.model = model

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """
        Embed a list of text chunks (as required by LangChain's interface).

        Args:
            texts (List[str]): List of raw text strings to embed.

        Returns:
            List[List[float]]: List of embeddings.
        """
        return self.model.embed_documents(texts)

    def embed_query(self, text: str) -> List[float]:
        """
        Embed a single query (e.g., for similarity search).

        Args:
            text (str): The text to embed.

        Returns:
            List[float]: The embedding.
        """
        return self.model.embed_query(text)
