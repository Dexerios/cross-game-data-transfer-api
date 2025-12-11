import os
import json
import logging
import requests
from flask import Flask, request, jsonify

# Enable full debug logging
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)

# ---------------------------------------
# Load Roblox API Key from Railway env vars
# ---------------------------------------
API_KEY = os.getenv("ROBLOX_API_KEY")
print("Loaded API KEY:", API_KEY)
OLD_UNIVERSE = 60375311
OLD_DATASTORE = "TransferTest"

NEW_UNIVERSE = 3727159513
NEW_DATASTORE = "TestStore"

# ---------------------------------------
# Helper: Write to Roblox Datastore
# ---------------------------------------
def roblox_write(universe, datastore, entry_key, data):
    url = f"https://apis.roblox.com/datastores/v1/universes/{universe}/standard-datastores/datastore/entries/entry"

    headers = {
        "x-api-key": API_KEY,
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    params = {
        "datastoreName": datastore,
        "scope": "global",
        "entryKey": entry_key
    }

    # Log what we are about to send
    print("Writing to Roblox DS:", universe, datastore, entry_key, data)

    response = requests.post(url, headers=headers, params=params, data=json.dumps(data))

    print("Roblox API Response:", response.status_code, response.text)

    response.raise_for_status()
    return True


# ---------------------------------------
# Health check route
# ---------------------------------------
@app.route("/")
def home():
    return "API is running", 200


# ---------------------------------------
# UPLOAD route — Roblox sends data → server writes to NEW DS
# ---------------------------------------
@app.route("/upload", methods=["POST"])
def upload():
    try:
        payload = request.get_json(force=True)
        print("Received Payload:", payload)

        entry_key = payload.get("entryKey")
        data = payload.get("data")

        if not entry_key or data is None:
            print("UPLOAD ERROR: missing fields")
            return jsonify({"error": "entryKey and data required"}), 400

        # Write to Roblox Datastore
        roblox_write(NEW_UNIVERSE, NEW_DATASTORE, entry_key, data)

        return jsonify({"success": True}), 200

    except Exception as e:
        print("UPLOAD ERROR:", e)
        return jsonify({"success": False, "error": str(e)}), 500


# ---------------------------------------
# Optional: migrate old → new datastore
# ---------------------------------------
@app.route("/migrate")
def migrate():
    try:
        entry_key = request.args.get("entryKey")
        if not entry_key:
            return jsonify({"error": "Missing entryKey"}), 400

        # Read old datastore
        url = f"https://apis.roblox.com/datastores/v1/universes/{OLD_UNIVERSE}/standard-datastores/datastore/entries/entry"
        headers = {"x-api-key": API_KEY, "Accept": "application/json"}
        params = {
            "datastoreName": OLD_DATASTORE,
            "scope": "global",
            "entryKey": entry_key
        }

        print("Reading from OLD DS:", entry_key)
        r = requests.get(url, headers=headers, params=params)

        print("Old DS Response:", r.status_code, r.text)

        if r.status_code == 404:
            return jsonify({"success": False, "reason": "No old data found"}), 404

        r.raise_for_status()
        old_data = r.json()

        # Write to NEW datastore
        roblox_write(NEW_UNIVERSE, NEW_DATASTORE, entry_key, old_data)

        return jsonify({"success": True, "migrated": old_data}), 200

    except Exception as e:
        print("MIGRATE ERROR:", e)
        return jsonify({"success": False, "error": str(e)}), 500




