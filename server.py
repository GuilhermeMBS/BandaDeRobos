import requests, os, json, re
from flask import Flask, request, jsonify

API_KEY = ""
API_URL = "https://apibox.erweima.ai/api/v1/generate"
PORT = 5000

timeline = []
callback_response = {}
CALLBACK_URL = "https://9ed0-139-82-11-26.ngrok-free.app/callback"

app = Flask(__name__)

def sanitize_name(name: str) -> str:
    return re.sub(r'[^\w\-\s]', '', name).strip()

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
    global callback_response

    try:
        data = request.get_json()
        callback_response = data
        with open("callback.json", "w") as f:
            json.dump(data, f, indent=2)
    except Exception:
        try:
            with open("callback.json", "r") as f:
                data = json.load(f)
                callback_response = data
        except Exception as e2:
            return jsonify({"error": "Failed to read saved callback", "details": str(e2)}), 500

    title = data.get("title") or data.get("data", {}).get("title")
    if not title:
        return jsonify({"error": "No title found in callback data"}), 400

    safe_title = sanitize_name(title)

    audio_entries = data.get("data", {}).get("data", [])
    if not audio_entries:
        return jsonify({"error": "No audio entries found"}), 400

    first_entry = audio_entries[0]
    audio_url = first_entry.get("stream_audio_url")
    if not audio_url:
        return jsonify({"error": "No audio URL in the first entry"}), 400

    folder_path = os.path.join(os.getcwd(), safe_title)
    os.makedirs(folder_path, exist_ok=True)

    try:
        resp = requests.get(audio_url)
        resp.raise_for_status()
        if "audio" not in resp.headers.get("Content-Type", ""):
            raise ValueError(f"Not an audio stream: {resp.headers.get('Content-Type')}")

        mp3_path = os.path.join(folder_path, "Musica.mp3")
        with open(mp3_path, "wb") as f:
            f.write(resp.content)

    except Exception as e:
        return jsonify({"status": "callback saved", "warning": "Audio not downloaded", "error": str(e)}), 206

    txt_filename = f"{safe_title}.txt"
    with open(txt_filename, "w", encoding="utf-8") as txtf:
        txtf.write(title)

    return jsonify({
        "status": "received and audio saved",
        "folder": safe_title,
        "mp3_path": mp3_path,
        "txt_file": txt_filename
    }), 200

@app.route("/lyrics", methods=["GET", "POST"])
def lyrics():
    if not callback_response:
        return jsonify({"error": "No callback data yet"}), 400

    task_id = callback_response.get("task_id")
    audio_id = callback_response.get("audio_url", "").split("/")[-1].split(".")[0]

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

    try:
        data = response.json()
        aligned = data["data"]["alignedWords"]
    except Exception:
        return jsonify({"error": "Malformed response from API"}), 500

    verse = ""
    verse_time = 0
    ok = False

    for entry in aligned:
        word = entry["word"]
        start = entry["startS"]
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

    return jsonify(data)

@app.route("/result", methods=["GET"])
def result():
    if callback_response:
        return jsonify(callback_response)
    return jsonify({"status": "waiting for callback"}), 202

if __name__ == "__main__":
    app.run(port=PORT, threaded=True)
