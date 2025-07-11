import os
from serial import Serial
import time
import threading
import tkinter as tk
from tkinter import filedialog, messagebox
from spleeter.separator import Separator
import librosa
import numpy as np
import sounddevice as sd
import json
from datetime import datetime
import gui
import unicodedata


# Função que monitora a pasta da música e envia ao LCD via serial
def monitor_lcd(pasta: str, meu_serial):
    timeline_path = os.path.join(pasta, "timeline.json")
    # aguarda até que o timeline.json apareça
    while not os.path.exists(timeline_path):
        time.sleep(1)
    # carrega a timeline
    with open(timeline_path, "r", encoding="utf-8") as f:
        timeline = json.load(f)
    # envia cada verso no tempo correto
    start_time = datetime.now()
    
    for entry in timeline:
        #print("OIIII")
        target = entry["start"]
        verse  = entry["verse"]
        verse = unicodedata.normalize('NFD', verse).encode('ASCII', 'ignore').decode('ASCII')
        while (datetime.now() - start_time).total_seconds() < target:
            #print((datetime.now() - start_time).total_seconds())
            time.sleep(0.01)
        try:
            meu_serial.write((verse + "\n").encode("UTF-8"))
        except:
            pass
        print("VERSO", verse)
        
        
def ler_serial():
  while True:
    if meu_serial != None:
      texto_recebido = meu_serial.readline().decode().strip()
      if texto_recebido != "":
        print("Recebido do Arduino:", texto_recebido)
    time.sleep(0.1)


def separar_stems(arquivo_entrada: str, pasta_saida: str,
                  modelo: str = 'spleeter:5stems'):
    separator = Separator(modelo)
    separator.separate_to_file(arquivo_entrada, pasta_saida)


def extrair_batidas_drums(caminho_drums: str):
    y, sr = librosa.load(caminho_drums, sr=None)
    _, frames = librosa.beat.beat_track(y=y, sr=sr)
    return librosa.frames_to_time(frames, sr=sr)

def calcular_energias(y: np.ndarray, sr: int, frame_ms: int):
    frame_len = max(1, int(sr * frame_ms / 1000)) 
    num_frames = int(np.ceil(len(y) / frame_len))
    energies = np.zeros(num_frames, dtype=float)
    for i in range(num_frames):
        start = i * frame_len
        end = min(start + frame_len, len(y))
        frame = y[start:end]
        energies[i] = np.sqrt(np.mean(frame**2)) if frame.size else 0.0
    e_min, e_max = energies.min(), energies.max()
    if e_max > e_min:
        energies = ((energies - e_min) / (e_max - e_min) * 100).astype(int)
    else:
        energies = np.zeros_like(energies, dtype=int)
    return energies


def extrair_energias_vocals(caminho_vocals: str, frame_ms: int):
    y, sr = librosa.load(caminho_vocals, sr=None, mono=True)
    return calcular_energias(y, sr, frame_ms)

def extrair_energias_other(caminho_other: str, frame_ms: int):
    y, sr = librosa.load(caminho_other, sr=None, mono=True)
    return calcular_energias(y, sr, frame_ms)

def reproduzir_completo(arquivo_original: str, beat_times, energies,energies_other, frame_ms: int):
    # Carrega o áudio
    y, sr = librosa.load(arquivo_original, sr=None)

    # Monta lista de eventos (tempo, tipo, valor)
    events = []
    for bt in beat_times:
        events.append((bt, 'beat', bt))
    for idx, e in enumerate(energies):
        t = idx * frame_ms / 1000.0
        events.append((t, 'energy', e))
    for idx, e in enumerate((energies_other)):
        t = idx * frame_ms / 1000.0
        events.append((t, 'other', e))
    events.sort(key=lambda ev: ev[0])

    # Inicia a reprodução
    sd.play(y, sr)
    start = time.time()

    # Agenda um timer para cada evento, sem usar sleep
    timers = []
    for t_event, kind, val in events:
        delay = start + t_event - time.time() #quase o que a gente fazia com a millis no arduino
#         if delay < 0:
#             # já passou do tempo, imprime imediatamente
#             if kind == 'beat':
#                 print(f"batida: {val}")
#             else:
#                 print(f"[{t_event:6.3f}s] Energia: {val}")
#             continue

        # callback captura valores atuais por default args
        def handler(kind=kind, val=val, t_event=t_event):
            try:
                if kind == 'beat':
                    print(f"batida: {val}")
                    meu_serial.write("$batida\n".encode("UTF-8"))
                elif kind == 'other':
                    if (val > 60):
                        meu_serial.write(f"$acorde\n".encode("UTF-8"))
                else:
                    print(f"[{t_event:6.3f}s] Energia: {val}")
                    meu_serial.write(f"$energia:{val}\n".encode("UTF-8"))
                    if (val > 50):
                        meu_serial.write("$voz true\n".encode("UTF-8"))
                    else:
                        meu_serial.write("$voz false\n".encode("UTF-8"))
            except:
                pass
                    

        #tentar colocar um timer único ao invés de um timer para cada instante
        timer = threading.Timer(delay, handler)
        timer.daemon = True
        timer.start()
        timers.append(timer)
        
    # Aguarda fim do áudio
    sd.wait()
    #os.remove("musica_recebida.mp3")
    # Garante que todos os timers terminem
    for timer in timers:
        timer.join()
    return events

    

# Função que aguarda o placeholder, processa tudo e dispara o monitor_lcd
def escolher_arquivo_novo():
    # 1) espera o placeholder
    while not os.path.exists("nome_placeholder.txt"):
        time.sleep(1)

    # 2) lê e remove o placeholder
    with open("nome_placeholder.txt", "r") as f:
        pasta = f.read().strip()
    try:
        os.remove("nome_placeholder.txt")
    except OSError:
        print("[WARN] não foi possível remover nome_placeholder.txt")

    # 3) valida a pasta
    if not os.path.isdir(pasta):
        messagebox.showerror("Erro", f"Pasta '{pasta}' não existe.")
        return

    # 4) inicia o monitor do LCD


    # 5) processa stems, extrai batidas/energias e reproduz
    mp3_path = os.path.join(pasta, "musica_recebida.mp3")
    if not os.path.isfile(mp3_path):
        messagebox.showerror("Erro", f"Arquivo '{mp3_path}' não encontrado.")
        return

    output_dir = os.path.join(pasta, "Faixas")
    os.makedirs(output_dir, exist_ok=True)
    frame_ms = 750
    
    proc = tk.Toplevel(gui.root_main)
    proc.title("Processando")
    proc.geometry("250x80")
    proc.resizable(False, False)
    tk.Label(proc, text="Processando, aguarde...").pack(expand=True, pady=20)
    proc.update()

    try:
        separar_stems(mp3_path, output_dir)
        base        = os.path.splitext(os.path.basename(mp3_path))[0]
        drums_path  = os.path.join(output_dir, base, 'drums.wav')
        vocals_path = os.path.join(output_dir, base, 'vocals.wav')
        other_path	= os.path.join(output_dir, base, 'other.wav')
        beat_times  = extrair_batidas_drums(drums_path)
        energies    = extrair_energias_vocals(vocals_path, frame_ms)
        energies_other	= extrair_energias_other(other_path, frame_ms)
    except Exception as e:
        proc.destroy()
        messagebox.showerror("Erro", f"Ocorreu um erro:\n{e}")
        return

    proc.destroy()
    messagebox.showinfo(
        "Concluído",
        f"Stems separados, {len(beat_times)} batidas extraídas e {len(energies)} janelas de energia calculadas."
    )

    events = reproduzir_completo(mp3_path, beat_times, energies,energies_other, frame_ms)

    # 6) salva eventos em JSON
    event_dicts = [
        {"time": float(t), "type": kind, "value": int(val) if kind=="energy" else float(val)}
        for t, kind, val in events
    ]
    json_path = os.path.join(pasta, "eventos.json")
    with open(json_path, "w", encoding="utf-8") as jf:
        json.dump(event_dicts, jf, ensure_ascii=False, indent=2)

    print("fim")

    
def reproduzir_com_eventos(folder, arquivo_mp3: str, events, meu_serial):
    print("RODOU")
    # carrega e toca
    y, sr = librosa.load(arquivo_mp3, sr=None)
    sd.play(y, sr)
    start = time.time()
    
    thread_lcd = threading.Thread(target=monitor_lcd, args=(folder,meu_serial))
    thread_lcd.daemon = True
    thread_lcd.start()

    timers = []
    for t_event, kind, val in events:
        delay = start + t_event - time.time() 

        # callback captura valores atuais por default args
        def handler(kind=kind, val=val, t_event=t_event):
            try:
                if kind == 'beat':
                    meu_serial.write("$batida\n".encode("UTF-8"))
                elif kind == 'other':
                    print("violao")
                    meu_serial.write(f"$acorde\n".encode("UTF-8"))
                else:
                    print(f"Energia: {val}")
                    meu_serial.write(f"$energia:{val}\n".encode("UTF-8"))
                    if (val > 50):
                        print('1')
                        meu_serial.write("$voz true\n".encode("UTF-8"))
                    else:
                        print('0')
                        meu_serial.write("$voz false\n".encode("UTF-8"))
            except:
                pass

        timer = threading.Timer(delay, handler)
        timer.daemon = True
        timer.start()
        timers.append(timer)

    sd.wait()
    for t in timers:
        t.join()
    

if __name__ == '__main__':
    # inicialização da serial
    meu_serial = Serial("COM8", baudrate=9600, timeout=0.1)
    print("[INFO] Serial: ok")

    # thread de leitura da serial
    thread_serial = threading.Thread(target=ler_serial, daemon=True)
    thread_serial.start()

    # thread que aguarda o placeholder e dispara escolher_arquivo_novo()
    thread_placeholder = threading.Thread(target=escolher_arquivo_novo, daemon=True)
    thread_placeholder.start()

    # inicia a GUI
    gui.criar_interface_principal(meu_serial)
