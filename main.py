import customtkinter as ctk
from datetime import datetime
import pandas as pd
import os
from registro_log import registrar_acao, buscar_ultimos_logs

# Configurações globais
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class SistemaTarefas(ctk.CTk):
    def __init__(self): 
        super().__init__() 

        self.title("Sistema de Cadastro - V1.0.2026")
        self.geometry("900x600")

        # Configuração de Layout (Grid)
        self.grid_columnconfigure(0, minsize=250) 
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.setup_sidebar()
        self.setup_main_frame()
        self.setup_logs_frame()

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

        self.btn_sub_o = ctk.CTkButton(self.sub_frame, text="  Ofertas", font=ctk.CTkFont(size=18),
                                       fg_color="transparent", anchor="w", command=self.abrir_tela_cadastro)
        self.btn_sub_o.pack(fill="x", padx=(30, 15), pady=2)

        # Outros Botões
        self.btn_dash = ctk.CTkButton(self.sidebar, text="Dashboard", font=ctk.CTkFont(size=18), 
                                      fg_color="transparent", anchor="w", command=self.abrir_tela_cadastro)
        self.btn_dash.pack(fill="x", padx=10, pady=5)

        self.btn_logs = ctk.CTkButton(self.sidebar, text="Logs do Sistema", font=ctk.CTkFont(size=18), 
                                      fg_color="transparent", anchor="w", command=self.abrir_tela_logs)
        self.btn_logs.pack(fill="x", padx=10, pady=5)

        self.user_label = ctk.CTkLabel(self.sidebar, text="Usuário: Admin", font=ctk.CTkFont(size=12))
        self.user_label.pack(side="bottom", pady=20)

    def setup_main_frame(self):
        """Frame principal de Cadastro"""
        self.main_frame = ctk.CTkFrame(self, corner_radius=15)
        self.main_frame.grid(row=0, column=1, padx=30, pady=30, sticky="nsew")

        self.title_form = ctk.CTkLabel(self.main_frame, text="Cadastrar", font=ctk.CTkFont(size=24, weight="bold"))
        self.title_form.pack(pady=(20, 10), padx=30, anchor="w")

        # Inputs
        self.entry_nome = self.create_input("Nome")
        self.entry_sobrenome = self.create_input("Sobrenome")
        self.entry_val1 = self.create_input("Valor 1")
        self.entry_val2 = self.create_input("Valor 2")
        self.entry_outros = self.create_input("Outros Detalhes")

        # Botões
        self.btn_container = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.btn_container.pack(fill="x", padx=30, pady=20)

        self.btn_salvar = ctk.CTkButton(self.btn_container, text="Salvar Tarefa", fg_color="#2eb8ac", 
                                        hover_color="#248f85", height=45, command=self.salvar_dados)
        self.btn_salvar.pack(side="left", expand=True, fill="x", padx=(0, 10))

        self.btn_limpar = ctk.CTkButton(self.btn_container, text="Limpar", fg_color="#f09644", 
                                        hover_color="#c77b38", height=45, command=self.limpar_campos)
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
                self.txt_logs.insert("end", f"{log['Data/Hora']} - {log['Ação']}\n")
        else:
            self.txt_logs.insert("end", "Nenhum log encontrado.")
        self.txt_logs.configure(state="disabled")

    # --- LÓGICA DE DADOS ---
    def salvar_dados(self):
        nome = self.entry_nome.get()
        
        # 1. Validação simples: Não salvar se o nome estiver vazio
        if not nome.strip():
            print("Erro: O campo Nome é obrigatório.")
            return 
        
        try:
            # 2. Preparar os dados para o Excel
            dados = {
                'Nome': [nome],
                'Sobrenome': [self.entry_sobrenome.get()],
                'Valor1': [self.entry_val1.get()],
                'Valor2': [self.entry_val2.get()],
                'Outros': [self.entry_outros.get()],
                'Data_Criacao': [datetime.now().strftime("%d/%m/%Y")]
            }
            
            df = pd.DataFrame(dados)
            filename = 'base_tarefas.xlsx'
            
            # 3. Lógica de salvamento no Excel
            if not os.path.exists(filename):
                df.to_excel(filename, index=False)
            else:
                existing_df = pd.read_excel(filename)
                pd.concat([existing_df, df]).to_excel(filename, index=False)

            # 4. REGISTRO ÚNICO DE LOG (Chamando apenas o módulo externo)
            # Removemos a linha 'self.registrar_log' que causava a duplicata
            registrar_acao(f"Cadastro realizado: {nome}")
            
            print(f"Dados de {nome} salvos com sucesso!")
            self.limpar_campos()
            
        except Exception as e:
            print(f"Erro ao salvar: {e}")
            
    def limpar_campos(self):
        for entry in [self.entry_nome, self.entry_sobrenome, self.entry_val1, self.entry_val2, self.entry_outros]:
            entry.delete(0, 'end')

if __name__ == "__main__":
    app = SistemaTarefas()
    app.mainloop()