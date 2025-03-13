import json

import matplotlib.pyplot as plt
import pandas as pd


def simplify_model_name(model_name):
    mapping = {
        "lmstudio-community/Llama-3.2-1B-Instruct-GGUF/Llama-3.2-1B-Instruct-Q8_0.gguf": "LLM",
        "lmstudio-community/Llama-3.2-1B-Instruct-GGUF/Llama-3.2-1B-Instruct-Q8_0.gguf+RAG": "LLM-rag",
        "lmstudio-community/Llama-3.2-1B-Instruct-GGUF/Llama-3.2-1B-Instruct-Q4_K_M.gguf": "LLM-q",
        "lmstudio-community/Llama-3.2-1B-Instruct-GGUF/Llama-3.2-1B-Instruct-Q4_K_M.gguf+RAG": "LLM-q-rag",
        "JulianVelandia/Llama-3.2-1B-unal-instruct-ft-gguf/model-f16.gguf": "LLM-ft",
        "JulianVelandia/Llama-3.2-1B-unal-instruct-ft-gguf/model-f16.gguf+RAG": "LLM-ft-rag",
        "JulianVelandia/Llama-3.2-1B-unal-instruct-ft-gguf/model-q4_k_m.gguf": "LLM-ft-q",
        "JulianVelandia/Llama-3.2-1B-unal-instruct-ft-gguf/model-q4_k_m.gguf+RAG": "LLM-ft-q-rag",
        "JulianVelandia/Llama-3.2-1B-unal-instruct-q-ft-gguf/model-f16.gguf": "LLM-q-ft",
        "JulianVelandia/Llama-3.2-1B-unal-instruct-q-ft-gguf/model-f16.gguf+RAG": "LLM-q-ft-rag",
    }
    return mapping.get(model_name, model_name)


def analyze_model_performance(json_file):
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    rankings = [entry["ranking"] for entry in data[:100]]
    model_positions = {simplify_model_name(model): [] for model in rankings[0]}

    for ranking in rankings:
        for position, model in enumerate(ranking, start=1):
            model_positions[simplify_model_name(model)].append(position)

    model_stats = {model: {"avg_position": sum(pos) / len(pos), "first_place": pos.count(1)} for model, pos in
                   model_positions.items()}
    df = pd.DataFrame.from_dict(model_stats, orient='index').sort_values(by='avg_position')

    plt.figure(figsize=(14, 7))
    df['avg_position'].plot(kind='bar', title='Average Ranking Position')
    plt.xlabel('Model')
    plt.ylabel('Avg Position (Lower is Better)')
    plt.xticks(rotation=45, ha='right')
    plt.show()

    plt.figure(figsize=(14, 7))
    df['first_place'].plot(kind='bar', title='First Place Count')
    plt.xlabel('Model')
    plt.ylabel('Count of First Places')
    plt.xticks(rotation=45, ha='right')
    plt.show()

    print("Model Performance Statistics:")
    print(df)


analyze_model_performance('../model_answers_ranking.json')
