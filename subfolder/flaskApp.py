import json
import requests
from flask import Flask
from flask import request
from flask import Response

app = Flask(__name__)
TOKEN = "Your API TOKEN from BotFather"


def imageAsDict(imageURL, caption):
    """

    Converts an image URL and a caption into a dictionary object that can be used to represent an image in a message or post.

    Args:
        imageURL (str): The URL of the image.
        caption (str): The caption to be displayed with the image.

    Returns:
        dict: A dictionary object representing the image with the following keys:
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
    Sends a group of media (up to 5 images) to a Telegram chat using the Telegram Bot API.

    Args:
        chatid (int): The ID of the chat to send the media to.
        allImages (list): A list of dictionaries representing the images to be sent. Each dictionary should have the following keys:
            - src: The URL of the image.
            - prompt: The caption to be displayed with the image.

    Returns:
        requests.Response: The response object returned by the Telegram Bot API after sending the media group.
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
        text (str): The text of the message to be sent.

    Returns:
        requests.Response: The response object returned by the Telegram Bot API after sending the message.
    """
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    r = requests.post(url, json=payload)
    return r


@app.post("/")
def index():
    """
    This function is a route of a web app that receives incoming messages from a Telegram chat and sends a response based on the message received. If the message is "/start", it sends a greeting message to the chat. Otherwise, it sends a request to an external API to search for images related to the message received, and then sends a group of up to 5 images to the chat using the Telegram Bot API.

    Returns:
        Response: A response object with status code 200 to indicate that the request was successful.
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
