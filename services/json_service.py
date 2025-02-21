import os
import json


def save_results(model: str, results: list, filename: str = "results.json"):
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as file:
            data = json.load(file)
    else:
        data = {}
    data[model] = results
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


def load_existing_results(filename: str = "results.json"):
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as file:
            return json.load(file)
    return {}


def filter_unprocessed_models(models: list, filename: str = "results.json"):
    existing_results = load_existing_results(filename)
    return [model for model in models if model not in existing_results]
