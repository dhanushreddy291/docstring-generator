import json
import requests
from flask import Flask
from flask import request
from flask import Response

app = Flask(__name__)
TOKEN = "Your API TOKEN from BotFather"


def imageAsDict(imageURL, caption):
    """

    Creates a dictionary object with the given image URL and caption. This function is useful for creating a JSON object that can be used to represent an image in a chatbot or other application.

    Args:
        imageURL (str): The URL of the image.
        caption (str): The caption to be displayed with the image.

    Returns:
        dict: A dictionary object with the following keys:
            - type: The type of media, which is always "photo" for images.
            - media: The URL of the image.
            - caption: The caption to be displayed with the image.

    """
    return {
        "type": "photo",
        "media": imageURL,
        "caption": caption,
    }


def sendMediaGroup(chatid, allImages):
    """
    Sends a media group to a Telegram chat using the Telegram Bot API. The media group consists of a list of images, each with a prompt or caption.

    Args:
        chatid (int): The ID of the chat to send the media group to.
        allImages (list): A list of dictionaries, where each dictionary contains the following keys:
            - src: The URL of the image.
            - prompt: The caption or prompt to be displayed with the image.

    Returns:
        requests.Response: The response object returned by the Telegram API.
    """
    url = f"https://api.telegram.org/bot{TOKEN}/sendMediaGroup"
    media = [imageAsDict(allImages[i]["src"], allImages[i]["prompt"]) for i in range(5)]
    payload = {"chat_id": chatid, "media": media}
    r = requests.post(url, json=payload)
    return r


def sendMessage(chat_id, text):
    """
    Sends a text message to a Telegram chat using the Telegram Bot API.

    Args:
        chat_id (int): The ID of the chat to send the message to.
        text (str): The text message to be sent.

    Returns:
        requests.Response: The response object returned by the Telegram API.
    """
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    r = requests.post(url, json=payload)
    return r


@app.post("/")
def index():
    """
    Defines a FastAPI route that listens for incoming messages from a Telegram chatbot. When a message is received, the function extracts the chat ID and input text from the message. If the input text is "/start", the function sends a greeting message to the chat. Otherwise, the function sends a media group containing images related to the input text, obtained from the Lexica API.

    Returns:
        Response: A response object with a status code of 200 to indicate that the request was successful.
    """
    msg = request.get_json()
    chat_id = msg["message"]["chat"]["id"]
    inputText = msg["message"]["text"]
    if inputText == "/start":
        sendMessage(chat_id, "Ya, I am Online. Send me a Prompt")
    else:
        BASE_URL = "https://lexica.art/api/v1/search?q=" + str(inputText)
        response = requests.get(BASE_URL)
        response_text = json.loads(response.text)
        allImages = response_text["images"]
        sendMediaGroup(chat_id, allImages)
    return Response("ok", status=200)
