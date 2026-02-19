import sys
import os
import pandas as pd
import customtkinter as ctk
from datetime import datetime
from tkinter import messagebox
from dashboard import DashboardFrame

# Mock das funções de log caso o módulo externo não exista
try:
    from registro_log import registrar_acao, buscar_ultimos_logs
except ImportError:
    def registrar_acao(usuario, perfil, acao):
        # Gera o log no formato solicitado
        agora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        print(f"LOG: {agora} | {perfil} | {usuario} | {acao}")

    def buscar_ultimos_logs(filtro):
        return []

class SistemaTarefas(ctk.CTk):
    def __init__(self, user="Admin", funcao="Administrador"): 
        super().__init__() 

        # Dados da Sessão
        self.user = user
        self.funcao = funcao
        self.hora_login = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        # Configuração da Janela
        self.title("Sistema de Cadastro - V1.0.2026")
        self.geometry("1000x650")
        
        # Layout Principal
        self.grid_columnconfigure(0, minsize=250) 
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Inicialização dos Componentes
        self.setup_sidebar()
        
        # Inicialização dos Frames de Conteúdo
        self.main_frame = self.setup_main_frame()
        self.frame_logs = self.setup_logs_frame()
        self.dash_frame = DashboardFrame(self)
        
        # Estado Inicial: Dashboard
        self.mostrar_dashboard()
        self.registrar_evento("Login realizado")

    def registrar_evento(self, acao):
        """Helper para registrar ações com os dados do usuário atual"""
        registrar_acao(self.user, self.funcao, acao)

    
    def mostrar_tela(self, frame_alvo):
        """Gerenciador central: Esconde absolutamente tudo e mostra o alvo"""
        # Lista de todos os frames que seu sistema possui
        frames_sistema = [
            self.main_frame, 
            self.frame_logs, 
            self.dash_frame,
        ]
        
        # Se o frame de ofertas já foi criado, adiciona ele na lista para esconder
        if hasattr(self, 'ofertas_frame'):
            frames_sistema.append(self.ofertas_frame)

        # Esconde todos
        for frame in frames_sistema:
            if frame:
                frame.grid_forget()
        
        # Mostra apenas o que você clicou
        frame_alvo.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")

    def mostrar_dashboard(self):
        self.dash_frame.atualizar_dados()
        self.mostrar_tela(self.dash_frame)
        self.btn_dash.configure(fg_color=("gray75", "gray25")) # Destaque visual
        self.btn_cadastro.configure(fg_color="transparent")

    def setup_sidebar(self):
        self.sidebar = ctk.CTkFrame(self, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        
        self.logo_label = ctk.CTkLabel(self.sidebar, text="AD-PLATINA", font=("Segoe UI", 24, "bold"))
        self.logo_label.pack(pady=30)

        # Botão Cadastro
        self.btn_cadastro = ctk.CTkButton(self.sidebar, text="Cadastro  ▼", font=ctk.CTkFont(size=18),
                                          fg_color="transparent", anchor="w", command=self.toggle_submenu)
        self.btn_cadastro.pack(fill="x", padx=10, pady=5)
        
        # O frame que vai esconder os dois botoes aseguir
        self.sub_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        
        # Botao dizimo
        self.btn_sub_d = ctk.CTkButton(self.sub_frame, text="  DIZIMOS", font=ctk.CTkFont(size=16),
                                       fg_color="transparent", anchor="w", command=self.abrir_tela_cadastro)
        self.btn_sub_d.pack(fill="x", padx=(30, 15), pady=2)

        # Botao ofertas
        self.btn_sub_o = ctk.CTkButton(self.sub_frame, text="  OFERTAS", font=ctk.CTkFont(size=16),
                                       fg_color="transparent", anchor="w", command=self.abrir_tela_ofertas)
        self.btn_sub_o.pack(fill="x", padx=(30, 15), pady=2)


        # Outros Botões
        self.btn_dash = ctk.CTkButton(self.sidebar, text="Dashboard", font=("Segoe UI", 18), 
                                     fg_color="transparent", anchor="w", command=self.mostrar_dashboard)
        self.btn_dash.pack(fill="x", padx=10, pady=5)

        self.btn_logs = ctk.CTkButton(self.sidebar, text="Logs do Sistema", font=("Segoe UI", 18), 
                                     fg_color="transparent", anchor="w", command=self.abrir_tela_logs)
        self.btn_logs.pack(fill="x", padx=10, pady=5)

        # Rodapé com Usuário e Sair
        self.container_usuario = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        self.container_usuario.pack(side="bottom", fill="x", padx=10, pady=20)

        ctk.CTkLabel(self.container_usuario, text=f"👤  {self.user}", font=("Segoe UI", 16, "bold")
                     ).pack(side="left", padx=(5, 2))
        
        ctk.CTkLabel(self.container_usuario, text="●", text_color="#2ecc71"
                     ).pack(side="left", padx=(0, 5))

        self.btn_sair = ctk.CTkButton(self.container_usuario, text="Sair", fg_color="#cc0000", 
                                     hover_color="#990000", width=60, command=self.encerrar_sistema)
        self.btn_sair.pack(side="right", padx=5)

    def setup_main_frame(self):
        frame = ctk.CTkFrame(self, corner_radius=15)
        ctk.CTkLabel(frame, text="Cadastra Dizimos", font=("Segoe UI", 24, "bold")).pack(pady=20, padx=30, anchor="w")

        self.entry_nome = self.create_input(frame, "Nome ")
        self.entry_val1 = self.create_input(frame, "Dízimos R$ (Ex: 100.50)")
        self.entry_val2 = self.create_input(frame, "Outros valores R$")
        self.entry_outros = self.create_input(frame, "Observações")

        btn_cont = ctk.CTkFrame(frame, fg_color="transparent")
        btn_cont.pack(fill="x", padx=30, pady=20)

        ctk.CTkButton(btn_cont, text="Salvar", text_color="#302828", fg_color="#2eb8ac", 
                    hover_color="#248f85", font=("Segoe UI", 18, "bold"), height=45, 
                    command=self.salvar_dados).pack(side="left", expand=True, fill="x", padx=(0, 10))

        ctk.CTkButton(btn_cont, text="Limpar", text_color="#302828", fg_color="#f09644", 
                    hover_color="#c77b38", font=("Segoe UI", 18, "bold"), height=45,
                    command=self.limpar_campos).pack(side="left", expand=True, fill="x")
        return frame

    def setup_logs_frame(self):
        frame = ctk.CTkFrame(self, corner_radius=15)
        ctk.CTkLabel(frame, text="Histórico de Atividades", font=("Segoe UI", 20, "bold")).pack(pady=10)
        
        self.txt_logs = ctk.CTkTextbox(frame, font=("Consolas", 12))
        self.txt_logs.pack(padx=20, pady=10, fill="both", expand=True)
        
        ctk.CTkButton(frame, text="Atualizar Logs", command=self.atualizar_visualizacao_logs).pack(pady=5)
        return frame

    def create_input(self, master, placeholder):
        entry = ctk.CTkEntry(master, placeholder_text=placeholder, height=40)
        entry.pack(fill="x", padx=30, pady=8)
        return entry

    def toggle_submenu(self):
        if self.sub_frame.winfo_manager():
            self.sub_frame.pack_forget()
        else:
            self.sub_frame.pack(fill="x", after=self.btn_cadastro)

    def abrir_tela_logs(self):
        self.mostrar_tela(self.frame_logs)
        self.atualizar_visualizacao_logs()

    def abrir_tela_cadastro(self):
        self.mostrar_tela(self.main_frame)

    def atualizar_visualizacao_logs(self):
        self.txt_logs.configure(state="normal")
        self.txt_logs.delete("1.0", "end")
        logs = buscar_ultimos_logs("")
        
        if logs:
            for log in logs:
                # Exibe formatado: Data | Perfil | Usuário | Ação
                self.txt_logs.insert("end", f"[{log.get('Data/Hora Login')}] {log.get('Perfil')} - {log.get('Usuário')}: {log.get('Ação')}\n")
        else:
            self.txt_logs.insert("end", "Logs offline ou nenhum registro encontrado.")
        self.txt_logs.configure(state="disabled")

    def salvar_dados(self):
        nome = self.entry_nome.get().strip()
        filename = 'base_tarefas.xlsx'
        
        if not nome:
            messagebox.showwarning("Aviso", "O nome é obrigatório.")
            return 

        try:
            val_d = float(self.entry_val1.get().replace(',', '.')) if self.entry_val1.get() else 0.0
            val_o = float(self.entry_val2.get().replace(',', '.')) if self.entry_val2.get() else 0.0
            
            # Verificação de existência
            if os.path.exists(filename):
                df_e = pd.read_excel(filename)
                if not df_e.empty and 'Nome' in df_e.columns:
                    if nome.upper() in df_e['Nome'].astype(str).str.upper().values:
                        if not messagebox.askyesno("Confirmar", f"{nome} já existe. Adicionar novo lançamento?"):
                            return

            # Novo registro
            novo_reg = pd.DataFrame([{
                'Nome': nome,
                'Dizimos': val_d,
                'Ofertas': val_o,
                'Outros': self.entry_outros.get(),
                'Data_Criacao': datetime.now().strftime("%d/%m/%Y"),
                'Responsavel': self.user
            }])

            if not os.path.exists(filename):
                novo_reg.to_excel(filename, index=False)
            else:
                df_atual = pd.read_excel(filename)
                pd.concat([df_atual, novo_reg], ignore_index=True).to_excel(filename, index=False)

            self.registrar_evento(f"Lançamento: {nome} (Total: R$ {val_d + val_o})")
            messagebox.showinfo("Sucesso", "Dados salvos com sucesso!")
            self.limpar_campos()

        except ValueError:
            messagebox.showerror("Erro", "Valores numéricos inválidos.")
        except PermissionError:
            messagebox.showerror("Erro", "Feche o arquivo Excel antes de salvar.")

    def limpar_campos(self):
        for entry in [self.entry_nome, self.entry_val1, self.entry_val2, self.entry_outros]:
            entry.delete(0, 'end')

    def encerrar_sistema(self):
        self.registrar_evento(f"Logout realizado (Entrada: {self.hora_login})")
        self.quit()
        self.destroy()
        sys.exit(0)

    def abrir_tela_ofertas(self):
        if not hasattr(self, 'ofertas_frame'):
            self.setup_ofertas_frame()
        self.mostrar_tela(self.ofertas_frame)

    def setup_ofertas_frame(self):
        """Frame de Cadastro de Ofertas com Validação de Dia"""
        self.ofertas_frame = ctk.CTkFrame(self, corner_radius=15)

        ctk.CTkLabel(self.ofertas_frame, text="Lançamento de Ofertas", 
                     font=("Segoe UI", 24, "bold")).pack(pady=(20, 10), padx=30, anchor="w")

        # Label de Instrução Forçada
        ctk.CTkLabel(self.ofertas_frame, text="⚠️ Selecione obrigatoriamente o dia do culto:",
                     text_color="#ffcc00", font=("Segoe UI", 13, "bold")).pack(padx=30, anchor="w", pady=(10, 0))

        dias_opcoes = [
            "Escola Dominical", "Cuto da Familha", "Circulo de Oração", "Quinta Profética", 
            "Culto de Missões", "Culto de Ceia", "Outros"
        ]

        # ComboBox sem valor padrão inicial
        self.combo_dia = ctk.CTkComboBox(self.ofertas_frame, values=dias_opcoes, width=400, height=45, state="readonly")
        self.combo_dia.pack(fill="x", padx=30, pady=5)
        self.combo_dia.set("--- CLIQUE PARA SELECIONAR ---") # Texto de instrução

        self.entry_oferta_val = self.create_input_no_frame(self.ofertas_frame, "Valor Arrecadado R$")
        self.entry_obs_oferta = self.create_input_no_frame(self.ofertas_frame, "Observações Adicionais")

        # Botão Salvar
        btn_salvar = ctk.CTkButton(self.ofertas_frame, text="Registrar Oferta", text_color="#302828",fg_color="#2eb8ac", 
                    hover_color="#248f85", font=("Segoe UI", 18, "bold"), height=50,
                    command=self.salvar_oferta_excel)
        btn_salvar.pack(fill="x", padx=30, pady=20)

    def create_input_no_frame(self, master, placeholder):
        """Helper para criar inputs rapidamente"""
        entry = ctk.CTkEntry(master, placeholder_text=placeholder, height=45)
        entry.pack(fill="x", padx=30, pady=10)
        return entry

    def salvar_oferta_excel(self):
        dia_selecionado = self.combo_dia.get()
        valor_str = self.entry_oferta_val.get().replace(',', '.')
        observacao_texto = self.entry_obs_oferta.get().strip()
        
        # 1. VALIDAÇÃO DO DIA (Obrigatória)
        if dia_selecionado == "--- CLIQUE PARA SELECIONAR ---" or not dia_selecionado:
            messagebox.showwarning("Campo Obrigatório", "Você precisa selecionar o DIA DO CULTO para continuar!")
            self.combo_dia.configure(border_color="#FF4B4B") # Destaca o erro em vermelho
            return
        else:
            self.combo_dia.configure(border_color="#333333") # Volta ao normal se ok

        # 2. VALIDAÇÃO DO VALOR
        if not valor_str:
            messagebox.showwarning("Campo Obrigatório", "Insira o valor arrecadado.")
            return

        try:
            valor = float(valor_str)
            filename = 'base_ofertas.xlsx'
            
            # (Restante da lógica de salvamento em Excel...)
            nova_oferta = pd.DataFrame([{
                'Data': datetime.now().strftime("%d/%m/%Y"),
                'Dia_Culto': dia_selecionado,
                'Valor': valor,
                'Observacao': observacao_texto,
                'Responsavel': self.user
            }])

            if not os.path.exists(filename):
                nova_oferta.to_excel(filename, index=False)
            else:
                df_existente = pd.read_excel(filename)
                pd.concat([df_existente, nova_oferta], ignore_index=True).to_excel(filename, index=False)

            messagebox.showinfo("Sucesso", f"Oferta de {dia_selecionado} registrada!")
            
            # Limpeza após sucesso
            self.combo_dia.set("--- CLIQUE PARA SELECIONAR ---")
            self.entry_oferta_val.delete(0, 'end')
            self.entry_obs_oferta.delete(0, 'end')

        except ValueError:
            messagebox.showerror("Erro", "Valor numérico inválido.")
        except PermissionError:
            messagebox.showerror("Erro", "Feche o arquivo 'base_ofertas.xlsx' antes de salvar.")

if __name__ == "__main__":
    app = SistemaTarefas()
    app.mainloop()