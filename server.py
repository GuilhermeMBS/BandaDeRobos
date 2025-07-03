import json
import requests
from flask import Flask, request, jsonify
from datetime import datetime

API_KEY = ""
API_URL = "https://apibox.erweima.ai/api/v1/generate"
PORT = 5000

timeline = []

# task: "47fea2f7b99b56574f375e9a41053284:
# id da música: "45de5fc3-6e30-4336-8aad-ed5d8b6fe704"

app = Flask(__name__)
callback_response = {}

CALLBACK_URL = "https://32b2-139-82-11-26.ngrok-free.app/callback"


@app.route("/generate", methods=["GET"])
def generate():
    prompt = request.args.get("prompt", "Music about programming")

    payload = {
        "prompt": prompt,
        "customMode": False,
        "instrumental": False,
        "model": "V3_5",
        "callBackUrl": CALLBACK_URL
    }

    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {API_KEY}'
    }

    try:
        response = requests.post(API_URL, headers=headers, data=json.dumps(payload))
        response.raise_for_status()
        return jsonify({"status": "generation started", "details": response.json()})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/callback", methods=["GET", "POST"])
def callback():
    data = request.get_json()
    print("Received callback data:")
    print(json.dumps(data, indent=2))
    global callback_response
    callback_response = data
    return jsonify({"status": "received"}), 200


@app.route("/lyrics", methods=["GET", "POST"])
def lyrics():
    #if not callback_response:
    #    return jsonify({"error": "No callback data yet"}), 400

    #try:
    # task_id = callback_response.get("task_id")
    # audio_id = callback_response.get("audio_url", "").split("/")[-1].split(".")[0]
    task_id = "47fea2f7b99b56574f375e9a41053284"
    audio_id = "45de5fc3-6e30-4336-8aad-ed5d8b6fe704"

    if not task_id or not audio_id:
        return jsonify({"error": "Missing taskId or audioId"}), 400

    payload = json.dumps({
        "taskId": task_id,
        "audioId": audio_id,
        "musicIndex": 0
    })
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {API_KEY}'
    }
    response = requests.post(
        "https://apibox.erweima.ai/api/v1/generate/get-timestamped-lyrics",
        headers=headers,
        data=payload
    )
    
    data = response.json()
    # aligned = data.get("data", {}).get("alignedWords", [])
    
    try:
        aligned = data["data"]["alignedWords"]
    except KeyError:
        return jsonify({"error": "Malformed response from API"}), 500

    verse = ""
    verse_time = 0
    ok = False
    
    for entry in aligned:
        word = entry["word"]
        start = entry["startS"]
        end = entry["endS"]
        if word[0] == "[":
            verse_time = start
            ok = False
            for (index, letter) in enumerate(word):
                if letter == "]":
                    verse = word[index+2:]
                    break
        elif "\n" in word:
            verse += word.rstrip("\n")
            timeline.append({"start": verse_time, "verse": verse})
            verse = ""
            ok = True
        else:
            if ok:
                verse_time = start
                ok = False
            verse += word
    
    #response.raise_for_status()
    #print(response.text)
    return jsonify(response.json())

    #except Exception as e:
        #return jsonify({"error": str(e)}), 500


@app.route("/result", methods=["GET"])
def result():
    if callback_response:
        return jsonify(callback_response)
    return jsonify({"status": "waiting for callback"}), 202


if __name__ == "__main__":
    app.run(port=PORT)
