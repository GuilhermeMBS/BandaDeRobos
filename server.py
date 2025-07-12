# server.py
import os
import re
import json
import requests
from flask import Flask, request, jsonify

API_KEY      = "<INSERT API KEY>"
API_URL      = "https://apibox.erweima.ai/api/v1/generate"
LYRICS_URL   = "https://apibox.erweima.ai/api/v1/generate/get-timestamped-lyrics"
CALLBACK_URL = "<NGROK SERVER>/callback"

app = Flask(__name__)
callback_response = None

def sanitize_name(name: str) -> str:
    return re.sub(r'[^\w\-\s]', '', name).strip()

def gera_timeline(callback_data: dict, folder_path: str) -> list:
    first     = callback_data["data"]["data"][0]
    # agora pega o task_id de dentro de "data"
    task_id   = callback_data.get("data", {}).get("task_id")
    audio_url = first.get("stream_audio_url", "")
    audio_id  = first.get("audio_id") or first.get("id") or audio_url.split("/")[-1].split(".")[0]

    if not task_id or not audio_id:
        raise ValueError(f"Missing task_id or audio_id (task_id={task_id!r}, audio_id={audio_id!r})")

    # 1) chama a API de timestamped lyrics
    payload = {"taskId": task_id, "audioId": audio_id, "musicIndex": 0}
    headers = {
        "Content-Type":  "application/json",
        "Accept":        "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }
    resp = requests.post(LYRICS_URL, headers=headers, json=payload, timeout=30)
    resp.raise_for_status()
    data_lyrics = resp.json()

    # 2) extrai alignedWords
    aligned = data_lyrics.get("data", {}).get("alignedWords", [])
    timeline = []
    verse      = ""
    verse_time = 0
    ok         = False

    for entry in aligned:
        w     = entry.get("word", "")
        start = entry.get("startS", 0)
        if w.startswith("["):
            verse_time = start
            ok         = False
            verse      = w.split("] ", 1)[-1]
        elif "\n" in w:
            verse += w.strip("\n")
            timeline.append({"start": verse_time, "verse": verse})
            verse = ""
            ok    = True
        else:
            if ok:
                verse_time = start
                ok         = False
            verse += w

    # 3) grava timeline.json
    timeline_path = os.path.join(folder_path, "timeline.json")
    with open(timeline_path, "w", encoding="utf-8") as tf:
        json.dump(timeline, tf, ensure_ascii=False, indent=2)

    return timeline

@app.route("/generate", methods=["GET"])
def generate():
    prompt = request.args.get("prompt", "Music about programming")
    payload = {
        "prompt":       prompt,
        "customMode":   False,
        "instrumental": False,
        "model":        "V3_5",
        "callBackUrl":  CALLBACK_URL
    }
    headers = {
        "Content-Type":  "application/json",
        "Accept":        "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }
    try:
        resp = requests.post(API_URL, headers=headers, json=payload, timeout=15)
        resp.raise_for_status()
        return jsonify({"status": "generation started", "details": resp.json()})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/callback", methods=["POST"])
def callback():
    global callback_response
    data = request.get_json()
    callback_response = data

    # cria pasta a partir do title
    first       = data["data"]["data"][0]
    title       = first.get("title", "untitled")
    safe_title  = sanitize_name(title)
    folder_path = os.path.join(os.getcwd(), safe_title)
    os.makedirs(folder_path, exist_ok=True)

    # baixa o MP3
    audio_url   = first.get("stream_audio_url")
    resp_audio  = requests.get(audio_url, timeout=30)
    resp_audio.raise_for_status()
    mp3_path    = os.path.join(folder_path, "musica_recebida.mp3")
    with open(mp3_path, "wb") as f:
        f.write(resp_audio.content)

    # salva callback.json
    callback_path = os.path.join(folder_path, "callback.json")
    with open(callback_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    # gera timeline.json imediatamente
    try:
        timeline = gera_timeline(data, folder_path)
    except Exception as e:
        print(f"[WARN] falha ao gerar timeline.json: {e}")
        timeline = []

    # emite placeholder para o cliente
    placeholder = "nome_placeholder.txt"
    with open(placeholder, "w", encoding="utf-8") as txtf:
        txtf.write(safe_title + "\n")

    return jsonify({
        "status":         "callback handled",
        "folder":         safe_title,
        "mp3_path":       mp3_path,
        "callback_file":  callback_path,
        "timeline_count": len(timeline)
    }), 200

@app.route("/result", methods=["GET"])
def result():
    if callback_response:
        return jsonify(callback_response)
    return jsonify({"status": "waiting for callback"}), 202

if __name__ == "__main__":
    app.run(port=5000, threaded=True)
