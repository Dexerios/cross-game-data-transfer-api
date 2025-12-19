import os
import logging
import requests
from flask import Flask, request, jsonify

# ===============================
# App Setup
# ===============================

logging.basicConfig(level=logging.INFO)
app = Flask(__name__)

# ===============================
# CONFIG
# ===============================

ROBLOX_API_KEY = os.environ.get("ROBLOX_API_KEY")
UNIVERSE_ID = 3064619271
DATASTORE_NAME = "TransferStore"

if not ROBLOX_API_KEY:
    raise RuntimeError("ROBLOX_API_KEY environment variable is required")

ROBLOX_DATASTORE_URL = (
    f"https://apis.roblox.com/datastores/v1/universes/"
    f"{UNIVERSE_ID}/standard-datastores/datastore/entries/entry"
)

HEADERS = {
    "x-api-key": ROBLOX_API_KEY,
    "Content-Type": "application/json",
    "Accept": "application/json",
}

# ===============================
# Roblox Datastore Write
# ===============================

def write_to_datastore(entry_key: str, data: dict) -> None:
    params = {
        "datastoreName": DATASTORE_NAME,
        "scope": "global",
        "entryKey": entry_key,
    }

    response = requests.put(
        ROBLOX_DATASTORE_URL,
        headers=HEADERS,
        params=params,
        json=data,          # <-- correct way
        timeout=15,
    )

    if not response.ok:
        logging.error("Roblox API error %s: %s", response.status_code, response.text)
        response.raise_for_status()

# ===============================
# Health Check
# ===============================

@app.route("/", methods=["GET"])
def health_check():
    return jsonify({"status": "ok"}), 200

# ===============================
# Receive Data from Old Game
# ===============================

@app.route("/upload", methods=["POST"])
def upload():
    try:
        payload = request.get_json(silent=True)

        if not payload:
            return jsonify({
                "success": False,
                "error": "Invalid or missing JSON body"
            }), 400

        entry_key = payload.get("entryKey")
        data = payload.get("data")

        if not isinstance(entry_key, str) or data is None:
            return jsonify({
                "success": False,
                "error": "entryKey (string) and data are required"
            }), 400

        write_to_datastore(entry_key, data)

        return jsonify({
            "success": True,
            "writtenKey": entry_key
        }), 200

    except requests.HTTPError as e:
        return jsonify({
            "success": False,
            "error": "Roblox datastore write failed",
            "details": str(e)
        }), 502

    except Exception as e:
        logging.exception("Unhandled server error")
        return jsonify({
            "success": False,
            "error": "Internal server error"
        }), 500
