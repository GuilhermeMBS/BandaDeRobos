import threading, requests
import tkinter as tk
from tkinter import filedialog, messagebox

# === Serial-reading stub ===
meu_serial = None  # Replace/initialize your Serial here

# === Configuration ===
API_BASE = "https://apibox.erweima.ai/api/v1/generate"  # Adjust if Flask runs elsewhere

# === Business logic ===
def tocar_musica_existente(file_path: str):
    # Your existing logic to play processed audio from file_path
    messagebox.showinfo("Info", f"Tocando música processada de:\n{file_path}")


def processar_musica(prompt: str):
    """
    Calls the Flask /generate endpoint with the given prompt.
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
    """
    Abre diálogo para selecionar um arquivo de áudio já processado.
    """
    filetypes = [("MP3 files", "*.mp3"), ("All files", "*")]
    path = filedialog.askopenfilename(title="Selecione o arquivo de música processada",
                                      filetypes=filetypes)
    if not path:
        return  # Usuário cancelou
    tocar_musica_existente(path)


def nova_musica_interface():
    """
    Abre uma nova janela para digitar o prompt de geração de música.
    """
    def on_submit():
        prompt = entry.get().strip()
        if not prompt:
            messagebox.showwarning("Aviso", "O prompt não pode ficar vazio.")
            return
        top.destroy()
        processar_musica(prompt)

    top = tk.Toplevel(root_main)
    top.title("Gerar Nova Música")
    top.geometry("400x150")
    top.resizable(False, False)

    tk.Label(top, text="Digite o prompt para geração de música:").pack(pady=(10,5))
    entry = tk.Entry(top, width=50)
    entry.pack(pady=(0,10))
    entry.focus_set()

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
        width=30,
        height=2
    ).pack(pady=(5, 2))

    tk.Button(
        root_main,
        text="Processar nova música",
        command=nova_musica_interface,
        width=30,
        height=2
    ).pack(pady=(2, 5))

    root_main.mainloop()

if __name__ == '__main__':
    print("[INFO] Serial: ok")
    thread = threading.Thread(target=meu_serial)
    thread.daemon = True
    thread.start()
    criar_interface_principal()