import json
from os import getenv

from github import Github
from pyrebase import pyrebase
import requests

FIREBASE_CONFIG: dict = json.loads(Github(
    getenv("ACCESS_TOKEN")
).get_gist("37bbbbce6b64b2f4a5d3195d7d06df92").files["firebase_config.json"].content)

FIREBASE = pyrebase.initialize_app(FIREBASE_CONFIG)

DATABASE = FIREBASE.database()
STORAGE = FIREBASE.storage()


def request_file(filename):

    url = STORAGE.get_url("").split("/")
    url[6] = f"o/{filename}"

    url = [urlpart + "/" for urlpart in url]

    url[-1] = url[-1].replace("/", "")
    url[6] = url[6][:-1]

    url = "".join(url)

    file_text = requests.get(url).text

    return file_text
