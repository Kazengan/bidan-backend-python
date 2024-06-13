import requests
import os
from dotenv import load_dotenv

def sender(nomor, text):
    load_dotenv()
    nomor = int(nomor)
    api_key = os.getenv("TEXTMEBOT_API_KEY")
    url = f"http://api.textmebot.com/send.php?recipient=+62{nomor}&apikey={api_key}&text={text}"
    print(url)
    try:
        requests.get(url)
        return "Success"
    except Exception as e:
        return e

def main(args):
    nomor = args.get("nomor")
    text = args.get("text")

    if not nomor or not text:
        return {"body" : {"message" : "nomor and text needed"}, "statusCode" : 401}

    response = sender(nomor, text)
    return {"body" : {"message" : response}, "statusCode" : 200}
