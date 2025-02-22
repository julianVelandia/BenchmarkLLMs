from rag import Rag

from constants.datasets import RAG_HF_DATASET
from constants.models import MODELS
from services.completion_service import run_model_on_questions
from services.data_service import get_questions_answers
from services.json_service import filter_unprocessed_models, save_results


def main():
    rag = Rag(hf_dataset=RAG_HF_DATASET)
    models = filter_unprocessed_models(MODELS)
    print('models', models)
    questions_answers = get_questions_answers(100, 40)
    for model in models:
        model_answers = run_model_on_questions(questions_answers, model, rag)
        save_results(model, model_answers)



main()
