import sys
import customtkinter as ctk
from datetime import datetime
from dashboard import DashboardFrame
from tkinter import messagebox
import pandas as pd
import os

try:
    from registro_log import registrar_acao, buscar_ultimos_logs
except ImportError:

    def registrar_acao(msg): print(f"LOG: {msg}")
    def buscar_ultimos_logs(f): return []

class SistemaTarefas(ctk.CTk):
    def __init__(self, user=None, funcao=None): 
        super().__init__() 

        # Armazenar os dados recebidos
        self.user = user
        self.funcao = funcao
        # Configuração da janela
        self.title("Sistema de Cadastro - V1.0.2026")
        self.geometry("900x600")
        # Configuração de Layout (Grid)
        self.grid_columnconfigure(0, minsize=250) 
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Chamadas dos setups
        self.setup_sidebar()
        self.setup_main_frame()
        self.setup_logs_frame()
        self.dash_frame = DashboardFrame(self)
        self.setup_main_frame() # Este é o seu frame de cadastro
        self.setup_logs_frame()
        self.mostrar_dashboard()
    # Função para chada do dashbord
    def mostrar_dashboard(self):
        # 1. Esconde as outras telas (Cadastro e Logs)
        if hasattr(self, 'main_frame'):
            self.main_frame.grid_forget()
        if hasattr(self, 'frame_logs'):
            self.frame_logs.grid_forget()
            
        # 2. Atualiza os números (lê o Excel novamente)
        self.dash_frame.atualizar_dados()
        
        # 3. Coloca o Dashboard na tela
        self.dash_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        
        # 4. Feedback visual nos botões (opcional)
        self.btn_dash.configure(fg_color="transparent")
        self.btn_cadastro.configure(fg_color="transparent")

        # Função sidebar que monta os botoes de acesso 
    def setup_sidebar(self):
        """Criação e organização da barra lateral"""
        self.sidebar = ctk.CTkFrame(self, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_propagate(False)
        
        self.logo_label = ctk.CTkLabel(self.sidebar, text="AD-PLATINA", font=ctk.CTkFont(size=28, weight="bold"))
        self.logo_label.pack(pady=20)

        # Botão Cadastro e Submenu
        self.btn_cadastro = ctk.CTkButton(self.sidebar, text="Cadastro  ▼", font=ctk.CTkFont(size=18),
                                          fg_color="transparent", anchor="w", command=self.toggle_submenu)
        self.btn_cadastro.pack(fill="x", padx=10, pady=5)

        self.sub_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        
        self.btn_sub_d = ctk.CTkButton(self.sub_frame, text="  Dizimos", font=ctk.CTkFont(size=18),
                                       fg_color="transparent", anchor="w", command=self.abrir_tela_cadastro)
        self.btn_sub_d.pack(fill="x", padx=(30, 15), pady=2)

        self.btn_sub_o = ctk.CTkButton(self.sub_frame, text=" Ofertas", font=ctk.CTkFont(size=18),
                                       fg_color="transparent", anchor="w", command=self.abrir_tela_cadastro)
        self.btn_sub_o.pack(fill="x", padx=(30, 15), pady=2)

        # Outros Botões
        self.btn_dash = ctk.CTkButton(self.sidebar, text="Dashboard", font=ctk.CTkFont(size=18), 
                                      fg_color="transparent", anchor="w", command=self.mostrar_dashboard)
        self.btn_dash.pack(fill="x", padx=10, pady=5)

        self.btn_logs = ctk.CTkButton(self.sidebar, text="Logs do Sistema", font=ctk.CTkFont(size=18), 
                                      fg_color="transparent", anchor="w", command=self.abrir_tela_logs)
        self.btn_logs.pack(fill="x", padx=10, pady=5)

        # Criar um Frame container para agrupar os dois elementos
        self.container_usuario = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        self.container_usuario.pack(side="bottom", fill="x", padx=10, pady=10)

        # Criar a Label do Usuário dentro do container
        texto_usuario = f"Bem-Vindo: {self.user}" if self.user else "Usuário: Admin"
        self.user_label = ctk.CTkLabel(
            self.container_usuario, 
            text=texto_usuario, 
            font=ctk.CTkFont(size=12),
            anchor="w"
        )
        # side="left"
        self.user_label.pack(side="left", fill="x", expand=True, padx=(5, 5))

        # Criar o Botão Sair dentro do container
        self.btn_sair = ctk.CTkButton(
            self.container_usuario, 
            text="Sair", 
            font=ctk.CTkFont(size=18), 
            fg_color="#cc0000",
            hover_color="#990000",
            width=80, 
            height=35,
            command=self.encerrar_sistema
        )
        # side="right" 
        self.btn_sair.pack(side="right", padx=(5, 5))
    
    # Função que encerra as seçoes do sistema
    def encerrar_sistema(self):
        self.quit()    # Para o loop do CustomTkinter
        self.destroy() # Destrói a janela atual
        sys.exit(0)


    def setup_main_frame(self):
        """Frame principal de Cadastro"""
        self.main_frame = ctk.CTkFrame(self, corner_radius=15)
        self.main_frame.grid(row=0, column=1, padx=30, pady=30, sticky="nsew")

        self.title_form = ctk.CTkLabel(self.main_frame, text="Cadastrar", font=ctk.CTkFont(size=24, weight="bold"))
        self.title_form.pack(pady=(20, 10), padx=30, anchor="w")

        # Inputs
        self.entry_nome = self.create_input("Nome")
        self.entry_val1 = self.create_input("Dizimos R$: ")
        self.entry_val2 = self.create_input("Outros valores R$ ")
        self.entry_outros = self.create_input("Outros Detalhes")

        # Botões
        self.btn_container = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.btn_container.pack(fill="x", padx=30, pady=20)

        self.btn_salvar = ctk.CTkButton(self.btn_container, text="Salvar Tarefa", text_color="#302828", fg_color="#2eb8ac", 
                                        hover_color="#248f85", font=("Segoe UI", 18, "bold"), height=45, command=self.salvar_dados)
        self.btn_salvar.pack(side="left", expand=True, fill="x", padx=(0, 10))

        self.btn_limpar = ctk.CTkButton(self.btn_container, text="Limpar", text_color="#302828", fg_color="#f09644", 
                                        hover_color="#c77b38", font=("Segoe UI", 18, "bold"), height=45, command=self.limpar_campos)
        self.btn_limpar.pack(side="left", expand=True, fill="x")

    def setup_logs_frame(self):
        """Frame de Logs (Inicia oculto)"""
        self.frame_logs = ctk.CTkFrame(self, corner_radius=15)
        
        self.lbl_logs = ctk.CTkLabel(self.frame_logs, text="Histórico de Atividades", font=("Arial", 20, "bold"))
        self.lbl_logs.pack(pady=10)

        self.txt_logs = ctk.CTkTextbox(self.frame_logs, width=500, height=300)
        self.txt_logs.pack(padx=20, pady=10, fill="both", expand=True)

        self.btn_voltar = ctk.CTkButton(self.frame_logs, text="Voltar ao Início", command=self.abrir_tela_cadastro)
        self.btn_voltar.pack(pady=10)

    def create_input(self, placeholder):
        """Helper para criar inputs padronizados"""
        entry = ctk.CTkEntry(self.main_frame, placeholder_text=placeholder, height=45)
        entry.pack(fill="x", padx=30, pady=5)
        return entry

    # --- LÓGICA DE NAVEGAÇÃO ---
    def toggle_submenu(self):
        if self.sub_frame.winfo_manager():
            self.sub_frame.pack_forget()
        else:
            self.sub_frame.pack(fill="x", after=self.btn_cadastro)

    def abrir_tela_logs(self):
        self.main_frame.grid_forget()
        self.frame_logs.grid(row=0, column=1, padx=30, pady=30, sticky="nsew")
        self.atualizar_visualizacao_logs()

    def abrir_tela_cadastro(self):
        self.frame_logs.grid_forget()
        self.main_frame.grid(row=0, column=1, padx=30, pady=30, sticky="nsew")

    def atualizar_visualizacao_logs(self, filtro=""):
        self.txt_logs.configure(state="normal")
        self.txt_logs.delete("1.0", "end")
        logs = buscar_ultimos_logs(filtro)
        
        if logs:
            for log in logs:
                self.txt_logs.insert("end", f"{log['Data/Hora Login']} - {log['Ação']}\n")
        else:
            self.txt_logs.insert("end", "Nenhum log encontrado.")
        self.txt_logs.configure(state="disabled")

        # --- LÓGICA DE DADOS ---
    def salvar_dados(self):
        nome = self.entry_nome.get().strip()
        filename = 'base_tarefas.xlsx'
        
        if not nome:
            messagebox.showwarning("Aviso", "O campo Nome é obrigatório.")
            return 
        
        try:
            # 1. Preparar os valores atuais
            # Usamos try/except interno para garantir que valores vazios não quebrem o código
            try:
                val_dizimo = float(self.entry_val1.get().replace(',', '.')) if self.entry_val1.get() else 0.0
                val_oferta = float(self.entry_val2.get().replace(',', '.')) if self.entry_val2.get() else 0.0
            except ValueError:
                messagebox.showerror("Erro", "Insira apenas números nos campos de valor (use ponto ou vírgula).")
                return

            # 2. Verificar se o nome já existe na base para exibir o alerta
            if os.path.exists(filename):
                df_existente = pd.read_excel(filename)
                df_existente.columns = [str(c).strip() for c in df_existente.columns]
                
                if 'Nome' in df_existente.columns:
                    mask = df_existente['Nome'].astype(str).str.upper() == nome.upper()
                    
                    if mask.any():
                        # Se o nome existe, apenas confirmamos se é isso mesmo que o usuário quer
                        pergunta = messagebox.askyesno("Usuário já cadastrado", 
                            f"O usuário '{nome}' já possui registros anteriores.\nDeseja adicionar este NOVO lançamento para ele?")
                        
                        if not pergunta:
                            return # Cancela se o usuário clicar em "Não"

            # 3. Criar a nova linha de dados (Histórico)
            novos_dados = {
                'Nome': [nome],
                'Dizimos': [val_dizimo],
                'Ofertas': [val_oferta],
                'Outros': [self.entry_outros.get()],
                'Data_Criacao': [datetime.now().strftime("%d/%m/%Y")] # Registra o dia exato
            }
            
            df_novo = pd.DataFrame(novos_dados)

            # 4. Salvar (sempre adicionando no final do arquivo)
            if not os.path.exists(filename):
                df_novo.to_excel(filename, index=False)
            else:
                # Carrega o que já existe e "gruda" a nova linha embaixo
                df_atual = pd.read_excel(filename)
                df_final = pd.concat([df_atual, df_novo], ignore_index=True)
                df_final.to_excel(filename, index=False)

            messagebox.showinfo("Sucesso", f"Lançamento registrado para {nome} com sucesso!")
            
            # Log e limpeza
            usuario_texto = f"{self.user}" if self.user else "Sistema"
            registrar_acao(f"Novo lançamento para: {nome} | Valor: {val_dizimo + val_oferta}")
            self.limpar_campos()
            
       
        except PermissionError:
        # Caso o arquivo esteja aberto
            messagebox.showerror("Erro de Permissão", 
                             "Não foi possível salvar! \n\nO arquivo 'base_tarefas.xlsx' está aberto. Feche o Excel e tente novamente.")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro inesperado: {e}")
            
    def limpar_campos(self):
        for entry in [self.entry_nome, self.entry_val1, self.entry_val2, self.entry_outros]:
            entry.delete(0, 'end')


if __name__ == "__main__":
    app = SistemaTarefas()
    app.mainloop()