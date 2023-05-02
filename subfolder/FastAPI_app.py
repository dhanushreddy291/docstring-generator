from transformers import pipeline
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    """

    Returns a JSON response with a simple "Hello World" message.
    "
    """
    return {"Hello": "World"}


@app.get("/emotion")
def read_item(text: str):
    """
    This function is a FastAPI route that takes in a string parameter 'text' and returns a JSON response with the predicted emotion of the input text. The emotion is predicted using a pre-trained DistilRoBERTa model for English language. The function uses the Hugging Face Transformers library to load the pre-trained model and generate the prediction.
    """
    classifier = pipeline(
        "text-classification",
        model="j-hartmann/emotion-english-distilroberta-base",
        top_k=None,
    )
    return classifier(text)
