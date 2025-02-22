import random
import time
import os
import json
from collections import defaultdict
from openai import OpenAI
from dotenv import load_dotenv


def load_model_results(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


def prepare_ranking_data(model_results):
    questions_dict = defaultdict(lambda: {"list_answers": [], "real_answer": None})

    for model_name, responses in model_results.items():
        for entry in responses:
            question = entry["question"]
            real_answer = entry["answer"]
            llm_answer = entry["llm_answer"]

            questions_dict[question]["list_answers"].append({"model_name": model_name, "response": llm_answer})
            if questions_dict[question]["real_answer"] is None:
                questions_dict[question]["real_answer"] = real_answer

    return [
        {"question": question, "list_answers": data["list_answers"], "real_answer": data["real_answer"]}
        for question, data in questions_dict.items()
    ]


def get_completion_ranker(list_answers, real_answer, api_key):
    retries = 5
    client = OpenAI(api_key=api_key)

    for attempt in range(retries):
        try:
            random.shuffle(list_answers)  # Mezclar respuestas para evitar sesgo
            formatted_responses = [f"{i + 1}: {entry['response']}" for i, entry in enumerate(list_answers)]

            prompt = (
                    "Rank the following responses from best to worst based on accuracy and relevance to the question. "
                    "Only return the ranking in a numbered list format, like this: \n1: model_name\n2: model_name\n...\n"
                    "Here are the responses:\n\n"
                    + "\n".join(formatted_responses) +
                    f"\n\nThe correct answer is:\n{real_answer}"
            )

            response = client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                stream=False,
            )

            ranking_text = response.choices[0].message.content.strip().split("\n")

            ranked_models = []
            for rank in ranking_text:
                for entry in list_answers:
                    if entry["response"] in rank:
                        ranked_models.append(entry["model_name"])
                        break

            return ranked_models
        except Exception:
            time.sleep(10)
    return "Failed to rank the responses after multiple attempts"


def main():
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    model_results_file = "../models_answers.json"
    model_results = load_model_results(model_results_file)
    organized_data = prepare_ranking_data(model_results)

    rankings_results = []
    organized_data = organized_data[:2]
    for question_data in organized_data:
        ranking = get_completion_ranker(question_data["list_answers"], question_data["real_answer"], api_key)
        rankings_results.append({"question": question_data["question"], "ranking": ranking})

    print(json.dumps(rankings_results, indent=4, ensure_ascii=False))


if __name__ == "__main__":
    main()
