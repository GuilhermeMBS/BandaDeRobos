# 🤖🎸 Banda de Robôs

Este projeto implementa uma banda formada por **3 robôs**:
- 🎸 Guitarrista
- 🥁 Baterista
- 🎤 Vocalista

Eles são controlados por servos conectados a um Arduino MEGA, e tocam músicas geradas por IA a partir de um *prompt* ou de músicas previamente geradas por esse mesmo local.

O código usa a API do Suno para gerar a música e as letras, e separa os instrumentos para que cada robô execute sua parte de forma sincronizada.

---

## 📋 Como funciona

### 1️⃣ Rode o servidor local
Em um terminal, execute:

python server.py

Esse servidor se conecta ao Ngrok para expor a API localmente e receber o callback da Suno com o áudio gerado.

### 2️⃣ Em outro terminal, execute o utilitário principal
python utils.py

Uma janela será aberta para você escolher entre:

1. Selecionar uma música pronta: escolha uma pasta com os arquivos da música já gerada.
2. Criar uma música nova: insira um prompt descritivo para que a API do Suno gere a música automaticamente.

### 3️⃣ Para uma música pronta
Basta selecionar a pasta com o nome da música desejada e iniciar.

### 4️⃣ Para criar uma nova música
Insira um prompt descritivo na nova janela e clique em gerar.

O prompt é enviado para a API do Suno, que gera uma música e devolve o áudio e a letra.

### 🎶 O que acontece durante a execução

✅ O som gerado ou escolhido é processado pelo utils.py, que:
- separa os instrumentos (usando Spleeter)
- extrai o ritmo e a energia da música
- sincroniza os comandos para os robôs com o áudio

✅ As instruções para cada robô são enviadas para o Arduino MEGA com o código arduino_implementacao.ino.

### 🎭 Funções dos robôs
🎤 Vocalista

Acende um LED quando a música está sendo reproduzida, proporcional à energia da voz.

Levanta e abaixa o braço do microfone conforme a energia.

🎸 Guitarrista

Move o braço no ritmo da música para simular acordes.

🥁 Baterista

Alterna os braços e ilumina os LEDs conforme as batidas.

LCD: mostra a letra da música verso a verso.

## 🗂 Estrutura dos arquivos
server.py	--> Servidor Flask + Ngrok para comunicação com a API do Suno

utils.py	--> Lógica principal do programa, com tratamento de áudio e da letra

gui.py	--> Interface gráfica para seleção/criação de músicas

arduino_implementacao.ino	--> Código para controlar os robôs no Arduino

### 🔧 Bibliotecas utilizadas
Python:

- Flask – servidor web
- requests – chamadas HTTP para a API
- pyngrok – integração com Ngrok
- tkinter – interface gráfica
- spleeter – separação de stems (vocais, bateria, etc.)
- librosa – análise de áudio e batidas
- numpy – cálculos numéricos
- sounddevice – reprodução de áudio
- pyserial – comunicação com o Arduino

Arduino:
- Servo – controle dos servos
- FastLED – controle dos LEDs RGB
- hd44780 – controle do LCD via I2C

### 🛠 Requisitos
- Arduino MEGA
- Servos motores para os movimentos dos robôs
- LED e LCD para o vocalista
- LEDs WS2811/WS2812 para o palco
- Cabos e fonte de alimentação adequados

<img width="3855" height="2135" alt="image" src="https://github.com/user-attachments/assets/c8f7af2d-9a9d-42f6-b693-b15930534e81" />

Divirta-se com a banda mais robótica do mundo! 🤖🎶
