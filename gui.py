# gui.py
import threading
import requests
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog

# === Serial-reading stub ===
meu_serial = None  # Replace/initialize your Serial here

# === Configuration ===
# Point to your local Flask server's base URL
API_BASE = "http://127.0.0.1:5000"

# === Business logic ===
def tocar_musica_existente(file_path: str):
    # Your existing logic to play processed audio from file_path
    messagebox.showinfo("Info", f"Tocando música processada de:\n{file_path}")


def processar_musica(prompt: str):
    """
    Calls the local Flask /generate endpoint with the given prompt.
    """
    try:
        url = f"{API_BASE}/generate"
        params = {'prompt': prompt}
        resp = requests.get(url, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        messagebox.showinfo("Gerar Música", f"Geração iniciada!\n{data}")
    except Exception as e:
        messagebox.showerror("Erro", f"Falha ao chamar /generate:\n{e}")

# === GUI Functions ===

def escolher_arquivo():
    filetypes = [("MP3 files", "*.mp3"), ("All files", "*")]
    path = filedialog.askopenfilename(
        title="Selecione o arquivo de música processada",
        filetypes=filetypes
    )
    if path:
        tocar_musica_existente(path)


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
            messagebox.showwarning("Aviso", "O prompt não pode ficar vazio.")
            return
        top.destroy()
        processar_musica(prompt)

    btn = tk.Button(top, text="Gerar", command=on_submit, width=15)
    btn.pack()

# === Main window setup ===

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
        command=escolher_arquivo,
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
    # Start serial-read thread if needed
    if meu_serial:
        thread = threading.Thread(target=meu_serial)
        thread.daemon = True
        thread.start()
    criar_interface_principal()
