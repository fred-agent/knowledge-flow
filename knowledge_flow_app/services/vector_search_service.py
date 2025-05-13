# knowledge_flow_app/services/vector_search_service.py
from typing import List
from langchain.schema.document import Document
from knowledge_flow_app.application_context import ApplicationContext

class VectorSearchService:
    """
    Vector Search Service
    ------------------------------------------------------
    """ 
    def __init__(self):
        context = ApplicationContext.get_instance()
        embedder = context.get_embedder()
        self.vector_store = context.get_vector_store(embedder)

    def similarity_search_with_score(self, question: str, k: int = 10) -> List[tuple[Document, float]]:
        return self.vector_store.similarity_search_with_score(question, k=k)
