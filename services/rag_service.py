from rag import Rag


def get_rag(query: str):
    rag = Rag()
    return rag.retrieval_augmented_generation(query)
