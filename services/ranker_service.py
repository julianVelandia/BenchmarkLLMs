import random
import time
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


def get_completion_ranker(list_answers: list, real_answer: str):
    retries = 5
    client = OpenAI(api_key=OPENAI_API_KEY)

    for attempt in range(retries):
        try:
            all_answers = list_answers + [{"model": real_answer}]
            randomized_answers = [f"{i + 1}: {random.choice(all_answers)['model']}" for i in range(len(all_answers))]
            prompt = (
                    "Rank the following responses from best to worst based on accuracy and relevance to the question. "
                    "Only return the ranking in a numbered list format, like this: \n1: model_name\n2: model_name\n...\n"
                    "Here are the responses: \n" + "\n".join(randomized_answers)
            )
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                stream=False,
            )
            ranking = response.choices[0].message.content.strip().split("\n")
            return [rank.split(": ")[1] for rank in ranking if ": " in rank]
        except Exception:
            time.sleep(10)
    return "Failed to rank the responses after multiple attempts"
