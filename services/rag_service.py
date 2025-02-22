def get_rag(query, rag, max_sections=2, threshold=0.35, max_words=250):
    return rag.retrieval_augmented_generation(query=query, threshold=threshold, max_sections=max_sections,
                                              max_words=max_words)
