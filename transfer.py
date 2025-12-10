import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# TODO: put your real key here (the same one you're already using)
API_KEY = "n69gqEZwK0ey6Jmr8YrOva+F1axHoUxS1E1NDn392yyfsmMVZXlKaGJHY2lPaUpTVXpJMU5pSXNJbXRwWkNJNkluTnBaeTB5TURJeExUQTNMVEV6VkRFNE9qVXhPalE1V2lJc0luUjVjQ0k2SWtwWFZDSjkuZXlKaGRXUWlPaUpTYjJKc2IzaEpiblJsY201aGJDSXNJbWx6Y3lJNklrTnNiM1ZrUVhWMGFHVnVkR2xqWVhScGIyNVRaWEoyYVdObElpd2lZbUZ6WlVGd2FVdGxlU0k2SW00Mk9XZHhSVnAzU3pCbGVUWktiWEk0V1hKUGRtRXJSakZoZUVodlZYaFRNVVV4VGtSdU16a3llWGxtYzIxTlZpSXNJbTkzYm1WeVNXUWlPaUl4TURFNU1EQXlNQ0lzSW1WNGNDSTZNVGMyTlRNMU16TTFNQ3dpYVdGMElqb3hOelkxTXpRNU56VXdMQ0p1WW1ZaU9qRTNOalV6TkRrM05UQjkuZmJ3M3lmWUVYNEtzdlhxUnVkR2l3ZjlDUENFNE5wMUM1T3hRejd2cTF2OHFlRVAtcG1rczFIb0RuNFpHV0pFQTFFUXlsMzFHUlRST3hZS0I5WEY2ZXdDSGVOU3BhYkgxUFVhUTk4SzJPaXZ1Uzg3ZjF1Z1VvR3JrV2E4YVJuRnRoQk9aNUsySHlDQXBBWHhKelpWdjIxME5jaWxfdmtCaFM5elhxbkJiWTlHdjVTWDRjZ2hPSVNsTkhfV2d0SlY1bTRhNkc2N21HNnRYbWRTcHgyWlU2VHVpLXczYjg4QnFjNEdLbG1LQ0RjbkZGTjExY0Z3SWpoTW5EMnVld2Fad200elZocE92UFAyaURISllvSUpkQkoxTlR0X2xrTGpuQlM1QUVQbG91b25yLXFKc0QxZmMxU0JJRTNnTFZtaUFoWjFjaHpsZ2NpazVlYll2RHhyZ3FR"

WORD_AREA_UNIVERSE = 60375311   # source universe
DATASTORE = "TransferTest"      # name of the datastore in Word Arena


@app.route("/")
def health():
    return "OK", 200


@app.route("/word-area-data")
def word_area_data():
    # Roblox will pass userId as a query param
    user_id = request.args.get("userId")
    if not user_id:
        return jsonify({"error": "missing userId"}), 400

    url = (
        f"https://apis.roblox.com/datastores/v1/universes/"
        f"{WORD_AREA_UNIVERSE}/standard-datastores/datastore/entries/entry"
    )

    headers = {
        "x-api-key": API_KEY,
        "Accept": "application/json",
    }

    params = {
        "datastoreName": DATASTORE,
        "scope": "global",
        "entryKey": f"Player_{user_id}",
    }

    r = requests.get(url, headers=headers, params=params)

    if r.status_code == 404:
        # Player has no data in the old game
        return jsonify({"exists": False}), 200

    r.raise_for_status()

    # whatever is stored in the datastore (string / json)
    try:
        data = r.json()
    except Exception:
        data = r.text

    return jsonify({"exists": True, "data": data}), 200


if __name__ == "__main__":
    # Railway sets PORT in an env var – fall back to 3000 for local testing
    port = int(os.environ.get("PORT", 3000))
    app.run(host="0.0.0.0", port=port)
