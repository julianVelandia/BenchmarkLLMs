from datasets import load_dataset

from constants.datasets import DATASET_HF


def get_questions_answers(num_questions: int, skip: int):
    dataset = load_dataset(DATASET_HF)['train']
    data = [(example['prompt'], example['completion']) for example in dataset]
    result = [
                 {'question': data[i][0], 'answer': data[i][1]}
                 for i in range(0, len(data), skip + 1)
             ][:num_questions]
    return result
