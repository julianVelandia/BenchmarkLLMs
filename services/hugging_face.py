from huggingface_hub import HfApi


def upload_to_huggingface(filename: str = "models_answers.json",
                          repo_id: str = "JulianVelandia/llms-answers-unal-repository",
                          token: str = None):
    api = HfApi()

    try:
        api.upload_file(
            path_or_fileobj=filename,
            path_in_repo=filename,
            repo_id=repo_id,
            repo_type="model",
            token=token
        )
        print(f"File '{filename}' successfully uploaded to '{repo_id}'.")
    except Exception as e:
        print(f"Error uploading file: {e}")
