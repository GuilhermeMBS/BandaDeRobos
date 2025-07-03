import tkinter as tk
from tkinter import messagebox, ttk
import pygame
import time
import random
import sys
import os

'''
Observações:

1.  Cores Hexadecimais:
    No código, as cores são definidas usando **códigos hexadecimais**, como '#E0E0E0' ou '#FF5555'.
    * Um código hexadecimal de cor começa com '#' seguido por seis caracteres.
    * Cada par de caracteres representa a intensidade de uma cor primária (vermelho, verde, azul), variando de '00' (nenhuma intensidade) a 'FF' (intensidade total).
    * Por exemplo:
        * '#FF0000' é vermelho puro (FF para Red, 00 para Green, 00 para Blue).
        * '#00FF00' é verde puro.
        * '#0000FF' é azul puro.
        * '#FFFFFF' é branco (todas as cores no máximo).
        * '#000000' é preto (nenhuma cor).
        * '#E0E0E0' é um cinza claro (mistura igual de R, G, B em alta intensidade).
        * '#FF5555' é um tom de vermelho alaranjado.

2.  Pygame Mixer:
    * **Pygame** é uma biblioteca de módulos Python projetada para escrever jogos. Ela inclui funcionalidades para gráficos, som, entrada do usuário, etc.
    * O `pygame.mixer` é o módulo dentro do Pygame que lida com a reprodução de áudio. Ele permite carregar e tocar sons, gerenciar volumes, e controlar a reprodução de música (arquivos grandes como MP3 ou WAV).
    * `pygame.mixer.init(frequency, size, channels, buffer)`:
        * `frequency=44100`: Define a frequência de amostragem (sample rate) do áudio em Hertz (Hz). 44.1 kHz é a frequência padrão de CDs de áudio, significando que 44.100 amostras de áudio são tiradas por segundo para recriar o som. Uma frequência mais alta geralmente significa melhor qualidade de áudio, mas exige mais processamento.
        * `size=-16`: Define o tamanho da amostra (sample size). O valor -16 indica áudio estéreo de 16 bits assinado. Um valor de 16 seria áudio de 16 bits sem sinal. 16 bits é uma profundidade de bit comum e de boa qualidade.
        * `channels=2`: Define o número de canais de áudio. 2 significa estéreo (som com dois canais, esquerdo e direito). 1 seria mono.
        * `buffer=512`: Define o tamanho do buffer de mixagem em amostras. Um buffer é uma pequena porção de memória usada para armazenar dados de áudio antes de serem enviados para a placa de som. Um buffer menor pode reduzir o atraso (latência) entre o comando e o som, mas pode causar interrupções se o sistema não conseguir preenchê-lo a tempo. 512 é um valor relativamente pequeno, bom para baixa latência.
    * `pygame.mixer.music.load(caminho)`: Carrega um arquivo de áudio para ser reproduzido como música de fundo. O Pygame mixer é otimizado para tocar apenas um arquivo de música por vez, em loop se desejado.
    * `pygame.mixer.music.play(loops)`: Inicia a reprodução da música carregada. `loops=-1` significa que a música tocará indefinidamente. Um valor de `0` significa tocar uma vez, `1` significa tocar duas vezes, e assim por diante.
    * `pygame.mixer.music.pause()` / `unpause()`: Pausa e despausa a reprodução da música, respectivamente.
    * `pygame.mixer.music.stop()`: Para completamente a reprodução da música.
    * `pygame.mixer.music.get_pos()`: Retorna o tempo decorrido da música em milissegundos desde o início da reprodução ou desde a última vez que foi despausada.
    * `pygame.mixer.Sound(caminho).get_length()`: Carrega o arquivo de áudio como um objeto `Sound` (usado para efeitos sonoros curtos) e retorna sua duração em segundos. Isso é usado para obter a duração total do áudio para a barra de progresso.
    * `pygame.mixer.quit()`: Desinicializa o módulo mixer do Pygame, liberando os recursos de áudio.

3.  Tkinter (ttk - Themed Tkinter):
    * Tkinter é a biblioteca padrão do Python para criar interfaces gráficas de usuário (GUIs).
    * Widgets Tkinter: São os elementos visuais que você vê em uma janela, como botões, rótulos, caixas de texto, etc.
    * `tk.Frame`: Um Frame é um widget de contêiner. Pense nele como uma "moldura" ou uma "caixa" invisível onde você pode agrupar outros widgets. Isso ajuda a organizar a interface, tornando-a mais fácil de gerenciar e posicionar. Por exemplo, você pode ter um `Frame` para os controles de entrada e outro `Frame` para exibir os resultados.
        * `bg`: Define a cor de fundo do widget.
        * `padx`/`pady`: Adiciona preenchimento (espaço interno) horizontal/vertical dentro do widget.
    * `tk.Label`: Um widget para exibir texto ou imagens fixas.
    * `tk.Entry`: Um widget para entrada de texto de uma única linha.
    * `tk.Button`: Um widget de botão clicável.
    * `tk.Canvas`: Um widget que permite desenhar gráficos, linhas, retângulos, círculos, etc. É usado aqui para as animações de batida e equalizador, e também para a barra de progresso personalizada.
    * `tk.Text`: Um widget para exibir e editar texto multilinha.
    * `tk.StringVar`: Uma variável especial do Tkinter usada para manter o controle do texto em widgets como `Label` ou `Entry`. Quando o valor de um `StringVar` muda, o widget associado é automaticamente atualizado na interface.
    * `ttk` (Themed Tkinter): É um submódulo do Tkinter que fornece widgets com uma aparência mais moderna e "nativa" do sistema operacional, em contraste com os widgets mais básicos do Tkinter tradicional.
        * `ttk.Combobox`: Um widget de caixa de combinação (dropdown) que permite ao usuário selecionar um item de uma lista predefinida ou, opcionalmente, digitar um novo valor.
        * `ttk.Style()`: Permite customizar a aparência e o comportamento dos widgets `ttk`, como o Combobox.
    * Métodos de Layout:
        * `pack()`: Um gerenciador de layout que organiza os widgets em blocos antes de colocá-los na janela. É bom para layouts simples (empilhar verticalmente ou lado a lado).
        * `grid()`: Um gerenciador de layout que organiza os widgets em uma grade (linhas e colunas). Oferece controle mais preciso sobre o posicionamento e o dimensionamento dos widgets.
            * `row`/`column`: Define a linha e a coluna onde o widget será colocado.
            * `sticky`: Controla como o widget se "cola" aos lados de sua célula na grade (e, portanto, como ele se expande dentro dela). Por exemplo, `tk.N+tk.S+tk.W+tk.E` (Norte, Sul, Oeste, Leste) faz com que o widget preencha a célula completamente.
            * `rowconfigure()` / `columnconfigure()`: Usados em um widget pai (como um `Frame`) para especificar como as linhas e colunas dentro dele devem se expandir quando a janela é redimensionada. `weight=1` significa que a linha/coluna se expandirá.
    * `self.raiz.after(tempo_ms, funcao)`: Este método agenda uma função (`funcao`) para ser executada depois de um determinado número de milissegundos (`tempo_ms`). É crucial para criar animações e loops de atualização em interfaces gráficas, pois permite que o programa responda a eventos da interface enquanto executa tarefas em segundo plano.

4.  Manipulação de Caminhos (Paths) e Sistema de Arquivos:
    * `import os`: O módulo `os` fornece uma maneira de usar funcionalidades dependentes do sistema operacional, como interagir com o sistema de arquivos.
    * `os.path.join(diretorio, nome_arquivo)`: Constrói um caminho de arquivo ou diretório de forma inteligente, unindo os componentes com o separador de diretório correto para o sistema operacional em uso (por exemplo, `\` no Windows, `/` no Linux/macOS). Isso garante que o código seja portátil.
    * `os.path.dirname(__file__)`: Retorna o caminho do diretório onde o script Python atual (`__file__`) está localizado. Isso é útil para encontrar arquivos de recursos (como arquivos de áudio) que estão na mesma pasta do script, independentemente de onde o script é executado.
    * `os.path.exists(caminho)`: Verifica se um arquivo ou diretório existe no `caminho` especificado. Retorna `True` se existir, `False` caso contrário. Usado para garantir que o arquivo de áudio `beat.wav` possa ser encontrado antes de tentar carregá-lo.

'''

class GeradorMusicaApp:
    def __init__(self, raiz):
        # --- Configurações Iniciais da Janela ---
        # `self.raiz` armazena a janela principal do Tkinter.
        self.raiz = raiz
        # Define o título da janela.
        self.raiz.title("Gerador de Música")
        # Define a cor de fundo principal da janela.
        self.raiz.configure(bg='#E0E0E0')

        # --- Inicialização do Pygame Mixer ---
        # Bloco try-except para lidar com possíveis erros na inicialização do áudio.
        try:
            # Verifica se o mixer já foi inicializado para evitar duplicidade.
            if not pygame.mixer.get_init():
                # Inicializa o mixer com configurações específicas para qualidade e latência.
                pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
                # Adiciona um pequeno atraso para o mixer estabilizar.
                time.sleep(0.1) 
                
                # Tenta carregar e descarregar um som "dummy" (fictício) para "acordar" o mixer
                # e resolver alguns problemas de áudio em certos sistemas.
                caminho_som_dummy = os.path.join(os.path.dirname(__file__), "beat.wav")
                if os.path.exists(caminho_som_dummy):
                    try:
                        pygame.mixer.music.load(caminho_som_dummy)
                        pygame.mixer.music.unload()
                    except pygame.error:
                        pass # Ignora erros se o som dummy não puder ser carregado.
        except pygame.error as e:
            # Exibe uma mensagem de erro fatal se o sistema de áudio não puder ser inicializado.
            messagebox.showerror("Erro de Áudio", f"Não foi possível inicializar o sistema de áudio: {str(e)}")
            sys.exit(1) # Sai da aplicação.

        # --- Variáveis de Áudio ---
        # Define o arquivo de áudio padrão (provisório).
        self.arquivo_audio = "beat.wav"
        # Variável para armazenar a duração do áudio em segundos, inicializada como 0.
        self.duracao_audio_segundos = 0

        # --- Configuração da Interface Gráfica ---
        # Chama o método para construir todos os elementos da interface.
        self.configurar_interface()

        # --- Variáveis de Controle de Animação e Reprodução ---
        # Flags booleanas para controlar o estado das animações.
        self.batida_animando = False
        self.eq_animando = False
        self.progresso_animando = False
        # Variáveis para rastrear o tempo de reprodução (início e pausa).
        self.tempo_inicio_reproducao = 0
        self.tempo_pausado = 0 
        
        # --- Protocolo de Fechamento da Janela ---
        # Associa a função `ao_fechar` ao evento de fechar a janela (clicar no 'X').
        self.raiz.protocol("WM_DELETE_WINDOW", self.ao_fechar)
    
    def configurar_interface(self):
        # --- Estilos de Fonte e Widget ---
        # Define estilos de fonte reutilizáveis.
        self.fonte_negrito = ('Helvetica', 10, 'bold')
        self.fonte_titulo = ('Helvetica', 11, 'bold')
        # Define um dicionário de opções para estilizar caixas de entrada (Entry).
        self.estilo_entrada = {'width': 22, 'bd': 1, 'relief': tk.SOLID, 'highlightbackground': '#C0C0C0', 'highlightthickness': 1} 
        # Define um dicionário de opções para estilizar botões padrão.
        self.estilo_botao = {'bd': 0, 'relief': tk.FLAT, 'activebackground': '#A0A0A0', 'bg': '#D0D0D0'}
        # Define um estilo específico para o botão de play/pause, com cor de destaque.
        self.estilo_botao_play = {'bd': 0, 'relief': tk.FLAT, 'activebackground': '#FF8888', 'bg': '#FF5555', 'fg': 'white'} 

        # --- Frame Principal ---
        # Cria o frame principal que conterá todas as outras seções da interface.
        frame_principal = tk.Frame(self.raiz, bg='#E0E0E0') 
        # Empacota o frame principal para preencher toda a janela e expandir.
        frame_principal.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # Configura as colunas e linhas do frame principal para se expandirem conforme o necessário.
        # Coluna 0 (Controles) não se expande horizontalmente.
        frame_principal.grid_columnconfigure(0, weight=0)
        # Coluna 1 (Área de Resultado) se expande horizontalmente.
        frame_principal.grid_columnconfigure(1, weight=1)
        # A linha 0 (onde estão os dois frames principais) se expande verticalmente.
        frame_principal.grid_rowconfigure(0, weight=1) 
        
        # --- Frame da Coluna de Controles ---
        # Cria um frame para agrupar os widgets de entrada e controle.
        frame_controle = tk.Frame(frame_principal, bg='#E0E0E0')
        # Posiciona o frame de controle na grade (grid) do frame principal.
        # `sticky=tk.N+tk.S+tk.W` faz com que ele se "cole" aos lados Norte, Sul e Oeste, expandindo verticalmente.
        frame_controle.grid(row=0, column=0, padx=10, pady=5, sticky=tk.N+tk.S+tk.W)
        
        # --- Definição de Preenchimento (Padding) ---
        # Valores de padding para espaçamento consistente entre os widgets.
        pady_pequeno = 5
        pady_medio = 15
        pady_grande = 20

        # --- Configuração dos Campos de Texto e Seleção ---
        # Rótulo para o campo PROMPT.
        tk.Label(frame_controle, text="PROMPT", font=self.fonte_titulo, bg='#E0E0E0').grid(row=0, column=0, sticky=tk.W, pady=(0,pady_pequeno))
        # Campo de entrada de texto para o prompt.
        self.entrada_prompt = tk.Entry(frame_controle, **self.estilo_entrada)
        self.entrada_prompt.grid(row=1, column=0, pady=(0,pady_medio), sticky=tk.W+tk.E)
        
        # Rótulo para a seleção de ESTILO.
        tk.Label(frame_controle, text="ESTILO", font=self.fonte_titulo, bg='#E0E0E0').grid(row=2, column=0, sticky=tk.W, pady=(0,pady_pequeno))
        # Variável para armazenar o valor selecionado no Combobox de estilo.
        self.estilo = tk.StringVar(value="(selecione)")
        # Combobox para seleção do estilo musical.
        menu_estilo = ttk.Combobox(frame_controle, textvariable=self.estilo, 
                                     values=["(selecione)", "Rock", "Punk", "Pop", "Metal"], 
                                     state="readonly", width=20)
        menu_estilo.grid(row=3, column=0, pady=(0,pady_medio), sticky=tk.W+tk.E)
        
        # Rótulo para a seleção de SENTIMENTO.
        tk.Label(frame_controle, text="SENTIMENTO", font=self.fonte_titulo, bg='#E0E0E0').grid(row=4, column=0, sticky=tk.W, pady=(0,pady_pequeno))
        # Variável para armazenar o valor selecionado no Combobox de sentimento.
        self.sentimento = tk.StringVar(value="(selecione)")
        # Combobox para seleção do sentimento.
        menu_sentimento = ttk.Combobox(frame_controle, textvariable=self.sentimento, 
                                         values=["(selecione)", "Alegria", "Tristeza", "Raiva", "Amor"], 
                                         state="readonly", width=20)
        menu_sentimento.grid(row=5, column=0, pady=(0,pady_medio), sticky=tk.W+tk.E)
        
        # --- Botão Gerar Música ---
        self.botao_gerar = tk.Button(frame_controle, text="GERAR MÚSICA", font=self.fonte_negrito,
                                     command=self.gerar_musica, **self.estilo_botao, fg='#333333')
        self.botao_gerar.grid(row=6, column=0, pady=(5,pady_grande), sticky=tk.W+tk.E, ipadx=5, ipady=5)
        
        # --- Controles de Reprodução (Play/Pause) ---
        # Frame para agrupar o botão de play/pause.
        frame_play = tk.Frame(frame_controle, bg='#E0E0E0')
        frame_play.grid(row=7, column=0, pady=(0,pady_medio), sticky=tk.W)
        
        # Botão de Play/Pause.
        self.botao_play = tk.Button(frame_play, text="►", font=('Helvetica', 16, 'bold'), width=3,
                                     command=self.alternar_reproducao, **self.estilo_botao_play) 
        self.botao_play.pack(side=tk.LEFT, padx=(0,10), ipadx=5, ipady=2)
        # Flags para controlar o estado de reprodução (tocando ou pausado).
        self.esta_tocando = False
        self.esta_pausado = False
        
        # --- Visualização da Batida e Equalizador ---
        # Frame para agrupar as animações visuais.
        frame_animacoes = tk.Frame(frame_controle, bg='#E0E0E0')
        frame_animacoes.grid(row=8, column=0, pady=(0,10), sticky=tk.W)
        
        # Canvas para a animação da batida (um quadrado que pulsa).
        self.canvas_batida = tk.Canvas(frame_animacoes, width=50, height=50, bg='white', 
                                         highlightthickness=0, bd=0)
        self.canvas_batida.pack(side=tk.LEFT)
        # Cria o retângulo inicial da batida no canvas.
        self.retangulo_batida = self.canvas_batida.create_rectangle(5, 5, 45, 45, fill='white')
        
        # Canvas para a animação do equalizador (barras que se movem).
        self.canvas_eq = tk.Canvas(frame_animacoes, width=150, height=50, bg='#333333', highlightthickness=0, bd=0)
        self.canvas_eq.pack(side=tk.LEFT, padx=(10,0))
        # Lista para armazenar as referências das barras do equalizador.
        self.barras_eq = []
        # Cria 10 barras retangulares para o equalizador.
        for i in range(10):
            x1 = 5 + i * 14
            x2 = x1 + 8
            barra = self.canvas_eq.create_rectangle(x1, 45, x2, 45, fill='#00EE00', width=0) 
            self.barras_eq.append(barra)
        
        # --- Barra de Progresso da Música ---
        # Frame para a barra de progresso e o display de tempo.
        frame_progresso = tk.Frame(frame_controle, bg='#E0E0E0')
        frame_progresso.grid(row=9, column=0, pady=(10,0), sticky=tk.W+tk.E)
        
        # Canvas para o fundo da barra de progresso.
        self.fundo_progresso = tk.Canvas(frame_progresso, height=4, bg='#C0C0C0', highlightthickness=0)
        self.fundo_progresso.pack(fill=tk.X, expand=True)
        # Cria a barra de progresso (inicialmente com largura 0).
        self.barra_progresso = self.fundo_progresso.create_rectangle(0, 0, 0, 4, fill='#FF5555', width=0)
        
        # Variável para exibir o tempo atual e total da música.
        self.variavel_tempo = tk.StringVar(value="0:00 / 0:00")
        # Rótulo para exibir o tempo.
        self.rotulo_tempo = tk.Label(frame_progresso, textvariable=self.variavel_tempo, 
                                         font=('Helvetica', 8), bg='#E0E0E0', fg='#555555')
        self.rotulo_tempo.pack(pady=(3,0), anchor=tk.W)
        
        # --- Área de Resultados ---
        # Frame para exibir os resultados da geração de música.
        frame_resultado = tk.Frame(frame_principal, bg='#E0E0E0')
        # Posiciona o frame de resultado na grade do frame principal, expandindo em todas as direções.
        frame_resultado.grid(row=0, column=1, padx=(20,10), pady=5, sticky=tk.N+tk.E+tk.S+tk.W) 
        # Permite que a coluna e a linha dentro do frame de resultado se expandam.
        frame_resultado.columnconfigure(0, weight=1)
        frame_resultado.rowconfigure(1, weight=1) 

        # Rótulo para a área de resultado.
        tk.Label(frame_resultado, text="RESULTADO", font=self.fonte_titulo, bg='#E0E0E0').grid(row=0, column=0, sticky=tk.W, pady=(0,pady_pequeno))
        # Widget de texto para exibir os resultados.
        self.area_texto_resultado = tk.Text(frame_resultado, wrap=tk.WORD, 
                                     bd=1, relief=tk.SOLID, font=('Helvetica', 10), bg='white', fg='#333333') 
        # Posiciona a área de texto, fazendo-a preencher todo o espaço disponível.
        self.area_texto_resultado.grid(row=1, column=0, pady=(0,0), sticky=tk.N+tk.E+tk.S+tk.W)
        
        # Placeholder inicial para a área de resultado.
        self.area_texto_resultado.insert(tk.END, "Resultados da Geração:\n\nAguardando música ser gerada...")
        self.area_texto_resultado.config(state=tk.DISABLED) # Desabilita a edição manual.
        
        # --- Barra de Status na Parte Inferior ---
        # Variável para armazenar a mensagem da barra de status.
        self.variavel_status = tk.StringVar(value="Pronto")
        # Rótulo que serve como barra de status, exibindo mensagens para o usuário.
        self.barra_status = tk.Label(self.raiz, textvariable=self.variavel_status, 
                                         bd=0, relief=tk.FLAT, anchor=tk.W, # Alinha o texto à esquerda.
                                         bg='#A0A0A0', fg='white', padx=10, pady=2) 
        self.barra_status.pack(side=tk.BOTTOM, fill=tk.X) # Empacota na parte inferior, preenchendo a largura.

        # --- Estilização do Combobox (ttk) ---
        # Cria um objeto Style para aplicar estilos aos widgets ttk.
        estilo_ttk = ttk.Style()
        # Define o tema padrão.
        estilo_ttk.theme_use('default') 
        # Configura as propriedades visuais do Combobox.
        estilo_ttk.configure('TCombobox',
                             fieldbackground='white', # Cor de fundo do campo de texto.
                             background='#D0D0D0',   # Cor de fundo do botão do Combobox.
                             foreground='#333333',   # Cor do texto.
                             selectbackground='white', # Cor de fundo do texto selecionado.
                             selectforeground='black', # Cor do texto selecionado.
                             bordercolor='#C0C0C0',   # Cor da borda.
                             borderwidth=1,
                             relief='solid')
        # Mapeia as cores de fundo para diferentes estados (leitura e ativo).
        estilo_ttk.map('TCombobox',
                       fieldbackground=[('readonly', 'white')],
                       background=[('readonly', '#D0D0D0'), ('active', '#A0A0A0')])
        # Configura a borda do Combobox.
        estilo_ttk.configure("TCombobox.Border", background="white")
        # Configura a lista suspensa do Combobox.
        estilo_ttk.configure("TCombobox.Listbox", background="white", foreground="#333333",
                             selectbackground="#FF5555", selectforeground="white")
    
    # --- Métodos de Controle do Ciclo de Vida da Aplicação ---
    def ao_fechar(self):
        # Para qualquer reprodução de áudio do Pygame.
        self.parar_reproducao() 
        # Encerra o mixer do Pygame para liberar recursos de áudio.
        pygame.mixer.quit() 
        # Fecha a janela do Tkinter.
        self.raiz.destroy()
    
    # --- Lógica de Geração de Música ---
    def gerar_musica(self):
        # Obtém os valores dos campos de entrada.
        prompt = self.entrada_prompt.get()
        estilo = self.estilo.get()
        sentimento = self.sentimento.get()
        
        # --- Validação de Entrada ---
        # Verifica se algum campo está vazio ou com a seleção padrão.
        if prompt == "" and (estilo == "(selecione)" or sentimento == "(selecione)"):
            messagebox.showerror("Erro", "Há caixas não preenchidas, não é possível gerar uma música.")
            return
        elif estilo == "(selecione)" or sentimento == "(selecione)": 
            messagebox.showerror("Erro", "Selecione estilo e sentimento para gerar uma música.")
            return
        elif prompt == "":
            messagebox.showerror("Erro", "Insira um prompt para gerar uma música.")
            return
        
        # Para qualquer música que esteja tocando antes de gerar uma nova.
        self.parar_reproducao() 

        self.variavel_status.set(f"Gerando música {estilo} {sentimento}...")
        # Força a atualização da interface para exibir a mensagem de status imediatamente.
        self.raiz.update_idletasks()
        
        # --- Simulação de Progresso da Geração ---
        for i in range(5):
            progresso = (i+1)/5 # Calcula o progresso em incrementos.
            # Obtém a largura atual do canvas da barra de progresso.
            largura_canvas_progresso = self.fundo_progresso.winfo_width() 
            # Define uma largura padrão caso a largura não esteja definida (ex: na inicialização).
            if largura_canvas_progresso == 1:
                largura_canvas_progresso = 200 
            # Atualiza as coordenadas da barra de progresso para simular o preenchimento.
            self.fundo_progresso.coords(self.barra_progresso, 0, 0, largura_canvas_progresso * progresso, 4)
            self.variavel_status.set(f"Gerando... {int(progresso*100)}%")
            self.raiz.update_idletasks() # Força nova atualização da UI.
            time.sleep(0.2) # Pequena pausa para simular o processamento.
        
        # --- Atualiza a Área de Resultados ---
        # Habilita a edição temporariamente para inserir o texto.
        self.area_texto_resultado.config(state=tk.NORMAL)
        self.area_texto_resultado.delete(1.0, tk.END) # Limpa o conteúdo existente.
        self.area_texto_resultado.insert(tk.END, 
            f"Música Gerada!\n\n"
            f"Prompt: {prompt}\n"
            f"Estilo: {estilo}\n"
            f"Sentimento: {sentimento}\n\n"
        )
        self.area_texto_resultado.config(state=tk.DISABLED) # Desabilita a edição novamente.

        # Reseta a barra de progresso visualmente.
        self.fundo_progresso.coords(self.barra_progresso, 0, 0, 0, 4)
        self.variavel_status.set("Pronto para tocar!")

        # --- Carregamento do Áudio ---
        # Verifica se o arquivo de áudio existe.
        if os.path.exists(self.arquivo_audio):
            try:
                pygame.mixer.music.load(self.arquivo_audio) # Carrega o arquivo de áudio no mixer.
                # Obtém a duração do áudio em segundos.
                self.duracao_audio_segundos = pygame.mixer.Sound(self.arquivo_audio).get_length()
                # Converte a duração para formato de minutos e segundos.
                total_minutos, total_segundos = divmod(int(self.duracao_audio_segundos), 60)
                # Atualiza o rótulo de tempo.
                self.variavel_tempo.set(f"0:00 / {total_minutos}:{total_segundos:02d}")
            except pygame.error as e:
                # Exibe aviso se o áudio não puder ser carregado e simula duração.
                messagebox.showwarning("Aviso", f"Não foi possível carregar o áudio '{self.arquivo_audio}': {str(e)}\nA reprodução será simulada.")
                self.duracao_audio_segundos = 194 # Duração simulada (3:14)
            except Exception as e:
                # Captura outros erros inesperados durante o carregamento do áudio.
                messagebox.showwarning("Aviso", f"Erro inesperado ao carregar áudio: {str(e)}\nA reprodução será simulada.")
                self.duracao_audio_segundos = 194
                pygame.mixer.music.unload() # Tenta descarregar para evitar problemas.
        else:
            # Aviso se o arquivo de áudio não for encontrado.
            messagebox.showwarning("Aviso", f"Arquivo de áudio '{self.arquivo_audio}' não encontrado.\nA reprodução será simulada com duração de 3:14.")
            self.duracao_audio_segundos = 194 # Duração simulada.
            pygame.mixer.music.unload() # Descarrega áudio se não foi encontrado.
    
    # --- Métodos de Controle de Reprodução de Áudio ---
    def alternar_reproducao(self):
        # Verifica se há uma música para tocar ou se o mixer está ativo.
        if self.duracao_audio_segundos == 0 and not pygame.mixer.music.get_busy():
            messagebox.showwarning("Aviso", "Gere uma música primeiro para tocar.")
            return

        # Alterna entre os estados de reprodução.
        if self.esta_tocando:
            self.pausar_reproducao()
        elif self.esta_pausado:
            self.despausar_reproducao()
        else:
            self.iniciar_reproducao()
    
    def iniciar_reproducao(self):
        # Inicia a reprodução da música ou a despausa.
        try:
            # Verifica se a música não está tocando ou se está pausada.
            if not pygame.mixer.music.get_busy() or self.esta_pausado:
                if self.esta_pausado:
                    # Se estiver pausado, despausa e ajusta o tempo de início.
                    pygame.mixer.music.unpause()
                    self.tempo_inicio_reproducao = time.time() - self.tempo_pausado 
                    self.esta_pausado = False
                else:
                    # Se não estiver tocando nem pausado, tenta carregar e tocar.
                    if os.path.exists(self.arquivo_audio) and self.duracao_audio_segundos > 0:
                        pygame.mixer.music.load(self.arquivo_audio)
                        pygame.mixer.music.play(loops=-1) # Toca em loop infinito.
                    else:
                        # Se o áudio não for válido, avisa e continua com simulação.
                        messagebox.showwarning("Aviso", "Não há áudio para tocar. Iniciando simulação.")
                    self.tempo_inicio_reproducao = time.time() # Registra o tempo de início.
                
                self.esta_tocando = True
                self.botao_play.config(text="||") # Altera o ícone do botão para "pausar".
                self.variavel_status.set("Tocando...")
                self.iniciar_animacoes() # Inicia as animações.

        except pygame.error as e:
            # Lida com erros específicos do Pygame durante a reprodução.
            messagebox.showerror("Erro", f"Erro ao reproduzir áudio: {str(e)}")
            self.esta_tocando = False
            self.esta_pausado = False
            self.botao_play.config(text="►")
            self.parar_animacoes()
        except Exception as e:
            # Lida com outros erros inesperados.
            messagebox.showerror("Erro", f"Erro inesperado: {str(e)}")
            self.esta_tocando = False
            self.esta_pausado = False
            self.botao_play.config(text="►")
            self.parar_animacoes()

    def pausar_reproducao(self):
        # Pausa a reprodução da música, salvando a posição atual.
        try:
            if pygame.mixer.music.get_busy(): # Só pausa se estiver tocando.
                pygame.mixer.music.pause()
                # Salva o tempo atual em segundos onde a música foi pausada.
                self.tempo_pausado = (pygame.mixer.music.get_pos() / 1000.0)
                self.esta_tocando = False
                self.esta_pausado = True
                self.botao_play.config(text="►") # Altera o ícone do botão para "play".
                self.variavel_status.set("Pausado")
                self.parar_animacoes_na_pausa() # Para as animações, exceto a barra de progresso.
        except Exception as e:
            print(f"Erro ao pausar: {e}")
            pass
            
    def despausar_reproducao(self):
        # Despausa a reprodução da música, retomando do ponto onde foi pausada.
        try:
            if self.esta_pausado: # Só despausa se estiver no estado de pausado.
                pygame.mixer.music.unpause()
                # Recalcula o tempo de início para que a barra de progresso continue corretamente.
                self.tempo_inicio_reproducao = time.time() - self.tempo_pausado 
                self.esta_tocando = True
                self.esta_pausado = False
                self.botao_play.config(text="||") # Altera o ícone do botão para "pausar".
                self.variavel_status.set("Tocando...")
                self.iniciar_animacoes() # Retoma as animações.
        except Exception as e:
            print(f"Erro ao despausar: {e}")
            pass

    def parar_reproducao(self):
        # Para completamente a reprodução da música e reseta todos os estados.
        try:
            if pygame.mixer.music.get_busy() or self.esta_pausado:
                pygame.mixer.music.stop() # Para a reprodução no Pygame.
        except Exception as e:
            print(f"Erro ao parar: {e}")
            pass
        finally:
            # Garante que todos os estados de reprodução e animação sejam resetados, independentemente de erros.
            self.esta_tocando = False
            self.esta_pausado = False
            self.botao_play.config(text="►") # Retorna o ícone do botão para "play".
            self.parar_animacoes() # Para e reseta todas as animações visuais.
            self.variavel_status.set("Pronto")
            self.tempo_pausado = 0 # Reseta o tempo de pausa.
    
    # --- Métodos de Controle de Animação ---
    def iniciar_animacoes(self):
        # Ativa as flags de animação.
        self.batida_animando = True
        self.eq_animando = True
        self.progresso_animando = True
        
        # Inicia os loops de atualização das animações.
        self.animar_batida()
        self.animar_eq()
        self.animar_progresso()
    
    def parar_animacoes(self):
        # Desativa as flags de animação para interromper os loops.
        self.batida_animando = False
        self.eq_animando = False
        self.progresso_animando = False
        
        # Reseta o estado visual da animação da batida para branco.
        self.canvas_batida.itemconfig(self.retangulo_batida, fill='white')
        # Reseta as alturas das barras do equalizador para a base.
        for barra in self.barras_eq:
            self.canvas_eq.coords(barra, self.canvas_eq.coords(barra)[0], 45, self.canvas_eq.coords(barra)[2], 45)
        
        # Reseta a barra de progresso e o rótulo de tempo para o estado inicial.
        self.fundo_progresso.coords(self.barra_progresso, 0, 0, 0, 4)
        total_minutos, total_segundos = divmod(int(self.duracao_audio_segundos), 60)
        self.variavel_tempo.set(f"0:00 / {total_minutos}:{total_segundos:02d}")

    def parar_animacoes_na_pausa(self):
        # Desativa as flags de animação para batida e equalizador, mas não a de progresso.
        self.batida_animando = False
        self.eq_animando = False
        # Reseta o estado visual da batida para branco.
        self.canvas_batida.itemconfig(self.retangulo_batida, fill='white')
        # Reseta as alturas das barras do equalizador para a base.
        for barra in self.barras_eq:
            self.canvas_eq.coords(barra, self.canvas_eq.coords(barra)[0], 45, self.canvas_eq.coords(barra)[2], 45)

    def animar_batida(self):
        # Anima a cor do quadrado da batida para simular um "piscar".
        if not self.batida_animando:
            return # Interrompe a animação se a flag estiver desativada.
            
        posicao_atual_ms = pygame.mixer.music.get_pos() # Obtém a posição atual da música em milissegundos.
        if self.esta_pausado:
            tempo_decorrido_seg = self.tempo_pausado # Mantém o tempo pausado se a música estiver pausada.
        else:
            tempo_decorrido_seg = posicao_atual_ms / 1000.0 # Converte milissegundos para segundos.

        intervalo_batida = 0.6 # Intervalo fixo para a simulação da batida.
        
        # Alterna a cor do retângulo da batida a cada intervalo.
        if int(tempo_decorrido_seg / intervalo_batida) % 2 == 0:
            nova_cor = '#ff5555'
        else:
            nova_cor = 'white'
        self.canvas_batida.itemconfig(self.retangulo_batida, fill=nova_cor)
        
        # Calcula o tempo para a próxima atualização da animação da batida.
        proximo_tempo_batida = (int(tempo_decorrido_seg / intervalo_batida) + 1) * intervalo_batida
        atraso_ms = int((proximo_tempo_batida - tempo_decorrido_seg) * 1000) 
        if atraso_ms <= 0:
            atraso_ms = 10 # Garante um atraso mínimo para evitar loops infinitos.

        self.raiz.after(atraso_ms, self.animar_batida) # Agenda a próxima chamada da função.
    
    def animar_eq(self):
        # Anima as alturas das barras do equalizador de forma aleatória.
        if not self.eq_animando:
            return # Interrompe a animação se a flag estiver desativada.
            
        for i, barra in enumerate(self.barras_eq):
            altura_base = random.randint(5, 45) # Altura base aleatória.
            if i % 3 == 0:
                altura = min(altura_base + 15, 45) # Algumas barras são um pouco mais altas.
            else:
                altura = altura_base
            
            coordenadas_atuais = self.canvas_eq.coords(barra) # Obtém as coordenadas atuais da barra.
            altura_atual = 45 - coordenadas_atuais[1] # Calcula a altura atual da barra.
            nova_altura = int(altura_atual * 0.3 + altura * 0.7) # Suaviza a transição da altura.
            
            # Atualiza as coordenadas da barra para refletir a nova altura.
            self.canvas_eq.coords(barra, coordenadas_atuais[0], 45 - nova_altura, 
                                     coordenadas_atuais[2], 45) 
        
        self.raiz.after(100, self.animar_eq) # Agenda a próxima atualização do equalizador a cada 100 ms.
    
    def animar_progresso(self):
        # Atualiza a barra de progresso e o display de tempo da música.
        if not self.progresso_animando:
            return # Interrompe a animação se a flag estiver desativada.
            
        if self.duracao_audio_segundos == 0:
            self.parar_reproducao() # Para a reprodução se a duração do áudio for zero.
            return

        if self.esta_pausado:
            tempo_decorrido_seg = self.tempo_pausado # Se pausado, usa o tempo salvo na pausa.
        else:
            posicao_atual_ms = pygame.mixer.music.get_pos() # Obtém a posição atual da música em milissegundos.
            tempo_decorrido_seg = posicao_atual_ms / 1000.0 # Converte para segundos.
            
            if posicao_atual_ms == -1: # Se a música não estiver tocando (retorno de -1 do Pygame).
                self.parar_reproducao() # Para a reprodução.
                return

        progresso = min(tempo_decorrido_seg / self.duracao_audio_segundos, 1.0) # Calcula o progresso (0 a 1).
        
        # Calcula a largura da barra de progresso com base na largura atual do canvas pai.
        largura_canvas_progresso = self.fundo_progresso.winfo_width() 
        if largura_canvas_progresso == 1:
            largura_canvas_progresso = 200 # Valor padrão se a largura ainda não foi renderizada.
        
        # Atualiza as coordenadas da barra de progresso.
        self.fundo_progresso.coords(self.barra_progresso, 0, 0, largura_canvas_progresso * progresso, 4) 
        
        # Converte o tempo decorrido e o tempo total para formato minutos:segundos.
        minutos, segundos = divmod(int(tempo_decorrido_seg), 60)
        total_minutos, total_segundos = divmod(int(self.duracao_audio_segundos), 60)
        # Atualiza o rótulo de tempo.
        self.variavel_tempo.set(f"{minutos}:{segundos:02d} / {total_minutos}:{total_segundos:02d}")
        
        # Se a música terminou e não está pausada, para a reprodução.
        if tempo_decorrido_seg >= self.duracao_audio_segundos and not self.esta_pausado:
            self.parar_reproducao()
            return

        self.raiz.after(50, self.animar_progresso) # Agenda a próxima atualização a cada 50 ms.

# --- Ponto de Entrada Principal da Aplicação ---
if __name__ == "__main__":
    raiz = tk.Tk() # Cria a janela principal do Tkinter.
    
    # --- Centralização da Janela ---
    largura_janela = 700
    altura_janela = 500
    # Obtém a largura e altura da tela do monitor.
    largura_tela = raiz.winfo_screenwidth() 
    altura_tela = raiz.winfo_screenheight()

    # Calcula as posições X e Y para centralizar a janela.
    posicao_x = int((largura_tela/2) - (largura_janela/2))
    posicao_y = int((altura_tela/2) - (altura_janela/2))

    # Define o tamanho e a posição da janela.
    raiz.geometry(f"{largura_janela}x{altura_janela}+{posicao_x}+{posicao_y}")
    
    # Cria uma instância da classe GeradorMusicaApp, passando a janela principal.
    app = GeradorMusicaApp(raiz)
    # Inicia o loop principal do Tkinter, que mantém a janela aberta e processa eventos.
    raiz.mainloop()
