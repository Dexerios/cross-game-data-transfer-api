from flask import Flask, request, jsonify
import requests
import json
import os

app = Flask(__name__)

# ---------------------------------------------------------
# Roblox API Key (stored in Railway environment variable)
# ---------------------------------------------------------
API_KEY = os.getenv("n69gqEZwK0ey6Jmr8YrOva+F1axHoUxS1E1NDn392yyfsmMVZXlKaGJHY2lPaUpTVXpJMU5pSXNJbXRwWkNJNkluTnBaeTB5TURJeExUQTNMVEV6VkRFNE9qVXhPalE1V2lJc0luUjVjQ0k2SWtwWFZDSjkuZXlKaGRXUWlPaUpTYjJKc2IzaEpiblJsY201aGJDSXNJbWx6Y3lJNklrTnNiM1ZrUVhWMGFHVnVkR2xqWVhScGIyNVRaWEoyYVdObElpd2lZbUZ6WlVGd2FVdGxlU0k2SW00Mk9XZHhSVnAzU3pCbGVUWktiWEk0V1hKUGRtRXJSakZoZUVodlZYaFRNVVV4VGtSdU16a3llWGxtYzIxTlZpSXNJbTkzYm1WeVNXUWlPaUl4TURFNU1EQXlNQ0lzSW1WNGNDSTZNVGMyTlRNMU16TTFNQ3dpYVdGMElqb3hOelkxTXpRNU56VXdMQ0p1WW1ZaU9qRTNOalV6TkRrM05UQjkuZmJ3M3lmWUVYNEtzdlhxUnVkR2l3ZjlDUENFNE5wMUM1T3hRejd2cTF2OHFlRVAtcG1rczFIb0RuNFpHV0pFQTFFUXlsMzFHUlRST3hZS0I5WEY2ZXdDSGVOU3BhYkgxUFVhUTk4SzJPaXZ1Uzg3ZjF1Z1VvR3JrV2E4YVJuRnRoQk9aNUsySHlDQXBBWHhKelpWdjIxME5jaWxfdmtCaFM5elhxbkJiWTlHdjVTWDRjZ2hPSVNsTkhfV2d0SlY1bTRhNkc2N21HNnRYbWRTcHgyWlU2VHVpLXczYjg4QnFjNEdLbG1LQ0RjbkZGTjExY0Z3SWpoTW5EMnVld2Fad200elZocE92UFAyaURISllvSUpkQkoxTlR0X2xrTGpuQlM1QUVQbG91b25yLXFKc0QxZmMxU0JJRTNnTFZtaUFoWjFjaHpsZ2NpazVlYll2RHhyZ3FR")  # put your key in env vars

OLD_UNIVERSE = 60375311
OLD_DATASTORE = "TransferTest"

NEW_UNIVERSE = 10155306460
NEW_DATASTORE = "TestStore"

# ---------------------------------------------------------
# Helper: Read from Roblox Datastore
# ---------------------------------------------------------
def roblox_read(universe, datastore, entry_key):
    url = f"https://apis.roblox.com/datastores/v1/universes/{universe}/standard-datastores/datastore/entries/entry"

    headers = {
        "x-api-key": API_KEY,
        "Accept": "application/json",
    }

    params = {
        "datastoreName": datastore,
        "scope": "global",
        "entryKey": entry_key,
    }

    r = requests.get(url, headers=headers, params=params)

    if r.status_code == 404:
        return None  # not found

    r.raise_for_status()
    return r.json()


# ---------------------------------------------------------
# Helper: Write to Roblox Datastore
# ---------------------------
