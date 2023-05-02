from transformers import pipeline
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    """

    Returns a JSON response with a simple greeting message "Hello World" when the root URL is accessed.

    Returns:
        dict: A dictionary containing the greeting message "Hello World".

    """
    return {"Hello": "World"}


@app.get("/emotion")
def read_item(text: str):
    """
    Returns the predicted emotion label for the given text input using a pre-trained DistilRoBERTa-based emotion classification model.

    Args:
        text (str): The input text to be classified.

    Returns:
        dict: A dictionary containing the predicted emotion label for the input text.
    """
    classifier = pipeline(
        "text-classification",
        model="j-hartmann/emotion-english-distilroberta-base",
        top_k=None,
    )
    return classifier(text)
