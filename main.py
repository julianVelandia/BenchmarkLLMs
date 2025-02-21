from constants.models import MODELS
from services.completion_service import run_model_on_questions
from services.data_service import get_questions_answers
from services.json_service import filter_unprocessed_models, save_results


def main():
    models = filter_unprocessed_models(MODELS)
    questions_answers = get_questions_answers(100, 40)
    for model in models:
        model_answers = run_model_on_questions(questions_answers, model)
        save_results(model, model_answers)


main()
