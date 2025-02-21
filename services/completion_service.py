import time

from openai import OpenAI


def _get_completion_local(model: str, prompt: str) -> str:
    retries = 5
    for attempt in range(retries):
        try:
            client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")
            models_available = client.models.list()
            current_model = models_available.data[0].id if models_available.data else "None"
            if model not in [m.id for m in models_available.data]:
                print(f"Please start the LM Studio server with the model: {model}. Currently running: {current_model}")
                time.sleep(10)
                continue
            history = [
                {"role": "system",
                 "content": "Eres un asistente inteligente. Siempre das respuestas bien razonadas que son correctas, concretas, cortas y útiles."},
                {"role": "user", "content": prompt},
            ]
            completion = client.chat.completions.create(
                model=model,
                messages=history,
                temperature=0.7,
                stream=False,
            )
            return completion.choices[0].message.content.strip()
        except Exception:
            time.sleep(10)
    return "There was no response from the model"


def run_model_on_questions(data: list, model: str):
    template_prompt = "Answer the following question in a single sentence: {question}"
    for index, item in enumerate(data, start=1):
        print(f"Processing question {index} out of {len(data)}")
        prompt = template_prompt.format(question=item['question'])
        item['llm_answer'] = _get_completion_local(model, prompt)
    return data
