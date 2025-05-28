import requests
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("IMGBB_API_KEY")

def upload_to_imgbb(image_path, api_key=api_key):
    url = "https://api.imgbb.com/1/upload"
    with open(image_path, "rb") as file:
        payload = {
            "key": api_key,
            "image": file.read()
        }
    response = requests.post(url, files=payload)
    data = response.json()
    if data["success"]:
        return data["data"]["url"]
    else:
        raise Exception("Upload failed: " + data["error"]["message"])
