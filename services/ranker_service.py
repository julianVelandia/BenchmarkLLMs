import json
import os
import random
import time
from collections import defaultdict

from dotenv import load_dotenv
from openai import OpenAI


def load_model_results(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


def load_existing_rankings(file_path="../model_answers_ranking.json"):
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                return []
    return []


def save_ranking_result(new_result, file_path="../model_answers_ranking.json"):
    existing_results = load_existing_rankings(file_path)

    existing_questions = {entry["question"] for entry in existing_results}
    if new_result["question"] in existing_questions:
        return

    existing_results.append(new_result)
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(existing_results, file, indent=4, ensure_ascii=False)


def prepare_ranking_data(model_results):
    questions_dict = defaultdict(lambda: {"list_answers": [], "real_answer": None})

    for model_name, responses in model_results.items():
        for entry in responses:
            question = entry.get("question")
            if not question:
                continue

            real_answer = entry.get("answer", "No respuesta")
            llm_answer = entry.get("llm_answer", "No respuesta")

            questions_dict[question]["list_answers"].append(
                {"model_name": model_name, "response": llm_answer if llm_answer.strip() else "No respuesta"})
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
            random.shuffle(list_answers)
            formatted_responses = [f"{i + 1}: {entry['response']}" for i, entry in enumerate(list_answers)]

            prompt = (
                    "Rank the following responses from best to worst based on their accuracy and relevance to the question. "
                    "Return only a numbered list with model numbers, like this: \n3, 5, 6, 4, 2, 1\n"
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

            ranking_text = response.choices[0].message.content.strip()

            ranked_numbers = ranking_text.split(",")
            ranked_models = []
            for num in ranked_numbers:
                index = int(num.strip()) - 1
                if 0 <= index < len(list_answers):
                    ranked_models.append(list_answers[index]["model_name"])

            return ranked_models if ranked_models else "no respuesta"
        except Exception:
            time.sleep(10)
    return "no respuesta"


def ranking_llms(model_results_file="../models_answers.json"):
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    model_results = load_model_results(model_results_file)
    organized_data = prepare_ranking_data(model_results)
    existing_rankings = load_existing_rankings()
    existing_questions = {entry["question"] for entry in existing_rankings}

    for question_data in organized_data:
        if question_data["question"] in existing_questions:
            continue

        ranking = get_completion_ranker(question_data["list_answers"], question_data["real_answer"], api_key)
        result = {"question": question_data["question"], "ranking": ranking}
        save_ranking_result(result)
        print(json.dumps(result, indent=4, ensure_ascii=False))


ranking_llms()
