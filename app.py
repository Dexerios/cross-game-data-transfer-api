from flask import Flask, request, jsonify
import requests
import json
import os

app = Flask(__name__)

# ---------------------------------------------------------
# Roblox API Key (stored in Railway environment variable)
# ---------------------------------------------------------
API_KEY = os.getenv("ROBLOX_API_KEY")

OLD_UNIVERSE = 60375311
OLD_DATASTORE = "TransferTest"

NEW_UNIVERSE = 10155306460
NEW_DATASTORE = "TestStore"

# ---------------------------------------------------------
# Helper: Write to Roblox Datastore
# ---------------------------------------------------------
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
        "entryKey": entry_key,
    }

    r = requests.post(url, headers=headers, params=params, data=json.dumps(data))
    r.raise_for_status()
    return True


# ---------------------------------------------------------
# ROOT ROUTE
# ---------------------------------------------------------
@app.route("/")
def home():
    return "API is running", 200


# ---------------------------------------------------------
# UPLOAD — Roblox game sends JSON → server writes to new datastore
# ---------------------------------------------------------
@app.route("/upload", methods=["POST"])
def upload():
    try:
        payload = request.get_json(force=True)

        entry_key = payload.get("entryKey")
        data = payload.get("data")

        if not entry_key or data is None:
            return jsonify({"error": "entryKey and data required"}), 400

        roblox_write(NEW_UNIVERSE, NEW_DATASTORE, entry_key, data)

        return jsonify({"success": True}), 200

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
