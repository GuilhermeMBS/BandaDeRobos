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

def ler_serial():
  while True:
    if meu_serial != None:
      texto_recebido = meu_serial.readline().decode().strip()
      if texto_recebido != "":
        print(texto_recebido)
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

def reproduzir_completo(arquivo_original: str, beat_times, energies, frame_ms: int):
    # Carrega o áudio
    y, sr = librosa.load(arquivo_original, sr=None)

    # Monta lista de eventos (tempo, tipo, valor)
    events = []
    for bt in beat_times:
        events.append((bt, 'beat', bt))
    for idx, e in enumerate(energies):
        t = idx * frame_ms / 1000.0
        events.append((t, 'energy', e))
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
            if kind == 'beat':
                print(f"batida: {val}")
            else:
                print(f"[{t_event:6.3f}s] Energia: {val}")

        timer = threading.Timer(delay, handler)
        timer.daemon = True
        timer.start()
        timers.append(timer)

    # Aguarda fim do áudio
    sd.wait()
    os.remove("musica_recebida.mp3")
    # Garante que todos os timers terminem
    for timer in timers:
        timer.join()
    

def escolher_arquivo():
#     mp3_path = filedialog.askopenfilename(
#         title="Selecione o arquivo MP3",
#         filetypes=[("MP3 files", "*.mp3")]
#     )
#     if not mp3_path:
#         return
    verifica = True
    while(verifica):
        print("procurando arquivo")
        mp3_path = "musica_recebida.mp3"
        if os.path.exists(mp3_path):
            verifica = False

    output_dir = "Faixa"
    frame_ms = 420

    proc = tk.Toplevel(root)
    proc.title("Processando")
    proc.geometry("250x80")
    proc.resizable(False, False)
    tk.Label(proc, text="Processando, aguarde...").pack(expand=True, pady=20)
    proc.update()

    try:
        # 1) separa stems
        separar_stems(mp3_path, output_dir)

        base = os.path.splitext(os.path.basename(mp3_path))[0]
        drums_path = os.path.join(output_dir, base, 'drums.wav')
        vocals_path = os.path.join(output_dir, base, 'vocals.wav')

        # 2) extrai batidas
        beat_times = extrair_batidas_drums(drums_path)

        # 3) extrai energias dos vocals
        energies = extrair_energias_vocals(vocals_path, frame_ms)

    except Exception as e:
        print("erro")
        proc.destroy()
        messagebox.showerror("Erro", f"Ocorreu um erro:\n{e}")
        return

    proc.destroy()
    messagebox.showinfo(
        "Concluído",
        f"Stems separados, {len(beat_times)} batidas extraídas e {len(energies)} janelas de energia calculadas."
    )

    # 4) reproduz áudio original e printa batidas + energia
    reproduzir_completo(mp3_path, beat_times, energies, frame_ms)
    print("fim")
    
    

if __name__ == '__main__':
    meu_serial = Serial("COM5", baudrate=9600, timeout=0.1)
    #meu_serial = None
    print("[INFO] Serial: ok")

    thread = threading.Thread(target=ler_serial)
    thread.daemon = True
    thread.start()

    root = tk.Tk()
    root.title("Separador e Analisador de Áudio")
    root.geometry("360x140")
    root.resizable(False, False)

    tk.Label(
        root,
        text="Selecione um MP3 para separar stems,\nextrair batidas e níveis de energia nos vocals"
    ).pack(pady=(10,5))
    tk.Button(
        root,
        text="Selecionar e Processar MP3",
        command=escolher_arquivo,
        width=30,
        height=2
    ).pack(pady=5)

    root.mainloop()




