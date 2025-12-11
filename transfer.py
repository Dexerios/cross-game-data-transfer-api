import requests
import json

API_KEY = "n69gqEZwK0ey6Jmr8YrOva+F1axHoUxS1E1NDn392yyfsmMVZXlKaGJHY2lPaUpTVXpJMU5pSXNJbXRwWkNJNkluTnBaeTB5TURJeExUQTNMVEV6VkRFNE9qVXhPalE1V2lJc0luUjVjQ0k2SWtwWFZDSjkuZXlKaGRXUWlPaUpTYjJKc2IzaEpiblJsY201aGJDSXNJbWx6Y3lJNklrTnNiM1ZrUVhWMGFHVnVkR2xqWVhScGIyNVRaWEoyYVdObElpd2lZbUZ6WlVGd2FVdGxlU0k2SW00Mk9XZHhSVnAzU3pCbGVUWktiWEk0V1hKUGRtRXJSakZoZUVodlZYaFRNVVV4VGtSdU16a3llWGxtYzIxTlZpSXNJbTkzYm1WeVNXUWlPaUl4TURFNU1EQXlNQ0lzSW1WNGNDSTZNVGMyTlRNMU16TTFNQ3dpYVdGMElqb3hOelkxTXpRNU56VXdMQ0p1WW1ZaU9qRTNOalV6TkRrM05UQjkuZmJ3M3lmWUVYNEtzdlhxUnVkR2l3ZjlDUENFNE5wMUM1T3hRejd2cTF2OHFlRVAtcG1rczFIb0RuNFpHV0pFQTFFUXlsMzFHUlRST3hZS0I5WEY2ZXdDSGVOU3BhYkgxUFVhUTk4SzJPaXZ1Uzg3ZjF1Z1VvR3JrV2E4YVJuRnRoQk9aNUsySHlDQXBBWHhKelpWdjIxME5jaWxfdmtCaFM5elhxbkJiWTlHdjVTWDRjZ2hPSVNsTkhfV2d0SlY1bTRhNkc2N21HNnRYbWRTcHgyWlU2VHVpLXczYjg4QnFjNEdLbG1LQ0RjbkZGTjExY0Z3SWpoTW5EMnVld2Fad200elZocE92UFAyaURISllvSUpkQkoxTlR0X2xrTGpuQlM1QUVQbG91b25yLXFKc0QxZmMxU0JJRTNnTFZtaUFoWjFjaHpsZ2NpazVlYll2RHhyZ3FR"

# Replace these
OLD_UNIVERSE_ID = 60375311
NEW_UNIVERSE_ID = 10155306460

OLD_DATASTORE = "TransferTest"
NEW_DATASTORE = "TestStore"

ENTRY_KEY = "Player_10190020"  # OR Player_1 if testing manually


def roblox_read(universe, datastore, key):
    url = f"https://apis.roblox.com/datastores/v1/universes/{universe}/standard-datastores/datastore/entries/entry"
    
    headers = {
        "x-api-key": API_KEY,
        "Accept": "application/json"
    }

    params = {
        "datastoreName": datastore,
        "scope": "global",
        "entryKey": key
    }

    response = requests.get(url, headers=headers, params=params)

    print("READ STATUS:", response.status_code)

    if response.status_code == 404:
        print("❌ No entry found.")
        return None

    response.raise_for_status()
    return response.json()


def roblox_write(universe, datastore, key, value_dict):
    url = f"https://apis.roblox.com/datastores/v1/universes/{universe}/standard-datastores/datastore/entries/entry"
    
    headers = {
        "x-api-key": API_KEY,
        "Content-Type": "application/json"
    }

    params = {
        "datastoreName": datastore,
        "scope": "global",
        "entryKey": key
    }

    response = requests.post(url, headers=headers, params=params, data=json.dumps(value_dict))

    print("WRITE STATUS:", response.status_code)
    print("WRITE BODY:", response.text)

    response.raise_for_status()


if __name__ == "__main__":
    print("📥 Reading old datastore...")
    old_data = roblox_read(OLD_UNIVERSE_ID, OLD_DATASTORE, ENTRY_KEY)

    if old_data is None:
        print("⚠️ Nothing to transfer.")
    else:
        print("📤 Writing to new datastore...")
        roblox_write(NEW_UNIVERSE_ID, NEW_DATASTORE, ENTRY_KEY, old_data)
        print("✅ Transfer complete.")
