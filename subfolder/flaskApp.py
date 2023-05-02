import os
import json
import requests
from flask import Flask
from flask import request
from flask import Response

app = Flask(__name__)
TOKEN = "Your API TOKEN from BotFather"

def imageAsDict(imageURL, caption):
    return {
        "type": "photo",
        "media": imageURL,
        "caption": caption,
    }


def sendMediaGroup(chatid, allImages):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMediaGroup"
    media = [imageAsDict(allImages[i]["src"], allImages[i]["prompt"]) for i in range(5)]
    payload = {"chat_id": chatid, "media": media}
    r = requests.post(url, json=payload)
    return r

def sendMessage(chat_id, text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    r = requests.post(url, json=payload)
    return r

@app.post("/")
def index():
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
