import threading
import requests
import os
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import json, librosa
import sounddevice as sd
import time
from serial import Serial

meu_serial = 
API_BASE = "http://127.0.0.1:5000"

mp3_path = None
json_path = None

def ler_serial_gui():
  while True:
    if meu_serial != None:
      texto_recebido = meu_serial.readline().decode().strip()
      if texto_recebido != "":
        print(texto_recebido)
    time.sleep(0.1)

def carregar_eventos(json_path: str):
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    # converte cada dict num tuple, garantindo float/int puros
    events = [
        (float(ev['time']),
         ev['type'],
         int(ev['value']) if ev['type']=='energy' else float(ev['value']))
        for ev in data
    ]
    return events


def reproduzir_com_eventos(arquivo_mp3: str, events):
    print("RODOU")
    # carrega e toca
    y, sr = librosa.load(arquivo_mp3, sr=None)
    sd.play(y, sr)
    start = time.time()

    timers = []
    for t_event, kind, val in events:
        delay = start + t_event - time.time() 

        # callback captura valores atuais por default args
        def handler(kind=kind, val=val, t_event=t_event):
            if kind == 'beat':
                print(f"batida: {val}")
                meu_serial.write("batida\n".encode("UTF-8"))
            else:
                print(f"[{t_event:6.3f}s] Energia: {val}")
                meu_serial.write(f"energia:{val}\n".encode("UTF-8"))
                if (val > 50):
                    meu_serial.write("voz true\n".encode("UTF-8"))
                    
                else:
                    meu_serial.write("voz false\n".encode("UTF-8"))

        timer = threading.Timer(delay, handler)
        timer.daemon = True
        timer.start()
        timers.append(timer)

    sd.wait()
    for t in timers:
        t.join()
    
    
def tocar_musica_existente(folder: str):
#     messagebox.showinfo(
#         "Info", f"Tocando música de:\n{path}\nEventos JSON:\n{json_path}"
#     )
    mp3_path  = os.path.join(folder, "musica_recebida.mp3")
    json_path = os.path.join(folder, "eventos.json")
    events = carregar_eventos(json_path)
    reproduzir_com_eventos(mp3_path, events)


def processar_musica(prompt: str):
    try:
        url = f"{API_BASE}/generate"
        params = {'prompt': prompt}
        resp = requests.get(url, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        messagebox.showinfo("Gerar Música", f"Geração iniciada!\n{data}")
    except Exception as e:
        messagebox.showerror("Erro", f"Falha ao chamar /generate:\n{e}")


def escolher_pasta_processada():
    global mp3_path, json_path
    folder = filedialog.askdirectory(
        title="Selecione a pasta com música e eventos"
    )
    if not folder:
        return  # Usuário cancelou

    candidate_mp3 = os.path.join(folder, "musica_recebida.mp3")
    candidate_json = os.path.join(folder, "eventos.json")

    if not os.path.isfile(candidate_mp3):
        messagebox.showerror(
            "Erro",
            f"Arquivo não encontrado: {candidate_mp3}"
        )
        return
    if not os.path.isfile(candidate_json):
        messagebox.showerror(
            "Erro",
            f"Arquivo não encontrado: {candidate_json}"
        )
        return

    mp3_path = candidate_mp3
    json_path = candidate_json

    # Call your playback or analysis logic
    tocar_musica_existente(folder)


def nova_musica_interface():
    top = tk.Toplevel(root_main)
    top.title("Gerar Nova Música")
    top.geometry("400x150")
    top.resizable(False, False)

    tk.Label(top, text="Digite o prompt para geração de música:").pack(pady=(10,5))
    entry = tk.Entry(top, width=50)
    entry.pack(pady=(0,10))
    entry.focus_set()

    def on_submit():
        prompt = entry.get().strip()
        if not prompt:
            messagebox.showwarning("Aviso", "O prompt não può ficar vazio.")
            return
        top.destroy()
        processar_musica(prompt)

    btn = tk.Button(top, text="Gerar", command=on_submit, width=15)
    btn.pack()


def criar_interface_principal():
    global root_main
    root_main = tk.Tk()
    root_main.title("Separador e Analisador de Áudio")
    root_main.geometry("360x180")
    root_main.resizable(False, False)

    tk.Label(root_main, text="Selecione uma opção abaixo:").pack(pady=(10, 5))

    tk.Button(
        root_main,
        text="Tocar música já processada",
        command=escolher_pasta_processada,
        width=30, height=2
    ).pack(pady=(5, 2))

    tk.Button(
        root_main,
        text="Processar nova música",
        command=nova_musica_interface,
        width=30, height=2
    ).pack(pady=(2, 5))

    root_main.mainloop()
        
        
if __name__ == '__main__':
    if meu_serial:
        thread = threading.Thread(target=meu_serial)
        thread.daemon = True
        thread.start()
    criar_interface_principal()
